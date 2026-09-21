from django.db import models
import uuid

class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        CREATED = 'created', 'Created'
        PROCESSING = 'processing', 'Processing'
        SUCCEEDED = 'succeeded', 'Succeeded'
        FAILED = 'failed', 'Failed'
        CANCELLED = 'cancelled', 'Cancelled'
        REFUND = 'refund', 'Refund'


    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    merchant_id = models.UUIDField()
    external_order_id = models.CharField(max_length=255)
    amount = models.PositiveBigIntegerField()
    currency = models.CharField(max_length=3)

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.CREATED,
    )

    stripe_payment_intent_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at',]

    def __str__(self):
        return f'{self.id}: {self.merchant_id} -> {self.external_order_id}'
