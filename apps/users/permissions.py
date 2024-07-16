from rest_framework.permissions import BasePermission


class IsCompany(BasePermission):
    """
    Allows access only to company users users.
    """

    def has_permission(self, request, _):
        user_type = (request.user.is_company or request.user.is_staff)
        return bool(request.user and user_type)


class IsCustomer(BasePermission):
    """
    Allows access only to customer users users.
    """

    def has_permission(self, request, _):
        user_type = (request.user.is_customer or request.user.is_staff)
        return bool(request.user and user_type)
