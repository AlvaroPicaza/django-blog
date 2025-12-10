from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # Para la fecha podriamos usar models.DateTimeField(auto_now_add=True), que recupera la fecha en la que se creo el post, pero no se podria modificar
    date_posted = models.DateTimeField(default=timezone.localtime)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})