from stripe import StripeClient
from django.conf import settings

from payments.models import Payment
from payments.state_machine import PaymentStateMachine


class PaymentsService:
    @staticmethod
    def create_payment_intent(payment: Payment):
        client=StripeClient(settings.STRIPE_SECRET_KEY)
        payment_intent = client.v1.payment_intents.create(
            {
                'amount': payment.amount,
                'currency': payment.currency,
                'metadata': {'order_id': payment.external_order_id}
            }
        )
        sm = PaymentStateMachine(payment)
        sm.apply(Payment.PaymentStatus.PROCESSING)

        payment.stripe_payment_intent_id = payment_intent.id
        payment.save()
        return payment_intent


    @staticmethod
    def cancel_payment_intent(payment: Payment):
        client = StripeClient(settings.STRIPE_SECRET_KEY)
        payment_intent = client.v1.payment_intents.cancel(payment.stripe_payment_intent_id)
        return payment_intent


    @staticmethod
    def refund_payment(payment: Payment):
        client = StripeClient(settings.STRIPE_SECRET_KEY)
        refund = client.v1.refunds.create({'payment_intent': payment.stripe_payment_intent_id, })
        return refund


    @staticmethod
    def change_status(payment_intent_id: str, event_type: str):
        payment = Payment.objects.filter(stripe_payment_intent_id=payment_intent_id).first()

        if payment is None:
            return None


        sm = PaymentStateMachine(payment)
        if not sm.handle_event(event_type=event_type):
            return None

        payment.save(update_fields=['status', 'updated_at'])
        return payment