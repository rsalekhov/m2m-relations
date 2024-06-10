from django.db import models
from django.core.exceptions import ValidationError

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, through='Scope')

    def __str__(self):
        return self.title

class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    is_main = models.BooleanField(default=False)

    def clean(self):
        if self.is_main and Scope.objects.filter(article=self.article, is_main=True).exists():
            raise ValidationError('Only one main scope allowed per article.')

    def save(self, *args, **kwargs):
        if self.is_main:
            Scope.objects.filter(article=self.article, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)
