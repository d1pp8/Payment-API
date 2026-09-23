from apps.payments.models import Payment

class PaymentStateMachine:
    transitions = {
        Payment.PaymentStatus.CREATED: frozenset({
            Payment.PaymentStatus.PROCESSING
        }),
        Payment.PaymentStatus.PROCESSING: frozenset({
            Payment.PaymentStatus.SUCCEEDED,
            Payment.PaymentStatus.FAILED,
            Payment.PaymentStatus.CANCELLED
        }),
        Payment.PaymentStatus.SUCCEEDED: frozenset({
            Payment.PaymentStatus.REFUND
        }),
        Payment.PaymentStatus.FAILED: set(),
        Payment.PaymentStatus.CANCELLED: set(),
        Payment.PaymentStatus.REFUND: set(),
    }

    events = {
        'payment_intent.succeeded': Payment.PaymentStatus.SUCCEEDED,
        'payment_intent.payment_failed': Payment.PaymentStatus.FAILED,
        'payment_intent.canceled': Payment.PaymentStatus.CANCELLED,
        'charge.refund.updated': Payment.PaymentStatus.REFUND,
    }

    def __init__(self, payment: Payment):
        self.payment = payment

    def handle_event(self, event_type: str) -> bool:
        target = self.events.get(event_type)
        if target is None:
            return False
        self.apply(target)
        return True

    def apply(self, target: str) -> None:
        if not self._can(target):
            raise ValueError(f'Invalid transition: {self.payment.status} -> {target}')
        self.payment.status = target

    def _can(self, target: str) -> bool:
        return target in self.transitions.get(self.payment.status, set())


