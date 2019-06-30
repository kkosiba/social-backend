from django.urls import include, path
from .views import CustomUserRetrieveUpdate


urlpatterns = [
    path(
        "user/", CustomUserRetrieveUpdate.as_view(), name="custom-user-retrieve-update"
    ),
    path("", include("rest_auth.urls")),
    path("register/", include("rest_auth.registration.urls")),
]
