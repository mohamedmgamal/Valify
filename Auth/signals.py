from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CustomUser,Otp
@receiver(post_save,sender=CustomUser)
def Handler(sender,instance,created,*args,**kwargs):
    if created:
        Otp(user_id=instance.id).save()
        otp =Otp.objects.get(user_id=instance.id)
        print(otp.otp)
        send_mail("Welcome to Valify ", f'welcome {instance.name} to Valify , to active your account please use this OTP {otp.otp} ',
                 "valifytask@gmail.com", [instance.email,"ValifyTask@gmail.com" ], fail_silently=False)