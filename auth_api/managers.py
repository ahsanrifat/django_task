from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Users must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user = user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user
