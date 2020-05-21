from django.urls import path
from results_viewer.views import get_paths

urlpatterns = [
    path('results/<str:uid>/paths/', get_paths),
]