#coding=utf-8
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import login as djangologin
from django.contrib.auth import logout as djangologout

from html5helper.decorator import render_json
from smart_auth.utils import check_auth_for_api, EasyUIPager,\
    check_superuser_for_api, MenuPermission
from smart_auth.forms import UserChangePasswordForm, GroupPermissionUpdateForm, GroupUserUpdateForm
from smart_auth.utils import PermissionUpdator, permission_serializer, group_serializer



@render_json
def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
        
    if request.user.is_authenticated():
        {"is_ok":True}

    user = authenticate(username=username, password=password)
    if not user:
        return {"is_ok":False, "reason":u"用户不存在或密码错误"}
    
    djangologin(request, user)
    return {"is_ok":True}


@render_json
def logout(request):
    djangologout(request)
    return {"is_ok":True}


@render_json
@check_auth_for_api
def get_my_menus(request):
    return {"is_ok": True, "menus": MenuPermission(request.user).my_menus()}



@render_json
@check_auth_for_api
def change_password(request):
    form = UserChangePasswordForm(request.POST)
    if form.is_valid() is False:
        return {"is_ok": False, "reason": form.errors}
    
    if authenticate(username=request.user.username, password=form.cleaned_data["old_password"]) == None:
        return {"is_ok": False, "reason": u"密码不对"}
    
    if form.cleaned_data["new_password"] != form.cleaned_data["new_password1"]:
        return {"is_ok": False, "reason": u"密码不一致"}
    
    request.user.set_password(form.cleaned_data["new_password"])
    request.user.save()
    
    return {"is_ok": True}


##########################
# only for superuser
##########################

@render_json
@check_superuser_for_api
def all_permission(request):
    content_type = request.GET.get("content_type")
    
    updator = PermissionUpdator()
    permissions = []
    
    if content_type:
        if content_type == updator.MENU_MODEL:
            permissions = Permission.objects.filter(content_type=updator.menu_content_type)
        elif content_type == updator.API_MODEL:
            permissions = Permission.objects.filter(content_type=updator.api_content_type)
    else:
        permissions = Permission.objects.filter(content_type__in=[updator.api_content_type, updator.menu_content_type])
    
    return EasyUIPager(permissions, request, permission_serializer).query()


@render_json
@check_superuser_for_api
def all_group(request):
    groups = Group.objects.all()
    return EasyUIPager(groups, request, group_serializer).query()


@render_json
@check_superuser_for_api
def group_permission_add(request):
    form = GroupPermissionUpdateForm(request.POST)
    if form.is_valid() is False:
        return {"is_ok": False, "reason": form.errors}
    
    group = form.cleaned_data["group"]
    permission = form.cleaned_data["permission"]
    
    group.permissions.add(permission)
    return{"is_ok": True}


@render_json
@check_superuser_for_api
def group_permission_delete(request):
    form = GroupPermissionUpdateForm(request.POST)
    if form.is_valid() is False:
        return {"is_ok": False, "reason": form.errors}
    
    group = form.cleaned_data["group"]
    permission = form.cleaned_data["permission"]
    
    group.permissions.remove(permission)
    return{"is_ok": True}


@render_json
@check_superuser_for_api
def group_user_add(request):
    form = GroupUserUpdateForm(request.POST)
    if form.is_valid() is False:
        return {"is_ok": False, "reason": form.errors}
    
    group = form.cleaned_data["group"]
    user = form.cleaned_data["user"]
    
    if user.groups.filter(id=group.id).count() > 0:
        return {"is_ok": False, "reason": u"已经加入了组"}
    
    user.groups.add(group)
    return{"is_ok": True}


@render_json
@check_superuser_for_api
def group_user_delete(request):
    form = GroupUserUpdateForm(request.POST)
    if form.is_valid() is False:
        return {"is_ok": False, "reason": form.errors}
    
    group = form.cleaned_data["group"]
    user = form.cleaned_data["user"]
    
    user.groups.remove(group)
    return {"is_ok": True}

