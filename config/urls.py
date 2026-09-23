from django.contrib import admin
from django.urls import path, include

from apps.payments.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('apps.payments.urls')),
    path('api/v1/', include('apps.users.urls')),

    path('', demo_checkout, name='demo-checkout'),
    path('payment-success/', payment_success, name='payment-success'),
]
