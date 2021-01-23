from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from accounts.models import GuestModel

User=settings.AUTH_USER_MODEL

# Create your models here.

class BillingProfileManager(models.Manager):
    def new_or_get(self,request):
        user=request.user
        guest_email_id=request.session.get('guest_email_id')
        billing_profile_created=False
        billing_profile=None
        if user.is_authenticated:
            billing_profile,billing_profile_created=self.model.objects.get_or_create(
                                                                user=user,email=user.email)
        elif guest_email_id is not None:
            guest_email_obj=GuestModel.objects.get(id=guest_email_id)
            billing_profile,guest_billing_profile_created=self.model.objects.get_or_create(email=guest_email_obj.email)
        else:
            pass
        return billing_profile,billing_profile_created


class BillingProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.DO_NOTHING,null=True,blank=True)
    email=models.EmailField()
    active=models.BooleanField(default=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    objects=BillingProfileManager()

    def __str__(self):
        return self.email

#def billing_profile_created_receiver(sender,instance,created,*args,**kwargs):
#    if created:
#        print("send to stripe/braintee")
#        instance.customer_id=

def user_created_receiver(sender,instance,created,*args,**kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance,email=instance.email)

post_save.connect(user_created_receiver,sender=User)
