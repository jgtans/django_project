from rest_framework.permissions import SAFE_METHODS, BasePermission


class EmployeeRolePermission(BasePermission):
    """
    Права доступа (ДЗ 6, K6):
    - посетитель: только чтение;
    - смотритель (группа watchers): изменение (перемещение между столами);
    - администратор (is_staff или группа admins): всё, включая создание и удаление.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user.is_authenticated:
            return False
        if user.is_staff or user.groups.filter(name="admins").exists():
            return True
        if user.groups.filter(name="watchers").exists():
            return request.method in ("PUT", "PATCH")
        return False
