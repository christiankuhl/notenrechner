from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from functools import wraps

class UserOwnedManager(models.Manager):
    """
    Wraps standard Manager query methods to enforce all calls
    made through this manager to be made within a user context.
    To be used together with the restricted_to_owner decorator
    defined below.
    """
    owner = None
    def all(self):
        return super(UserOwnedManager, self).filter(owner=UserOwnedManager.owner)
    def filter(self, **kwargs):
        return super(UserOwnedManager, self).filter(owner=UserOwnedManager.owner, **kwargs)
    def exclude(self, **kwargs):
        return self.filter(UserOwnedManager.owner).exclude(**kwargs)
    def get(self, *args, **kwargs):
        return super(UserOwnedManager, self).get(owner=UserOwnedManager.owner, *args, **kwargs)
    def create(self, **kwargs):
        return super(UserOwnedManager, self).create(owner=UserOwnedManager.owner, **kwargs)
    def get_or_create(self, defaults=None, **kwargs):
        if defaults is None:
            defaults = {}
        defaults['owner'] = UserOwnedManager.owner
        return super(UserOwnedManager, self).get_or_create(owner=UserOwnedManager.owner, defaults=defaults, **kwargs)
    def update_or_create(self, defaults=None, **kwargs):
        if defaults is None:
            defaults = {}
        defaults['owner'] = UserOwnedManager.owner
        return super(UserOwnedManager, self).update_or_create(owner=UserOwnedManager.owner, defaults=defaults, **kwargs)

class OwnedModel(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    objects = UserOwnedManager()
    class Meta:
        abstract = True
        default_manager_name = 'objects'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    faecher = models.ManyToManyField("notenrechner.Fach")

def restricted_to_owner(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        owned_models = OwnedModel.__subclasses__()
        for cls in owned_models:
            cls.objects.__class__.owner = request.user
        result = view_func(request, *args, **kwargs)
        for cls in owned_models:
            cls.objects.user = None
        return result
    return _wrapped_view
