"""
В этом задании вам предстоит работать с моделью ноутбука. У него есть бренд (один из нескольких вариантов),
год выпуска, количество оперативной памяти, объём жесткого диска, цена, количество этих ноутбуков на складе
и дата добавления.

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
  (я бы советовал использовать для этого shell)
- реализовать у модели метод to_json, который будет преобразовывать объект ноутбука в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from django.http import (
    HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseForbidden, JsonResponse)

from challenges.models import Laptop
from challenges.enums import LaptopManufacturer


def laptop_details_view(request: HttpRequest, laptop_id: int) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание ноутбука по его id.
    Если такого id нет, вернуть 404.
    """
    try:
        return JsonResponse(Laptop.objects.get(id=laptop_id).to_json())
    except Laptop.DoesNotExist:
        return HttpResponseNotFound()


def laptop_in_stock_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание всех ноутбуков, которых на складе больше нуля.
    Отсортируйте ноутбуки по дате добавления, сначала самый новый.
    """
    laptops_in_stock_query = Laptop.objects.filter(in_stock__gt=0).order_by('-created_at')
    laptops_in_stock = list(map(lambda x: x.to_json(), laptops_in_stock_query))
    return JsonResponse({'laptops': laptops_in_stock})


def laptop_filter_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть список ноутбуков с указанным брендом и указанной минимальной ценой.
    Бренд и цену возьмите из get-параметров с названиями brand и min_price.
    Если бренд не входит в список доступных у вас на сайте или если цена отрицательная, верните 403.
    Отсортируйте ноутбуки по цене, сначала самый дешевый.
    """
    target_brand, target_min_price = request.GET.get('brand'), request.GET.get('min_price')
    manufactorers_choices_keys = [choice.value for choice in LaptopManufacturer]
    if any([
        target_brand is None or target_brand.lower() not in manufactorers_choices_keys,
        target_min_price is None or not target_min_price.isdigit(),
    ]):
        return HttpResponseForbidden()
    else:
        laptops_query = Laptop.objects.filter(
            manufacturer=target_brand,
            price_usd__gte=target_min_price,
        ).order_by('-price_usd')
        return JsonResponse({'laptops': list(map(lambda x: x.to_json(),  laptops_query))})


def last_laptop_details_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание последнего созданного ноутбука.
    Если ноутбуков нет вообще, вернуть 404.
    """
    try:
        return JsonResponse(Laptop.objects.latest('created_at').to_json())
    except Laptop.DoesNotExist:
        return HttpResponseNotFound()
