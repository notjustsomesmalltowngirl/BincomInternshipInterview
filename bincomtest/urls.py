from . import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polling-unit/<int:uniqueid>/', views.polling_unit_results, name='polling_unit_results'),
    path("", views.home, name="home"),
    path("lga-results/", views.lga_results, name="lga_results"),
    path("create-results/", views.create_results, name="create_results")
]
