from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("marketplace/", include(("marketplace.urls", "marketplace"), namespace="marketplace")),
    path("payments/", include(("payments.urls", "payments"), namespace="payments")),
    path(
        "",
        TemplateView.as_view(template_name="home.html"),
        name="home",
    ),
]

