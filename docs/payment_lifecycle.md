# Payment Lifecycle

### CREATED

The default status assigned when a `Payment` object is created.

The payment exists in the Payment API, but the payment processing has not started yet.

---

### PROCESSING

The status assigned after the user has entered the required payment details and initiated the payment by clicking the **Pay** button.

The payment is currently being processed by the payment provider.

---

### SUCCEEDED

The status assigned after the payment has been successfully completed. 

The payment amount has been successfully processed.

---

### FAILED

The status assigned when the payment cannot be completed because of a technical problem.

Examples:
- Network error.
- Payment provider API error.
- Internal server error.

---

### DECLINED

The status assigned when the payment is explicitly rejected by the bank or payment provider.

Examples:
- Insufficient funds.
- Expired card.
- Invalid card.
- Bank declined the payment.

---

### CANCELLED

The status assigned when the payment is explicitly cancelled before it has been successfully processed.

For example:
- The user clicks the **Cancel** button.
- The payment provider reports that the payment was cancelled.

---

### EXPIRED

The status assigned when the payment is not completed within the allowed time period.

For example:
- The payment remains in the `CREATED` state for longer than the configured expiration time.

---

### REFUNDED

The status assigned after a successfully completed payment has been fully refunded.

A payment can only be refunded if its current status is `SUCCEEDED`.



## Allowed Status Transitions

### CREATED

Can transition to:
- PROCESSING
- CANCELLED
- EXPIRED

### PROCESSING

Can transition to:
- SUCCEEDED
- FAILED
- DECLINED

### SUCCEEDED

Can transition to:
- REFUNDED

### FAILED

This is a terminal status.

No further transitions are allowed.

---

### DECLINED

This is a terminal status.

No further transitions are allowed.

---

### CANCELLED

This is a terminal status.

No further transitions are allowed.

---

### EXPIRED

This is a terminal status.

No further transitions are allowed.

---

### REFUNDED

This is a terminal status.

No further transitions are allowed.

---

# Retry Policy

Terminal payment states cannot transition back to a previous state.

If a payment attempt fails, is declined, cancelled, or expired, the original `Payment` object remains unchanged.

If the user wants to attempt the payment again, a new `Payment` object must be created.

This allows the system to preserve the complete payment history.