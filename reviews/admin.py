from django.contrib import admin

from reviews.models import Review, Book, Publisher, BookContributor, Contributor

# Register your models here.

admin.site.register(Publisher)

admin.site.register(Book)

admin.site.register(Contributor)

admin.site.register(BookContributor)