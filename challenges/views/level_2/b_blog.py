"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
(опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
- реализовать у модели метод to_json, который будет преобразовывать объект книги в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from datetime import timedelta
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden

from challenges.enums import SubmssionStatus
from challenges.models import Submission, LatestSubmission


def last_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    last_posts_query = LatestSubmission.objects.filter(status=SubmssionStatus.PUBLISHED)[:3]
    last_posts = list(map(lambda x: x.to_json(), last_posts_query))
    return render(request, 'posts.html', context={'posts': last_posts})


def posts_search_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    search_query = request.GET.get('query')
    if search_query is None:
        return HttpResponseForbidden()
    search_results_query = LatestSubmission.objects.filter(
        Q(
            title__icontains=search_query
        ) | Q(
            body__icontains=search_query
        ) | Q(
            author__icontains=search_query
        ) | Q(
            category__icontains=search_query
        )
    )
    search_results = list(map(lambda x: x.to_json(), search_results_query))
    return render(request, 'posts.html', context={'posts': search_results})


def untagged_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    untagged_posts_query = Submission.objects.filter(
        category__isnull=True).order_by('author', 'published_at')
    untagged_posts = list(map(lambda x: x.to_json(), untagged_posts_query))
    return render(request, 'posts.html', context={'posts': untagged_posts})


def categories_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    target_categories_raw = request.GET.get('categories') or ''
    target_categories = target_categories_raw.lower().split(',')
    categories_posts_query = Submission.objects.filter(category__in=target_categories)
    categories_posts = list(map(lambda x: x.to_json(), categories_posts_query))
    return render(request, 'posts.html', context={'posts': categories_posts})


def last_days_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    target_delta_days_raw = request.GET.get('last_days')
    if target_delta_days_raw is None or not target_delta_days_raw.isdigit():
        return HttpResponseForbidden()
    min_date = timezone.now() - timedelta(days=int(target_delta_days_raw))
    last_days_posts_query = LatestSubmission.objects.filter(
        published_at__range=(min_date, timezone.now()))
    last_days_posts = list(map(lambda x: x.to_json(), last_days_posts_query))
    return render(request, 'posts.html', context={'posts': last_days_posts})
