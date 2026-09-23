from django.db import models
from django.conf import settings
from apps.common.models import UUIDModel


class Payment(UUIDModel):
    class PaymentStatus(models.TextChoices):
        CREATED = 'created', 'Created'
        PROCESSING = 'processing', 'Processing'
        SUCCEEDED = 'succeeded', 'Succeeded'
        FAILED = 'failed', 'Failed'
        CANCELLED = 'cancelled', 'Cancelled'
        REFUND = 'refund', 'Refund'

    merchant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
    )
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
        return f'{self.uuid}: {self.merchant} -> {self.external_order_id}'
