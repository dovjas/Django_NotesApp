from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Note(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    note_title = models.CharField(max_length=150)
    note_description = models.TextField(null=True,blank=True)
    note_complete = models.BooleanField(default=False)
    note_created = models.DateTimeField(auto_now_add=True)
    note_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.note_title

    class Meta:
        ordering = ['note_complete']