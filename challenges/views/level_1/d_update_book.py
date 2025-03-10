"""
В этом задании вам нужно реализовать функцию update_book, которая обновляет в БД данные книги с указанным id.
Функция должна сохранять в БД новые значения и возвращать экземпляр книги с уже обновлёнными данными.
Не забудьте обработать случай несуществующего id, тогда функция должна возврать None.

Чтобы проверить, работает ли ваш код, запустите runserver и сделайте POST-запрос
на 127.0.0.1:8000/book/<id книги>/update/.
После обновления книги попробуйте получить описание книги и убедитесь, что вы видите новые значения.
"""
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse

from challenges.models import Book


def update_book(book_id: int, new_title: str, new_author_full_name: str, new_isbn: str) -> Book | None:
    try:
        target_book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return None

    target_book.title = new_title
    target_book.author_full_name = new_author_full_name
    target_book.isbn = new_isbn
    target_book.save()

    return target_book


def update_book_handler(request: HttpRequest, book_id: int) -> HttpResponse:
    title = request.POST.get("title")
    author_full_name = request.POST.get("author_full_name")
    isbn = request.POST.get("isbn")
    if not all([title, author_full_name, isbn]):
        return HttpResponseBadRequest("One of required parameters are missing")

    assert title and author_full_name and isbn
    book = update_book(book_id, title, author_full_name, isbn)

    if book is None:
        return HttpResponseBadRequest()

    return JsonResponse({
        "id": book.pk,
        "title": book.title,
        "author_full_name": book.author_full_name,
        "isbn": book.isbn,
    })
