from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from rest_framework_api_key.models import AbstractAPIKey


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):

    """ Class designed to create users. """

    username = models.CharField('username', max_length=30, blank=True)
    email = models.EmailField('Adresse mail', unique=True)
    first_name = models.CharField('Prénom', max_length=30, blank=True)
    last_name = models.CharField('Nom', max_length=30, blank=True)
    date_joined = models.DateTimeField('date joined', auto_now_add=True, null=True, blank=True)
    avatar = models.FileField('Avatar', blank=True)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_superuser = models.BooleanField(default=False)
    credits = models.IntegerField('Crédits', default=0)



    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'



    def get_full_name(self) -> str:
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self) -> str:
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs) -> None:
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, *args, **kwargs) -> None:
        if not self.first_name:
            self.first_name = 'John'
        if not self.last_name:
            self.last_name = 'Doe'

        super(User, self).save(*args, **kwargs)



class StripeCustomer(models.Model):
    """Class designed to create Stripe customers."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_status = models.BooleanField(default=False)
    subscription_beginning_date = models.DateTimeField(blank=True, null=True)
    subscription_ending_date = models.DateTimeField(blank=True, null=True)
    subscription_cancelled_date = models.DateTimeField(blank=True, null=True)
    subscription_cancelled = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Stripe Customer'
        verbose_name_plural = 'Stripe Customers'

    def __str__(self):
        return str(self.user.email)


class Plans(models.Model):
    """Class designed to create plans."""
    name = models.CharField(max_length=255, blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    stripe_plan_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'

    def __str__(self):
        return str(self.name)



class UserAPIKey(AbstractAPIKey):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='api_keys')