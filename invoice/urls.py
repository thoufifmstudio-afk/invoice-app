from django.urls import path
from .views import (
    invoice_form,
    invoice_list,
    send_invoice,
    download_invoice,
    mark_paid,
    dashboard,
)

urlpatterns = [
    path("", invoice_form, name="invoice_form"),
    path("invoices/", invoice_list, name="invoice_list"),
    path("send/<int:invoice_id>/", send_invoice, name="send_invoice"),
    path("download/<int:invoice_id>/", download_invoice, name="download_invoice"),
    path("paid/<int:invoice_id>/", mark_paid, name="mark_paid"),
    path("dashboard/", dashboard, name="dashboard"),
]
