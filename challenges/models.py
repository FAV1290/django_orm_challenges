import decimal
import datetime
from django.db import models

from challenges.enums import SubmssionStatus, LaptopManufacturer


class Book(models.Model):
    title = models.CharField(max_length=256)
    author_full_name = models.CharField(max_length=256)
    isbn = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.title


class Laptop(models.Model):
    manufacturer = models.CharField(max_length=64, choices=LaptopManufacturer.choices)
    model = models.CharField(max_length=128)
    ram_gb = models.PositiveSmallIntegerField()
    storage_type = models.CharField(max_length=8, choices=[('hdd', 'HDD'), ('ssd', 'SSD')])
    storage_gb = models.PositiveSmallIntegerField()
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_json(self) -> dict[str, int | str | datetime.datetime | decimal.Decimal]:
        return {
            'id': self.pk,
            'manufacturer': self.get_manufacturer_display(),
            'model': self.model,
            'ram_gb': self.ram_gb,
            'storage_type': self.storage_type,
            'storage_gb': self.storage_gb,
            'price_usd': self.price_usd,
            'in stock': self.in_stock,
        }


class Submission(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    author = models.CharField(max_length=64)
    status = models.PositiveSmallIntegerField(choices=SubmssionStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField()
    category = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        choices=[
            ('php', 'PHP'),
            ('c++', 'C++'),
            ('javascript', 'JavaScript'),
        ],
    )

    def to_json(self) -> dict[str, int | str | datetime.datetime]:
        return {
            'title': self.title,
            'body': self.body,
            'author': self.author,
            'status': self.get_status_display(),
            'published_at': self.published_at,
            'category': self.get_category_display(),
        }


class LatestSubmission(Submission):
    class Meta():
        ordering = ['-published_at']
        proxy = True
