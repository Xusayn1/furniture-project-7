from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    SAFE methods: allow for everyone.
    Write methods: allow if admin or object owner.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_staff:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_staff:
            return True
        owner = getattr(obj, "author", None)
        return owner == request.user


class IsPremiumUser(BasePermission):
    """
    Allow access only to premium users.
    """

    message = "This feature requires a Premium account."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        profile = getattr(user, "profile", None)
        return bool(profile and profile.is_premium)
