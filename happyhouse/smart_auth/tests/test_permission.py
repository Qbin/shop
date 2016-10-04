#encoding=utf-8
import json

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser, Group, Permission

from smart_auth.utils import APIPermission, MenuPermission, PermissionUpdator


        
class TestPermissionUpdateCommand(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.user = DjangoUser.objects.create_user(username="xxx", password="xxx")
        self.group = Group.objects.create(name="sss")
        self.user.groups.add(self.group)
        self.client = Client()
        self.logined_client = Client()
        self.logined_client.login(username=self.user.username, password=self.user.username)
        
    def tearDown(self):
        TestCase.tearDown(self)
        self.user.delete()
        self.group.delete()
        
    def test_update(self):
        updator = PermissionUpdator()
        updator.update()
        
        api_permissions = Permission.objects.filter(content_type=updator.api_content_type)
        self.assertGreater(api_permissions.count(), 0)
        
        category_tree_permission = Permission.objects.get(content_type=updator.api_content_type,  
                                                          codename="smart_auth.apis.demo.demo_api")
        self.assertIsNotNone(category_tree_permission)
        
        menu_permissions = Permission.objects.filter(content_type=updator.menu_content_type)
        self.assertGreater(menu_permissions.count(), 0)


class TestAPIPermission(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.user = DjangoUser.objects.create_user(username="xxx", password="xxx")
        self.client = Client()
        self.logined_client = Client()
        self.logined_client.login(username=self.user.username, password=self.user.username)
        self.updator = PermissionUpdator()
        self.updator.update()
        
    def tearDown(self):
        TestCase.tearDown(self)
        self.user.delete()
        self.updator.api_content_type.delete()
        self.updator.menu_content_type.delete()
        
    def test_has_perm_failed(self):
        url = reverse("smart_auth.apis.demo.demo_api")
        api_permission = APIPermission(self.user, url)
        self.assertFalse(api_permission.has_perm())
        
    def test_has_perm_ok(self):
        url = reverse("smart_auth.apis.demo.demo_api")
        permission = Permission.objects.get(content_type=self.updator.api_content_type, codename="smart_auth.apis.demo.demo_api")
        self.user.user_permissions.add(permission)
        
        api_permission = APIPermission(self.user, url)
        print api_permission.view_name
        self.assertTrue(api_permission.has_perm())
        
        
class TestMenuPermission(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.user = DjangoUser.objects.create_user(username="xxx", password="xxx")
        self.client = Client()
        self.logined_client = Client()
        self.logined_client.login(username=self.user.username, password=self.user.username)
        self.updator = PermissionUpdator()
        self.updator.update()
        
    def tearDown(self):
        TestCase.tearDown(self)
        self.user.delete()
        self.updator.api_content_type.delete()
        self.updator.menu_content_type.delete()
        
    def test_has_perm_failed(self):
        menu_permission = MenuPermission(self.user)
        menus = menu_permission.my_menus()
        self.assertEqual(len(menus), 0)
        
    def test_has_perm_ok(self):
        menu_permission = MenuPermission(self.user)
        permissions = Permission.objects.filter(content_type=self.updator.menu_content_type)
        for item in permissions:
            print u"%d, %s, %s, %s" % (item.id, item.name, item.content_type, item.codename)
        
        codename = u"%s:%s:%s" % (menu_permission.menus[0]["text"], menu_permission.menus[0]['children'][0]['text'], 
                                  menu_permission.menus[0]['children'][0]['url'])
        permission = Permission.objects.get(content_type=self.updator.menu_content_type, 
                                            codename=codename)
        self.user.user_permissions.add(permission)
        
        menus = menu_permission.my_menus()
        print menus
        
        self.assertEqual(len(menus), 1)
        
        self.user.user_permissions.remove(permission)
        
        

class TestUserApi(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.user = DjangoUser.objects.create_user(username="xxx", password="xxx")
        self.user.is_active = True
        self.user.is_superuser = True
        self.user.save()
        self.group = Group.objects.create(name="11122")
        self.user.groups.add(self.group)
        
        self.member_group = Group.objects.create(name="wwee")
        
        self.client = Client()
        self.logined_client = Client()
        self.logined_client.login(username=self.user.username, password=self.user.username)
        self.permission_updator = PermissionUpdator()
        self.permission_updator.update()
        
    def tearDown(self):
        TestCase.tearDown(self)
        self.user.delete()
        self.group.delete()
        self.member_group.delete()
        self.permission_updator.api_content_type.delete()
        self.permission_updator.menu_content_type.delete()
        
    def test_login(self):
        data = {"username":"xxx", "password":"kkkk"}
        url = reverse("smart_auth.apis.user.login")
        
        resp = self.client.post(url, data)
        result = json.loads(resp.content)
        self.assertFalse(result["is_ok"])
        
    def test_login_with_ok(self):
        data = {"username":self.user.username, "password":self.user.username}
        url = reverse("smart_auth.apis.user.login")
        
        resp = self.client.post(url, data)
        result = json.loads(resp.content)
        self.assertTrue(result["is_ok"])
              
    def test_logout(self):
        url = reverse("smart_auth.apis.user.logout")
        
        resp = self.client.get(url)
        result = json.loads(resp.content)
        self.assertTrue(result["is_ok"])
        
    def test_get_my_menus(self):
        url = reverse("smart_auth.apis.user.get_my_menus")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        
    def test_all_permission(self):
        url = reverse("smart_auth.apis.user.all_permission")
        resp = self.logined_client.get(url)
        self.assertEqual(resp.status_code, 200)
        
        result = json.loads(resp.content)
        self.assertTrue(result["is_ok"])
        
    def test_all_group(self):
        group = Group.objects.create(name="hello")
        url = reverse("smart_auth.apis.user.all_group")
        resp = self.logined_client.get(url)
        self.assertEqual(resp.status_code, 200)
        
        result = json.loads(resp.content)
        self.assertTrue(result["is_ok"])
        
        group.delete()
        
    def test_group_permission_add(self):
        group = Group.objects.create(name="hello")
        user = DjangoUser.objects.create_user(username="kkiioo")
        user.groups.add(group)
        permission = Permission.objects.filter(content_type=self.permission_updator.menu_content_type)[0]
        
        url = reverse("smart_auth.apis.user.group_permission_add")
        resp = self.logined_client.post(url, {"group": group.id, "permission": permission.id})
        self.assertEqual(resp.status_code, 200)
        
        result = json.loads(resp.content)
        self.assertTrue(result["is_ok"])
        
        self.assertTrue(user.has_perm("smart_auth.%s" % permission.codename))
        
        group.delete()
        user.delete()
        
    def test_group_permission_delete(self):
        group = Group.objects.create(name="hello")
        user = DjangoUser.objects.create_user(username="kkiioo")
        user.groups.add(group)
        permission = Permission.objects.filter(content_type=self.permission_updator.menu_content_type)[0]
        
        url = reverse("smart_auth.apis.user.group_permission_delete")
        resp = self.logined_client.post(url, {"group": group.id, "permission": permission.id})
        self.assertEqual(resp.status_code, 200)
        
        result = json.loads(resp.content)
        self.assertTrue(result["is_ok"])
        
        self.assertFalse(user.has_perm("skill.%s" % permission.codename))
        
        user.delete()
        group.delete()
    
    def test_group_user_add(self):
        group = Group.objects.create(name="hello")
        user = DjangoUser.objects.create_user(username="kkiioo")
        
        url = reverse("smart_auth.apis.user.group_user_add")
        resp = self.logined_client.post(url, {"group": group.id, "user": user.id})
        self.assertEqual(resp.status_code, 200)
        
        result = json.loads(resp.content)
        self.assertTrue(result["is_ok"])
        
        self.assertTrue(group in user.groups.all())
        
        group.delete()
        user.delete()
        
    def test_group_user_delete(self):
        group = Group.objects.create(name="hello")
        user = DjangoUser.objects.create_user(username="kkiioo")
        
        url = reverse("smart_auth.apis.user.group_user_delete")
        resp = self.logined_client.post(url, {"group": group.id, "user": user.id})
        self.assertEqual(resp.status_code, 200)
        
        result = json.loads(resp.content)
        self.assertTrue(result["is_ok"])
        
        self.assertTrue(group not in user.groups.all())
        
        group.delete()
        user.delete()
        
    
    
        