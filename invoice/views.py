from django.shortcuts import render, redirect
from django.core.mail import send_mail
from datetime import date
from .models import Invoice
from django.db.models import Sum

def invoice_form(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        amount = request.POST.get("amount")

        today = date.today()

        count = Invoice.objects.filter(
            created_at__date=today
        ).count() + 1

        invoice_number = (
            f"INV-{today.strftime('%Y%m%d')}-{count:03d}"
        )

        invoice = Invoice.objects.create(
            invoice_number=invoice_number,
            customer_name=name,
            customer_email=email,
            amount=amount
        )

        return render(
            request,
            "invoice/result.html",
            {
                "invoice_id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "date": invoice.created_at.strftime("%d %B %Y"),
                "time": invoice.created_at.strftime("%I:%M %p"),
                "name": invoice.customer_name,
                "amount": invoice.amount,
                "invoice_status": invoice.status,
            }
        )

    return render(request, "invoice/form.html")


from django.core.mail import send_mail
from django.shortcuts import redirect
from .models import Invoice

def send_invoice(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)

    send_mail(
        subject=f"Invoice {invoice.invoice_number}",
        message=(
            f"Hello {invoice.customer_name},\n\n"
            f"Invoice No: {invoice.invoice_number}\n"
            f"Date: {invoice.created_at.strftime('%d %B %Y %I:%M %p')}\n"
            f"Amount: ₹{invoice.amount}\n\n"
            f"Thank you!"
        ),
        from_email=None,
        recipient_list=[invoice.customer_email],
    )

    return redirect("/")


def mark_paid(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    invoice.status = "PAID"
    invoice.save()
    return redirect("/")
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Invoice


def download_invoice(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="invoice_{invoice.invoice_number}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    p.drawString(100, 800, f"Invoice No: {invoice.invoice_number}")
    p.drawString(100, 780, f"Customer: {invoice.customer_name}")
    p.drawString(100, 760, f"Email: {invoice.customer_email}")
    p.drawString(100, 740, f"Amount: ₹{invoice.amount}")
    p.drawString(100, 720, f"Date: {invoice.created_at.strftime('%d %B %Y')}")

    p.showPage()
    p.save()

    return response
from .models import Invoice

def invoice_list(request):
    invoices = Invoice.objects.order_by("-created_at")
    return render(request, "invoice/list.html", {
        "invoices": invoices
    })

from django.shortcuts import get_object_or_404

def mark_paid(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    invoice.status = "PAID"
    invoice.save()
    return redirect("/invoices/")
from django.db.models import Sum

def dashboard(request):
    total_invoices = Invoice.objects.count()

    total_revenue = Invoice.objects.aggregate(
        total=Sum("amount")
    )["total"] or 0

    paid_revenue = Invoice.objects.filter(
        status="PAID"
    ).aggregate(total=Sum("amount"))["total"] or 0

    unpaid_revenue = Invoice.objects.filter(
        status="UNPAID"
    ).aggregate(total=Sum("amount"))["total"] or 0

    paid_count = Invoice.objects.filter(status="PAID").count()
    unpaid_count = Invoice.objects.filter(status="UNPAID").count()

    return render(request, "invoice/dashboard.html", {
        "total_invoices": total_invoices,
        "total_revenue": total_revenue,
        "paid_revenue": paid_revenue,
        "unpaid_revenue": unpaid_revenue,
        "paid_count": paid_count,
        "unpaid_count": unpaid_count,
    })
