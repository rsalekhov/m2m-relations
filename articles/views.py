from django.shortcuts import render, get_object_or_404
from .models import Article

def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {
        'article': article,
    }
    return render(request, 'article_detail.html', context)
