from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

@login_required
def login_redirect(request):
    if request.user.is_staff:
        return redirect(reverse("invitation:dashboard"))
    else:
        return redirect(
            reverse("invitation:invitation",
            args=[request.user.username]))
