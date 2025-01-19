from django.core.cache import cache

from django.urls import path
from . import views
from django.contrib import admin
from mailing.apps import MailingConfig
from mailing.views import SendingCreateView, SendingDeleteView, SendingUpdateView,SendingListView, SendingDetailView, SendingServiceView
from .models import Sending
from django.conf import settings
from django.conf.urls.static import static
# app_name = 'catalog'
app_name = MailingConfig.name

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',SendingListView.as_view(), name='product_list'),
    # path('catalog/<int:pk>',cache_page(60)(ProductDetailView.as_view(), name='product_detail')),
    path('catalog/<int:pk>',ProductDetailView.as_view(), name='sending_detail'),
    path('catalog/new/',SendingCreateView.as_view(), name='sending_create'),
    path('catalog/<int:pk>/edit/',SendingUpdateView.as_view(), name='sending_edit'),
    path('catalog/<int:pk>/delete/',SendingDeleteView.as_view(), name='sending_delete'),
    path('catalog/<int:pk>/category',SendingServiceView.as_view(), name='sending_list_???'),
]