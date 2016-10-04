#coding=utf-8
import math
import os
import copy
import types
import importlib

from django.conf import settings
from django.contrib.auth.models import Permission, ContentType, User as DjangoUser
from django.contrib.auth import authenticate

from html5helper.utils import do_paginator
from smart_auth.resolver import resolve_to_name



def check_auth_for_api(view_func):
    """ mobile GET must have secret="", return dict
    """
    def wrap(request, *args, **kwargs):
        if request.user and request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        
        secret = request.GET.get("_secret") or request.POST.get("_secret")
        if secret:
            user = authenticate(secret=secret)
            if user:
                request.user = user
                return view_func(request, *args, **kwargs)
        
        login_error = {"is_ok":False, "reason":u"登陆凭证已经失效，请重新登陆", "login_timeout":True}
        return login_error
    
    return wrap


def check_superuser_for_api(view_func):
    """ you must been super user
    """
    def wrap(request, *args, **kwargs):
        secret = request.GET.get("_secret") or request.POST.get("_secret")
        if secret:
            request.user = authenticate(secret=secret)
                
        if request.user and request.user.is_authenticated() and request.user.is_superuser == True and request.user.is_active == True:
            return view_func(request, *args, **kwargs)
        
        login_error = {"is_ok":False, "reason":u"你不是超级管理员"}
        return login_error
    
    return wrap


def check_permission_for_api(view_func):
    """ mobile GET must have secret="", return dict
    """
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated() is False:
            secret = request.GET.get("_secret") or request.POST.get("_secret")
            if secret:
                user = authenticate(secret=secret)
                if not user:
                    return {"is_ok": False, "reason": u"登陆凭证失效了，请重新登陆"}
                
                request.user = user
            else:
                return {"is_ok": False, "reason": u"登陆凭证失效了，请重新登陆"}
        
        api_permission = APIPermission(request.user, request.path)
        if api_permission.has_perm():
            return view_func(request, *args, **kwargs)
        
        return {"is_ok": False, "reason": u"权限 '%s' 不存在" % api_permission.view_name}
    
    return wrap


def permission_serializer(permission):
    result = {"id": permission.id, "name": permission.name, "codename": permission.codename}
    result["content_type"] = {
        "id": permission.content_type.id,
        "model": permission.content_type.model,
    }
    
    return result    


def user_serializer(user):
    data = {"id": user.id, "email": user.email, "username": user.username}
    return data


def group_serializer(grp):    
    result = {"id": grp.id, "name": grp.name}
    updator = PermissionUpdator()
    
    group_permissions = grp.permissions.all()
    codename_group_permissions = {}
    for item in group_permissions:
        codename_group_permissions[item.codename] = item
    
    permissions = Permission.objects.filter(content_type__in=[updator.api_content_type, updator.menu_content_type])
    codename_permissions = {}
    for item in permissions:
        codename_permissions[item.codename] = item
        
    result["menu_permissions"] = settings.MENUS
    for parent in result["menu_permissions"]:
        parent_codename = updator._pack_menu_codename(None, parent)
        parent["id"] = codename_permissions[parent_codename].id if parent_codename in codename_permissions else None
        parent["checked"] = parent_codename in codename_group_permissions
        for child in parent['children']:
            child_codename = updator._pack_menu_codename(parent, child)
            child["id"] = codename_permissions[child_codename].id if child_codename in codename_permissions else None
            child["checked"] = child_codename in codename_group_permissions
            
    result["api_permissions"] = []
    for _, item in codename_permissions.iteritems():
        if item.content_type == updator.menu_content_type:
            continue
        data = permission_serializer(item)
        data["checked"] = item.codename in codename_group_permissions
        result["api_permissions"].append(data)
    result["api_permissions"].sort(key=lambda x: x["codename"])
    
    result["users"] = [user_serializer(x) for x in DjangoUser.objects.filter(groups__id=grp.id)]
    result["users_count"] = len(result["users"])
    
    return result


class APIPermission(object):
    
    def __init__(self, user, path):
        self.user = user
        self.path = path
        self.view_name = resolve_to_name(path)
        
    def has_perm(self):
        perm = "smart_auth.%s" % self.view_name
        return self.user.has_perm(perm)


class MenuPermission:
    
    def __init__(self, user):
        self.user = user
        self.menus = settings.MENUS
        self.updator = PermissionUpdator()
    
    def my_menus(self):
        """ Return list of menus, format is:
        [
            {'text': "", 'url':'', 'children': [
                {'text':"", 'url':'', },
            ]},
            ....
        ]
        """
        result = []
        
        for parent in self.menus: 
            new_parent = copy.deepcopy(parent)
            new_parent["children"] = []
            
            for menu in parent["children"]:
                new_menu = copy.deepcopy(menu)
                if not new_menu["url"]:
                    continue
                if self._can_show(parent, menu) is False:
                    continue
                
                new_parent["children"].append(new_menu)
        
            if len(new_parent['children']) == 0:
                continue
            
            result.append(new_parent)
        
        return result  
    
    def _can_show(self, parent, menu):
        perm = u"smart_auth.%s" % (self.updator._pack_menu_codename(parent, menu)) 
        return self.user.has_perm(perm)



class PermissionUpdator(object):
    
    def __init__(self):
        self.API_MODEL = "API"
        self.MENU_MODEL = "MENU"
        self.APP_LABEL = "smart_auth"
        self.menus = settings.MENUS
        self.apis_dir = settings.APIS_DIR
        self.apis_prefix = settings.APIS_PREFIX
        
        self.api_content_type, _ = ContentType.objects.get_or_create(app_label=self.APP_LABEL, model=self.API_MODEL)
        self.menu_content_type, _ = ContentType.objects.get_or_create(app_label=self.APP_LABEL, model=self.MENU_MODEL)
            
    def update(self):
        self._update_apis()
        self._update_menus()
    
    def _update_apis(self):
        workdir = self.apis_dir
        code_files = os.listdir(workdir)
        for code_file in code_files:
            if code_file == "__init__.py" or code_file.find(".pyc") > 0 or code_file == "." or code_file == "..":
                continue
            
            mod_name = "%s.%s" % (self.apis_prefix, code_file.split(".")[0])
            mod = importlib.import_module(mod_name)
            for function in dir(mod):
                if function.find("__") == 0 or function.find("_") == 0:
                    continue
                
                if isinstance(getattr(mod, function), types.FunctionType) is False:
                    continue
                
                if hasattr(mod.__dict__[function], "__permission_name__") is False:
                    continue
                
                permission_name = getattr(mod.__dict__[function], "__permission_name__")
               
                codename = self._pack_api_codename(code_file, function)
                permission, _ = Permission.objects.get_or_create(content_type=self.api_content_type, codename=codename)
                permission.name = permission_name
                permission.save()
    
    def _pack_api_codename(self, code_file, view_name):
        mod_name = "%s.%s" % (self.apis_prefix, code_file.split(".")[0])
        return "%s.%s" % (mod_name, view_name)
    
    def _update_menus(self):
        for menu in self.menus:
            Permission.objects.get_or_create(name=menu['text'], content_type=self.menu_content_type, codename=self._pack_menu_codename(None, menu))
            for child in menu["children"]:
                Permission.objects.get_or_create(name=u"%s:%s" % (menu["text"], child["text"]), content_type=self.menu_content_type, 
                                                 codename=self._pack_menu_codename(menu, child))
        
    def _pack_menu_codename(self, parent, menu):
        if parent:
            return u"%s:%s:%s" % (parent["text"], menu["text"], menu["url"])
        
        return u"%s:%s" % (menu["text"], menu["url"])
    

class EasyUIPager(object):
    
    def __init__(self, queryset, request, serializer=None):
        self.queryset = queryset
        self.request = request
        self.serializer = serializer
        
    def query(self):
        """ return dict
        """
        page = int(self.request.GET.get("page", '1'))
        rows = int(self.request.GET.get("rows", '10'))
        sort = self.request.GET.get("sort", "id")
        order = self.request.GET.get("order", "desc")
        
        result = {"is_ok":True, "rows":[], "total":0, "page": page, "total_page":0}
        
        def get_order(o):
            return "" if o == "asc" else "-"
        
        if sort and isinstance(self.queryset, types.ListType) is False:
            items = self.queryset.order_by("%s%s" % (get_order(order), sort))
        else:
            items = self.queryset
            
        pager = do_paginator(items, page, rows)
        result["total"] = pager.paginator.count
        result["rows"] = []
        for row in pager:
            if hasattr(row, "as_json"):
                result["rows"].append(row.as_json())
            elif self.serializer:
                result["rows"].append(self.serializer(row))
            else:
                result["rows"].append(row)
        result["total_page"] = math.ceil(float(result["total"])/rows)
        
        return result
        
