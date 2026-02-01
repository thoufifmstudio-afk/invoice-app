from django.db import models

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=50)
    customer_name = models.CharField(max_length=100)
    customer_email = models.EmailField()
    amount = models.IntegerField()

    status = models.CharField(
        max_length=20,
        default="UNPAID"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number
