from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    user_type_data = ((1, "Inspector"), (2, "Buyer"), (3, "Seller"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class Inspector(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100)
    objects = models.Manager()

class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    aadhar_number = models.CharField(max_length=16, blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    objects = models.Manager()

class Buyer(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    aadhar_number = models.CharField(max_length=16, blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    address = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    objects = models.Manager()

class Land(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    land_price = models.DecimalField(max_digits=10, decimal_places=2)
    property_pid = models.CharField(max_length=100)
    physical_survey_number = models.CharField(max_length=100)
    image = models.ImageField(upload_to='land_images/')
    documents = models.FileField(upload_to='land_documents/')

class Approval(models.Model):
    land = models.ForeignKey(Land, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE)
    objects = models.Manager()

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Inspector.objects.create(admin=instance)
        if instance.user_type == 2:
            Buyer.objects.create(admin=instance)
        if instance.user_type == 3:
            Seller.objects.create(admin=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.inspector.save()
    if instance.user_type == 2:
        instance.buyer.save()
    if instance.user_type == 3:
        instance.seller.save()
