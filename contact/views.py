from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.http import HttpResponse


def contact(request):
    """Contact us page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, [settings.DEFAULT_FROM_EMAIL])
                console_email = send_mail(subject, message, from_email, [settings.DEFAULT_FROM_EMAIL])
                print(console_email)
            except BadHeaderError:
                return HttpResponse("Invalid header.")
            return redirect('contact_success')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }

    return render(request, 'contact/contact.html', context)


def contact_success(request):
    return render(request, 'contact/contact_success.html')
