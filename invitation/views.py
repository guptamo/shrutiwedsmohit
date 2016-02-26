from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
def login_redirect(request):
    if request.user.is_staff:
        return redirect(reverse("invitation:dashboard"))
    else:
        return redirect(reverse("invitation:invitation"))


@login_required
def invitation(request):
    return render(request, "invitation/invitation.html")


@login_required
@user_passes_test(
    lambda u: u.is_staff,
    login_url=reverse_lazy("invitation:invitation"),
    redirect_field_name="")
def dashboard(request):
    return render(request, "invitation/dashboard.html")
