from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.
GENDER_CHOICES = (("MALE", "male"),
                  ("FEMALE", "female"))


class Country(models.Model):
  name = models.CharField(max_length=100, null=True)

  def __str__(self) -> str:
      return self.name


class City(models.Model):
  country = models.ForeignKey(Country, on_delete=models.CASCADE)
  name = models.CharField(max_length=100, null=True)

  def __str__(self) -> str:
      return self.name


class MyAccountManager(BaseUserManager):
    def create_user(self, email, 
                    name=None,
                    password=None,
                    gender=None,
                    age=None,
                    country=None,
                    city=None
                    ):
        if not email:
            raise ValueError('Users must have an email address')

        try:
          splitted_name = name.split(" ")
          first_name = splitted_name[0]
          last_name = " ".join(splitted_name[1: ])
        except:
          first_name = None
          last_name = None

        user = self.model(
            email=self.normalize_email(email),
            username=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            name=name,
            gender=gender,
            age=age,
            country=country,
            city=city
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.is_active=True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

class Users(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True, blank=True, null=True, default=None)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    username= models.CharField(max_length=30,unique=True, blank=True, null=True)
    gender= models.CharField(max_length=30, blank=True, null=True, choices=GENDER_CHOICES, default='MALE')
    age = models.IntegerField(null=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = MyAccountManager()

    class Meta:
        db_table = "tbl_users"

    def __str__(self):
        return str(self.email)


    def has_perm(self, perm, obj=None): return self.is_superuser

    def has_module_perms(self, app_label): return self.is_superuser

    def tokens(self):
      refresh = RefreshToken.for_user(self)
      return {
          'refresh': str(refresh),
          'access': str(refresh.access_token)
      }