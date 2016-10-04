#encoding=utf-8
from django.conf.urls import patterns, url, include
from django.contrib.auth import views as auth_views


#apis 
user_api_urls = patterns("smart_auth.apis.user", 
    url(r"^login/$", "login"),
    url(r"^logout/$", "logout"),
    url(r"^change/password/", "change_password"),
    
    url(r"^my/menus/$", "get_my_menus"),
    
    url(r"^permission/all/$", "all_permission"),
    url(r"^group/all/$", "all_group"),
    url(r"^group/permission/add/$", "group_permission_add"),
    url(r"^group/permission/delete/$", "group_permission_delete"),
    url(r"^group/user/add/$", "group_user_add"),
    url(r"^group/user/delete/$", "group_user_delete"),
)

demo_api_urls = patterns("smart_auth.apis.demo", 
    url(r"^demo/api/$", "demo_api"),
)


apis_urls = patterns("skill.apis",
    url(r"^user/", include(user_api_urls)),
    url(r"^demo/", include(demo_api_urls)),
)


####################


urlpatterns = patterns("smart_auth.views",
    url(r"^api/", include(apis_urls)),
    
    url(r'^admin/password_reset/$', auth_views.password_reset, name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
)



