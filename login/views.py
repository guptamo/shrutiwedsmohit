from django.shortcuts import redirect, render
from django.core.urlresolvers import reverse


def admin_redirect(request):
    if request.user.is_staff:
        return redirect(reverse("add_invitation"))
    else:
        return redirect(reverse("invitation:invitation"))


def add_invitation(request):
    return render(request, "login/add-invitation.html")
