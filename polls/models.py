from django.db import models
from django.utils import timezone
import datetime

class Question(models.Model):
    question_text = models.CharField(
        max_length=200, verbose_name='질문',
        help_text='질문을 션택하세요.'
    )
    pub_date = models.DateTimeField('생성날짜')
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE )
    choice_text = models.CharField(
        max_length=200,
        verbose_name='답변',
        help_text='답변을 입력하세요.'
    )
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text

