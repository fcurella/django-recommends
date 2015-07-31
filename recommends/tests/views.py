# Create your views here.
from django.contrib.auth import authenticate, login as _login
from django.http import HttpResponseRedirect
from django.views.generic import DetailView

from .models import RecProduct


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            _login(request, user)
            # redirect to a success page.
        else:
            # Return a 'disabled account' error message
            pass
    else:
        pass
        # Return an 'invalid login' error message.
    return HttpResponseRedirect(request.POST.get('next', '/'))


class RecProductView(DetailView):
    model = RecProduct
