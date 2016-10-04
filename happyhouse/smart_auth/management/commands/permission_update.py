# coding=utf-8

from django.core.management.base import BaseCommand

from html5helper.utils import wrapper_raven
from smart_auth.utils import PermissionUpdator

                

class Command(BaseCommand):
    args = ""
    help = "Update permission table."
    
    @wrapper_raven
    def handle(self, *args, **options):
        updator = PermissionUpdator()
        updator.update()
             
        
    
    
                    
            