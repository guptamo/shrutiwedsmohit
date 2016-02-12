from django.shortcuts import render


def invitation(request):
    return render(request, "invitation/invitation.html")
