from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth import logout, authenticate, login
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse

import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '[%(asctime)s] | %(name)-12s | %(levelname)-8s: %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
# Create your views here.


def index(request):
    context = {}
    return render(request, 'index.html', context)


def get_activation_key(username):
    """
    Generate the activation key which will be emailed to the user.
    """
    return signing.dumps(obj=username, salt=settings.REGISTRATION_SALT)


def page_not_found_404(request, exception):
    return render(request, "404.html")


def permission_error_403(request, exception):
    return render(request, "403.html")


def page_error_500(request):
    return render(request, "500.html")


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        next = request.POST.get('next', '/')
        if form.is_valid():
            user = form.save()
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                user.is_active = False
                user.save()
                logger.info(
                    f'Successfully added new user {user.username} - {user.email}')
                {%- if cookiecutter.email == 'y' %}
                try:
                    send_mail("Verify your email",
                              f"Thanks for signing up at Happiness - An Inside Job. Please click the link below to activate your account https://happiness-aninsidejob.com/activate/{get_activation_key(user.username)}",
                              from_email="connie@happiness-aninsidejob.com",
                              recipient_list=[user.email],
                              fail_silently=False)
                except:
                    logger.error(
                        f"Failed to send verification email to {user.username} - {user.email}")
                {%- endif %}
            messages.success(
                request, 'Thanks for registering! Please check your email to activate your account')
            response = HttpResponseRedirect(next)
            return response
        else:
            return render(request=request,
                          template_name="registration/signup.html",
                          context={"form": form, 'next': request.GET.get('next', '/')})
    else:
        form = SignUpForm()
        return render(request=request,
                      template_name="registration/signup.html",
                      context={"form": form, 'next': request.GET.get('next', '/')})


def activate_user_account(request, activation_key):
    """
    Verify that the activation key is valid and within the
    permitted activation time window, returning the username if
    valid or raising ``ActivationError`` if not.
    """
    logger.info(f"Trying to activate key: {activation_key}")
    try:
        username = signing.loads(
            activation_key,
            salt=settings.REGISTRATION_SALT,
            max_age=settings.ACCOUNT_ACTIVATION_DAYS * 86400
        )
        logger.info("Successfully verified activation")
        user = User.objects.get(username=username)
        logger.info(
            f"Setting user: '{user.username} - {user.first_name} {user.last_name}' status as active")
        user.is_active = True
        user.save()
        messages.success(request, 'Successfully activated user account')
    except signing.SignatureExpired:
        logger.warning('Signature expired')
        messages.warning(request, 'Failed to activate user account')
    except signing.BadSignature:
        logger.warning('Bad signature')
        messages.warning(request, 'Failed to activate user account')
    except Exception as e:
        logger.error(e)
        messages.warning(request, 'Failed to activate user account')
    return redirect('/')
