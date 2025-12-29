from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    title_tag = models.SlugField(max_length=120, blank=True, null=True, allow_unicode=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now) # () 없음.
    updated_at = models.DateTimeField(auto_now=True)
    
    category_choices = [
        ('General', '일반'),
        ('Hobby', '취미'),
        ('Music', '음악'),
        ('Movie', '영화'),
        ('Game', '게임'),
        ('coding', '코딩'),
        ('Politics', '정치'),
        ('Science', '과학'),
        ('Travel', '여행'),
        ('Food', '음식'),
        ('Sports', '스포츠'),
    ]
    category = models.CharField(max_length=50, blank=True, null=True, 
                                choices=category_choices,
                                default='General')

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.title} - {self.author.username}'
    
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        if not self.title_tag:
            self.title_tag = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_posted']