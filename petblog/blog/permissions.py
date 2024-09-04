from rest_framework import permissions


from rest_framework import permissions

class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Дозвіл, який дозволяє редагувати або видаляти пост лише автору або адміністратору.
    """

    def has_object_permission(self, request, view, obj):
        # Дозволити перегляд всім користувачам
        if request.method in permissions.SAFE_METHODS:
            return True

        # Дозволити редагування і видалення тільки автору або адміністратору
        return request.user == obj.author or request.user.is_staff
