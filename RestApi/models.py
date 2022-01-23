from django.db import models

# Create your models here.
from Auth.models import CustomUser


class poll(models.Model):
    title=models.CharField(blank=False,null=False,max_length=64)
    description=models.TextField(blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    expiry_date =models.DateTimeField(null=False)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['created_at']


class Choices(models.Model):
    name=models.CharField(blank=False,null=False,max_length=64)
    poll=models.ForeignKey(poll, related_name='choices', on_delete=models.CASCADE)
    def __str__(self):
         return f"{self.poll.title}::{self.name} "

class Answers(models.Model):
    poll=models.ForeignKey(poll,on_delete=models.CASCADE)
    choice = models.ForeignKey(Choices, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    class Meta:
         unique_together = (("user", "poll",))
    def __str__(self):
        return f"{self.poll.title}  A:{self.choice.name} user:{self.user_id}"

class DiscussionThread(models.Model):
    poll = models.ForeignKey(poll, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment=models.TextField()
