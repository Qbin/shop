#!/bin/env python
# coding=utf-8
''' all decorator functions.
'''

import csv
import types
import json
from urlparse import urljoin

from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.utils.encoding import smart_str
from django.core.urlresolvers import reverse
from django.templatetags.static import PrefixNode


def render_template(template, **kwargs):
    new_kwargs = {"settings": settings}
    
    if kwargs.has_key("settings"):
        kwargs.pop("settings")
        
    if kwargs.has_key("request"):
        request = kwargs["request"]
    
    if not kwargs.has_key("current_nav"):
        if kwargs.has_key("breadcrumbs") and kwargs['breadcrumbs']:
            kwargs["current_nav"] = kwargs["breadcrumbs"][-1]["title"]
        else:
            kwargs["current_nav"] = None
        
    new_kwargs.update(kwargs)
    
    if request:
        instance = RequestContext(request)
        return render_to_response(template, new_kwargs, context_instance = instance)
    
    return render_to_response(template, new_kwargs)


def render_json_auth(check_auth=False):
    """ render http response to json decorator
    """
    def do_wrap(view_func):
        
        def wrap(request, *args, **kwargs):
            if check_auth:
                if request.user.is_authenticated() is False:
                    return {"is_ok":False, "reason":u"请先登陆"}
            
            retval = view_func(request, *args, **kwargs)
            if isinstance(retval, HttpResponse):
                retval.mimetype = 'application/json; charset=utf-8'
                return retval
            else:
                js = json.dumps(retval)
                return HttpResponse(js, content_type='application/json; charset=utf-8')
        
        return wrap
    
    return do_wrap


def render_json(view_func):
    """ render http response to json decorator
    """
    def wrap(request, *args, **kwargs):
        retval = view_func(request, *args, **kwargs)
        if isinstance(retval, HttpResponse):
            retval.mimetype = 'application/json; charset=utf-8'
            if settings.DEBUG:
                retval["Access-Control-Allow-Origin"] = "*"
            return retval
        else:
            js = json.dumps(retval)
            resp = HttpResponse(js, content_type='application/json; charset=utf-8')
            if settings.DEBUG:
                resp["Access-Control-Allow-Origin"] = "*"
            return resp
    return wrap



def render_csv(view_func, encoding="gbk"):
    """ render http response to csv
    """
    def wrap(request, *args, **kwargs):
        # data_list is list of list, for example [["a", "b"], ["a1", "a2"]]
        attachment_name, data_list = view_func(request, *args, **kwargs)
        response = HttpResponse(mimetype = "text/csv")
        response['Content-Disposition'] = u"attachment; filename=\"%s\"" % attachment_name
        writer = csv.writer(response)
        for data in data_list:
            row = []
            for cell in data:
                if not isinstance(cell, types.UnicodeType):
                    row.append(smart_str(u"%s" % cell, encoding = encoding))
                else:
                    row.append(smart_str(cell, encoding = encoding))
            writer.writerow(row)
        return response
    return wrap


def site_url(path):
    """ return url contain domain
    """
    host = settings.APP_DOMAIN
    while host[-1] == "/":
        host = host.strip("/")
    return "http://%s%s" % (host, path)


def reverse_site_url(name, args = None, kwargs = None):
    path = reverse(name, args = args, kwargs = kwargs)
    return "http://%s%s" % (settings.APP_DOMAIN, path)


def static(path):
    return urljoin(PrefixNode.handle_simple("STATIC_URL"), path)