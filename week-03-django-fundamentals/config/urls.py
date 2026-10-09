
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("employees/", include("apps.employees.urls")),
    path("departments/", include("apps.departments.urls")),
    path("api/", include("apps.employees.api_urls")),
]
