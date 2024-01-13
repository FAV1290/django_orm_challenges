from django.contrib import admin

from challenges.models import Laptop, Submission


@admin.register(Laptop)
class LaptopAdmin(admin.ModelAdmin):
    pass


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    pass
