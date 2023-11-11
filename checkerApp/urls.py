from django.urls import path
from . import views as checker_views

urlpatterns = [
    path('visited_links', checker_views.LinksView.as_view(), name='init_links'),
    path('visited_domains', checker_views.DomainsView.as_view(), name='get_domains')
]
