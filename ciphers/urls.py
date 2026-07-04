from django.urls import path

from . import views

app_name = "ciphers"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("rail-fence/", views.rail_fence_view, name="rail_fence"),
    path("rsa/", views.rsa_view, name="rsa"),
]
