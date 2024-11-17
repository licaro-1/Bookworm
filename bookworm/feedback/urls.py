from django.urls import path

from feedback import views

app_name = "feedback"

urlpatterns = [
    path("create/", views.feedback_create, name="feedback_create"),
    path("<uuid:uuid>/", views.feedback_created, name="feedback_created")
]
