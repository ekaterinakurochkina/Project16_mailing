from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import SendingCreateView, SendingDeleteView, SendingUpdateView,SendingListView, SendingDetailView, HomePageView

app_name = MailingConfig.name


urlpatterns = [
    path('',HomePageView.as_view(), name='home'),
    path('sending/list',SendingListView.as_view(), name='sending_list'),
    path('sending/<int:pk>',SendingDetailView.as_view(), name='sending_detail'),
    path('sending/new/',SendingCreateView.as_view(), name='sending_create'),
    path('sending/<int:pk>/edit/',SendingUpdateView.as_view(), name='sending_edit'),
    path('sending/<int:pk>/delete/',SendingDeleteView.as_view(), name='sending_delete'),

]