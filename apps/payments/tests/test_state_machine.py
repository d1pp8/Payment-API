import pytest
from apps.payments.models import Payment
from apps.payments.state_machine import PaymentStateMachine

Status = Payment.PaymentStatus

@pytest.mark.parametrize("source,target", [
    (Status.CREATED, Status.PROCESSING),

    (Status.PROCESSING, Status.SUCCEEDED),
    (Status.PROCESSING, Status.FAILED),
    (Status.PROCESSING, Status.CANCELLED),

    (Status.SUCCEEDED, Status.REFUND),
])

def test_allowed_transitions(source, target):
    payment = Payment(status=source)
    PaymentStateMachine(payment).apply(target)
    assert payment.status == target


@pytest.mark.parametrize("source,target", [
    (Status.CREATED, Status.SUCCEEDED),
    (Status.CREATED, Status.FAILED),
    (Status.CREATED, Status.CANCELLED),

    (Status.SUCCEEDED, Status.FAILED),
    (Status.SUCCEEDED, Status.PROCESSING),

    (Status.FAILED, Status.SUCCEEDED),
    (Status.FAILED, Status.PROCESSING),
    (Status.FAILED, Status.CANCELLED),

    (Status.CANCELLED, Status.SUCCEEDED),
    (Status.CANCELLED, Status.PROCESSING),
    (Status.CANCELLED, Status.FAILED),

    (Status.REFUND, Status.SUCCEEDED),
])

def test_forbidden_transitions(source, target):
    payment = Payment(status=source)
    with pytest.raises(ValueError):
        PaymentStateMachine(payment).apply(target)

