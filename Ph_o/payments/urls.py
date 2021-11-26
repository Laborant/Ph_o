from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from payments import views


urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('order/', views.ApproveInvoice.as_view(), name='order'),
]
