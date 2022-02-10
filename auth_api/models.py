from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.utils import timezone
from django.db.models.signals import post_save, pre_save

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)
    username = None
    full_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=timezone.now)
    profile_picture = models.ImageField(
        null=True, blank=True, upload_to="profile_pictures/%Y"
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]
    objects = UserManager()

    class Meta:
        db_table = "custom_user"

    def __str__(self):
        return self.email + "_" + str(self.id)


def user_created_signal(sender, instance, **kwargs):
    print("User has been created-----")
    print(instance)


post_save.connect(user_created_signal, sender=User)
