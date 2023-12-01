from django.urls import path, include
from rest_framework import routers
from . import views

app_name = "feeds"

router = routers.SimpleRouter()
router.register(r"feeds", views.FeedViewSet)

urlpatterns = [path("/", include(router.urls))]
