from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User as Invitation

@login_required
def login_redirect(request):
    if request.user.is_staff:
        return redirect(reverse("invitation:dashboard"))
    else:
        return redirect(reverse(
            "invitation:invitation"))

@login_required
def invitation(request):
    return render(request, "invitation/invitation.html")

@login_required
def dashboard(request):
    if request.user.is_staff:
        return render(request, "invitation/dashboard.html")
    else:
        return redirect(reverse("invitation:invitation"))
