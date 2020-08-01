from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Note(models.Model):
    # title of the Note
    title = models.CharField(max_length=70, blank=False)
    # User who created the Note
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    # Description for the Note
    description = models.TextField()
    # Time when the note is created
    time_created = models.DateTimeField(default=timezone.localtime().now)

    def __str__(self):
        """
        String representation of the Note Object
        format - <title> | <time_created>
        """

        return f"{self.title} | {self.time_created}"