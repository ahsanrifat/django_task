from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .custom_permission import IsAdminOrUser
from rest_framework.response import Response
from django.db.models.signals import post_save, pre_save
from .serializers import UserCreateSerializer, CustomTokenObtainPairSerializer
from rest_framework import status

# from django.core.exceptions import PermissionDenied
from .models import User
import ipdb

# Create your views here.


def get_unauthorised_response_json():
    return {"success": False, "message": "Unauthorised Content"}


def get_exception_response_json(e):
    return {"success": False, "message": str(e)}


class CreateNewUser(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        try:
            # request.data = json.dumps(request.data)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            user_data = serializer.data
            del user_data["password"]
            headers = self.get_success_headers(serializer.data)
            response = Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
            # response = super().create(request, *args, **kwargs)
            if response.status_code == 201:
                return Response(
                    {
                        "success": True,
                        "message": "User Created Successfully",
                        "user_data": user_data,
                    }
                )
            else:
                return Response({"success": False, "message": response.message})
        except Exception as e:
            return Response(get_exception_response_json(e))


class UploadProfilePicture(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAdminOrUser]

    def post(self, request, *args, **kwargs):
        try:
            user_obj = User.objects.get(id=kwargs.get("pk"))
            profile_picture = request.data["profile_picture"]
            if profile_picture.name.split(".")[-1] in ("png", "jpg", "jpeg"):
                profile_picture.name = (
                    str(kwargs.get("pk"))
                    + str(user_obj.start_date)
                    + "_profile_picture."
                    + profile_picture.name.split(".")[-1]
                )
                user_obj.profile_picture = profile_picture
                user_obj.save()
                return Response(
                    {
                        "success": True,
                        "message": "Profile Picture Uploaded Successfully",
                        "profile_picture_path": user_obj.profile_picture.url,
                    }
                )
            else:
                return Response(
                    {
                        "success": False,
                        "message": "Invalid file format",
                        "accepted_formats": "png, jpeg, jpg",
                        "given_format": profile_picture.name.split(".")[-1],
                    }
                )
        except Exception as e:
            return Response(get_exception_response_json(e), 400)


class GetUpdateDeleteUser(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            user_data = serializer.data
            del user_data["password"]
            return Response({"success": True, "user_data": user_data})
        except Exception as e:
            return Response(get_exception_response_json(e), 400)

    def delete(self, request, *args, **kwargs):
        #
        try:
            # if it's a admin's token
            if request.user.is_superuser:
                response = super().delete(request, *args, **kwargs)
                if response.status_code == 204:
                    return Response({"success": True, "message": "Deleted User"})
                return response
            else:
                return Response(
                    {"success": False, "message": "Only an Admin can delete an user"},
                    401,
                )
        except Exception as e:
            print("Exception in delete user-->", e)
            return Response(get_exception_response_json(e), 400)

    def patch(self, request, *args, **kwargs):
        try:
            # password changing mechanism
            if "password" in request.data:
                instance = self.get_object()
                instance.set_password(request.data["password"])
                return Response(
                    {"success": True, "message": "Password Changed Successfully"}
                )
            elif "password" not in request.data:
                response = super().patch(request, *args, **kwargs)
                return Response({"success": True, "message": "Data updated partially"})
        except Exception as e:
            print("Exception in patch user-->", e)
            return Response(get_exception_response_json(e), 400)

    def put(self, request, *args, **kwargs):
        return Response({"success": False, "message": "PUT not allowed"}, 400)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
