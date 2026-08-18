from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from employees.views import EmployeeViewSet

router = DefaultRouter()
router.register("employees", EmployeeViewSet, basename="employees-api")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    # JWT + регистрация (Djoser, K5)
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    # API (ДЗ 6)
    path("api/v1/", include(router.urls)),
    # Документация Swagger (ДЗ 7, K1)
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    # Публичные страницы — ВНЕ DEBUG (критический фикс аудита)
    path("", include("employees.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
