#coding=utf-8
""" test fields
"""

from django.test import TestCase
from html5helper import fields


class TestCharField(TestCase):
    def test_new(self):
        field = fields.CharField()
        self.assertIsNotNone(field)
        
        
class TestTextField(TestCase):
    def test_new(self):
        textarea = fields.TextField(rows= 5, placeholder="gggg")
        self.assertIsNotNone(textarea)
        
    
class TestPasswordField(TestCase):
    def test_new(self):
        ctrl = fields.PasswordField(placeholder="gggg")
        self.assertIsNotNone(ctrl)
        

class TestIntegerField(TestCase):
    def test_new(self):
        ctrl = fields.IntegerField(placeholder="gggg")
        self.assertIsNotNone(ctrl)


class TestMarkdownField(TestCase):
    def test_new(self):
        ctrl = fields.MarkdownField()
        self.assertIsNotNone(ctrl)

        

class TestChoiceField(TestCase):
    def test_new(self):
        ctrl = fields.ChoiceField(choices=((0, "1"), (1, "2")))
        self.assertIsNotNone(ctrl)

