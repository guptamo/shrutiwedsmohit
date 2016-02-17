from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse


def invitation(request):
    return render(request, "invitation/invitation.html")


def admin_redirect(request):
    if request.user.is_staff:
        return redirect(reverse("invitation:add_invitation"))
    else:
        return redirect(reverse("invitation:invitation"))


def add_invitation(request):
    return render(request, "invitation/add-invitation.html")
