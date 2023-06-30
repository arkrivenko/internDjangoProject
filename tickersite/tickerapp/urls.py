from django.urls import path
from .views import RequestCreateView

app_name = "tickerapp"

urlpatterns = [
    path("", RequestCreateView.as_view(), name="mp4maker"),
]
