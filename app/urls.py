from django.conf.urls import url

from app.views import test_view

urlpatterns = [
    url(r'^test/', test_view),
]
