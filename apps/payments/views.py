from django.http import HttpResponse

import stripe

from django.conf import settings

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404,render

from apps.payments.serializers import (
    PaymentSerializer,
    PaymentCreateSerializer,
    PaymentCreateResponseSerializer
)

from apps.payments.models import Payment
from apps.payments.services import PaymentsService

from django.views.decorators.csrf import csrf_exempt

from rest_framework import permissions



class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save()

        payment_intent = PaymentsService.create_payment_intent(payment)

        response_data = {
            'payment_id': payment.id,
            'external_order_id': payment.external_order_id,
            'amount': payment.amount,
            'currency': payment.currency,
            'client_secret': payment_intent.client_secret
        }

        response_serializer = PaymentCreateResponseSerializer(response_data)


        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


    def list(self, request):
        queryset = Payment.objects.all()
        serializer = PaymentSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Payment.objects.all()
        payment = get_object_or_404(queryset, pk=pk)
        serializer = PaymentSerializer(payment)

        return Response(serializer.data)

    def cancel(self, request, pk=None):
        payment = get_object_or_404(Payment, pk=pk)
        PaymentsService.cancel_payment_intent(payment)

        return Response({'detail': 'Payment cancellation requested'}, status=status.HTTP_200_OK)

    def refund(self, request, pk=None):
        payment = get_object_or_404(Payment, pk=pk)

        if payment.status != Payment.PaymentStatus.SUCCEEDED:
            return Response({'detail': 'Only succeeded payments can be refunded.'}, status=status.HTTP_400_BAD_REQUEST)
        payment_refund = PaymentsService.refund_payment(payment)
        return Response({'refund_id': payment_refund.id, 'status': payment_refund.status}, status=status.HTTP_200_OK)



def demo_checkout(request):
    return render(request, 'index.html')

def payment_success(request):
    return render(request, 'payment_success.html')







@csrf_exempt
def stripe_webhook(request):
    payload = request.body

    signature = request.META.get('HTTP_STRIPE_SIGNATURE')

    webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload,
            signature,
            webhook_secret
        )
    except ValueError:
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    event_type = event['type']
    event_object = event['data']['object']

    if event_type.startswith('payment_intent.'):
        payment_intent_id = event_object['id']

    elif event_type == 'charge.refund.updated':
        payment_intent_id  = event_object['payment_intent']

    else:
        return HttpResponse(status=200)

    PaymentsService.change_status(payment_intent_id, event_type)

    return HttpResponse(status=200)