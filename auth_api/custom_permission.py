from rest_framework.permissions import BasePermission


class IsAdminOrUser(BasePermission):
    message = "Not Authenticated"

    def has_permission(self, request, view):
        try:
            user_id = view.kwargs[view.lookup_field]
            if request.user.is_authenticated and (
                request.user.is_superuser or request.user.id == user_id
            ):
                return True
            return False
        except Exception as e:
            self.message = str(e)
            return False
