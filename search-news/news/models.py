from django.db import models

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    description = models.TextField()
    pub_date = models.CharField(max_length=200, blank=True)
    is_bookmarked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
