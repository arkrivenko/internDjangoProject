from django.urls import path
from .views import RequestCreateView

app_name = "tickerapp"

urlpatterns = [
    path("create/", RequestCreateView.as_view(), name="mp4maker"),
]
