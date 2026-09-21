from django.urls import path

from payments.views import (
    PaymentViewSet,
    stripe_webhook,
    demo_checkout,
    payment_success
)

app_name = 'payments'

urlpatterns = [

    path('payments/', PaymentViewSet.as_view({'get':'list', 'post': 'create'}), name='payments'),
    path('payments/<uuid:pk>/', PaymentViewSet.as_view({'get':'retrieve', }), name='payments-detail'),
    path('payments/<uuid:pk>/cancel/', PaymentViewSet.as_view({'post': 'cancel'}), name='payment-cancel'),
    path('payments/<uuid:pk>/refund/', PaymentViewSet.as_view({'post': 'refund'}), name='payment-refund'),

    path('webhooks/stripe/', stripe_webhook, name='stripe-webhook'),

    path('', demo_checkout, name='demo-checkout'),
    path('payment-success/', payment_success, name='payment-success'),
]