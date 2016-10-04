#encoding=utf-8
import datetime
import random
import hashlib
import types

from django.db import models
from django.contrib.auth.models import User as DjangoUser



class BaseModel(models.Model):
    
    class Meta:
        abstract = True
        ordering = ["-id"]
        
    def as_json(self):
        data = {}
        field_names = self._meta.get_all_field_names()
        for name in field_names:
            if hasattr(self, name) is False:
                continue
            field = getattr(self, name)
            
            if isinstance(field, datetime.datetime):
                data[name] = field.strftime("%Y-%m-%d %H:%M:%S")
            elif field == None:
                data[name] = None
            elif isinstance(field, types.BooleanType):
                data[name] = field
            elif isinstance(field, types.LongType) or isinstance(field, types.IntType):
                data[name] = field
            elif isinstance(field, types.FloatType):
                data[name] = field
            else:
                data[name] = u"%s" % field
                
        return data
    
    
    def _get_choice(self, choices, select_id):
        for item in choices:
            if item[0] == select_id:
                return item
        
        return None


#################
# end server auth
#################


class Token(BaseModel):
    user = models.ForeignKey(DjangoUser, related_name="token_user")
    secret = models.CharField(max_length = 128, unique = True)
    add_datetime = models.DateTimeField(auto_now_add=True)
        
    @classmethod
    def generate(cls, user):
        try:
            token = cls.objects.get(user = user)
        except:
            token = None
        secret = hashlib.md5("%s%s%s%d" % (user.username, user.id, 
                                       datetime.datetime.now().strftime("%Y%m%d%H%M%S"), 
                                       random.randint(1, 99999999))).hexdigest()
        if token is None:
            token = cls.objects.create(user = user, secret = secret)
        elif token.is_expires:
            token.secret = secret
            token.expires_datetime = datetime.datetime.now() + datetime.timedelta(365)
            token.save()
        return token
    
    @property
    def is_expires(self):
        return False
    
    
class TokenBackend(object):
    """ used for authenticate
    """
    def authenticate(self, secret=None):
        # Check the token and return a User.
        try:
            token = Token.objects.get(secret=secret)
        except:
            return None

        return token.user
    
    def get_user(self, user_id):
        try:
            return DjangoUser.objects.get(pk=user_id)
        except DjangoUser.DoesNotExist:
            return None
