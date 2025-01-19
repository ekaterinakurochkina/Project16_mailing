from django.views.generic.edit import DeleteView, CreateView, UpdateView
from django.views.generic import ListView, DetailView
from .forms import SendingForm, SendingModeratorForm
from .models import MailingRecipient, Message, Sending, MailingAttempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from mailing.servies import get_object_from_cache


class SendingCreateView(LoginRequiredMixin, CreateView):
    model = Sending
    form_class = SendingForm
    fields = ["name", 'recipient', 'message']
    template_name = "sending_form.html"
    success_url = reverse_lazy("mailing:sending_list")

    def form_valid(self, form):
        sending = form.save()
        user = self.request.user
        sending.owner = user
        sending.save()
        return super().form_valid(form)


class SendingListView(LoginRequiredMixin, ListView):
    model = Sending
    template_name = "sending_list.html"
    context_object_name = "sendings"

    def get_queryset(self):
        user = self.request.user
        if user.has_perm("mailing.can_canceled_sending"):
            return get_object_from_cache()      # подключаем к представлению функцию обращения к кешу
        else:
            return Sending.objects.filter(owner=user)

class SendingDetailView(LoginRequiredMixin, DetailView):
    model = Sending
#     надо дописать!

class SendingUpdateView(LoginRequiredMixin, UpdateView):
    model = Sending
    form_class = SendingForm
    template_name = "sending_form.html"

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return SendingForm
        if user.has_perm("mailing.can_canceled_sending"):
            return SendingModeratorForm
        raise PermissionDenied

    def get_success_url(self):
        return reverse_lazy('mailing:sending_detail', kwargs={'pk': self.object.pk})


class SendingDeleteView(LoginRequiredMixin, DeleteView):
    model = Sending
    template_name = "sending_confirm_delete.html"
    success_url = reverse_lazy("mailing:sending_list")


class SendingServiceView(LoginRequiredMixin, ListView):
    model = Sending
    # template_name = 'product_list_from_category.html'
    # context_object_name = 'products_category'
    #
    # def get_queryset(self):
    #     category_id = self.kwargs.get('pk')
    #     return get_product_category(category_id=category_id)


class AttemptListView(LoginRequiredMixin, ListView):
    template_name = "mailing_service/attempts.html"
    context_object_name = "attempt_list"

    def get_queryset(self):
        # Получаем только попытки рассылок, принадлежащих пользователю
        return MailingAttempt.objects.filter(mailing__created_by=self.request.user)

# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'catalog/product_detail.html'
#     context_object_name = 'product'
#
#     # def get_object(self, queryset=None):     # функция, которая показывает карточку товара только его владельцу
#     #     self.object = super().get_object(queryset)
#     #     if self.queryset == self.object.owner:
#     #         self.object.save()
#     #         return self.object
#     #     raise PermissionDenied
#
#
# class ProductCreateView(LoginRequiredMixin, CreateView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'catalog/product_create.html'
#     success_url = reverse_lazy('catalog:product_list')
#
#     def form_valid(self, form):
#         product = form.save()
#         user = self.request.user
#         product.owner = user
#         product.save()
#         return super().form_valid(form)
#
#
# class ProductUpdateView(LoginRequiredMixin, UpdateView):
#     model = Product
#     form_class = ProductForm
#     template_name = 'catalog/product_form.html'
#
#     def get_form_class(self):
#         user = self.request.user
#         if user == self.object.owner:
#             return ProductForm
#         if user.has_perm("catalog.can_unpublish_product"):
#             return ProductModeratorForm
#         raise PermissionDenied
#
#     def get_success_url(self):
#         return reverse_lazy('catalog:product_detail', kwargs={'pk': self.object.pk})
#
#
# class ProductDeleteView(LoginRequiredMixin, DeleteView):
#     model = Product
#     template_name = 'catalog/product_confirm_delete.html'
#     success_url = reverse_lazy('catalog:product_list')
#
#
# class ProductServiceView(LoginRequiredMixin, ListView):
#     model = Category
#     template_name = 'catalog/product_list_from_category.html'
#     context_object_name = 'products_category'
#
#     def get_queryset(self):
#         category_id = self.kwargs.get('pk')
#         return get_product_category(category_id=category_id)

