
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator, MaxValueValidator


class Bin(models.Model):
    Bin_Id = models.AutoField(primary_key=True)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    bin_content = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(150)],
        default=0.0
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_sent = models.BooleanField(default=False)  # Track email notification status

    def save(self, *args, **kwargs):
        if self.bin_content > 120:
            self.bin_content = 0.0
        super().save(*args, **kwargs)

@receiver(post_save, sender=Bin)
def send_email_on_bin_content(sender, instance, created, **kwargs):
    if created:
        # Newly created instance, no need to check for email_sent flag
        return

    if instance.bin_content >= 80 and not instance.email_sent:
        # Send email notification if bin_content reaches 80 and email has not been sent
        subject = 'Bin Content Alert'
        message = (
            f'Bin {instance.Bin_Id} has reached a content level of {instance.bin_content}.\n'
            f'Latitude: {instance.latitude}\n'
            f'Longitude: {instance.longitude}'
        )
        recipient_list = [instance.user.email]
        send_mail(subject, message, None, recipient_list)

        # Mark email_sent as True to indicate email has been sent
        instance.email_sent = True
        instance.save()

    if instance.bin_content == 0 and instance.email_sent:
        # Reset email_sent flag if bin_content drops back to 0
        instance.email_sent = False
        instance.save()
