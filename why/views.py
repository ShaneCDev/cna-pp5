from django.shortcuts import render


def why_us(request):
    """Why us page"""

    return render(request, 'why/why_us.html')
