from django.urls import path, include

from .views import Query

urlpatterns = [
    path('query/', Query.as_view()),
]
