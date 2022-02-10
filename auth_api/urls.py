from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenBlacklistView,
)
from .views import (
    CreateNewUser,
    GetUpdateDeleteUser,
    CustomTokenObtainPairView,
    UploadProfilePicture,
)


urlpatterns = [
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/user/create/", CreateNewUser.as_view()),
    path("api/user/logout/", TokenBlacklistView.as_view()),
    path("api/user/<pk>/", GetUpdateDeleteUser.as_view()),
    path("api/upload/profile_picture/user/<pk>/", UploadProfilePicture.as_view()),
]
