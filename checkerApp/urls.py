from django.urls import path
from . import views as checker_views
urlpatterns = [
    path('visited_links', checker_views.DomainsView.as_view(), name='get_history')
]