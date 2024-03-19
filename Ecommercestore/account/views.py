from django.shortcuts import render, redirect
from .forms import CreateUserForm, loginform, UpdateUserForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

# import for our email Register class
from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate
from django.contrib.auth.models import User


# import for our email verification class
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# import for our login | logout class
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout


# import for our dashboard for security and dont let anyone access to our account
from django.contrib.auth.decorators import login_required

# import fo messages
from django.contrib import messages


# import for change password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


def register(request):

    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():

            user = form.save()

            user.is_active = False

            user.save()

            # Email verification setup (template)

            current_site = get_current_site(request)

            subject = 'Account verification email'

            message = render_to_string('account/registration/email-verification.html',
                                       {'user': user, 'domain': current_site.domain,
                                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                        'token': user_tokenizer_generate.make_token(user),
            })

            user.email_user(subject=subject, message=message)

            return redirect('email-verification-sent')

    context = {'form': form}

    return render(request, 'account/registration/register.html', context=context)


def email_verification(request, uidb64, token):

    unique_id = force_str(urlsafe_base64_decode(uidb64))

    user = User.objects.get(pk=unique_id)

    #success

    if user and user_tokenizer_generate.check_token(user, token):

        user.is_active = True

        user.save()

        return redirect('email-verification-success')

    #Failed

    else:

        return redirect('email-verification-failed')


def email_verification_sent(request):

    return render(request, 'account/registration/email-verification-sent.html')

def email_verification_success(request):

    return render(request, 'account/registration/email-verification-success.html')

def email_verification_failed(request):

    return render(request, 'account/registration/email-verification-failed.html')



def my_login(request):

    form = loginform()

    if request.method == 'POST':

        form = loginform(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect('dashboard')

    context = {'form':form}

    return render(request, 'account/my-login.html', context=context)



# Logout
def user_logout(request):

    try:

        for key in list(request.session.keys()):

            if key == 'session_key':

                continue

            else:

                del request.session[key]

    except KeyError:

        pass

    messages.success(request, 'Your Logout successfully')

    return redirect('store')



# Dashboard
@login_required(login_url='my-login')
def dashboard(request):

    return render(request, 'account/dashboard.html')




# profile managment view
@login_required(login_url='my-login')
def profile_management(request):

    # Updating our user's username and email address

    user_form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':

        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():

            user_form.save()

            messages.info(request, 'Account updated')

            return redirect('dashboard')

    context = {'user_form':user_form}

    return render(request, 'account/profile-management.html', context=context)


# delete account view
@login_required(login_url='my-login')
def delete_account(request):

    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':

        user.delete()

        messages.error(request, 'Account deleted')

        return redirect('store')

    return render(request, 'account/delete-account.html')


#shipping address view
@login_required(login_url='my-login')
def manage_shipping(request):

    try:

        # Account user with shipment information

        shipping = ShippingAddress.objects.get(user=request.user.id)

    except ShippingAddress.DoesNotExist:

        # Account user with no shipment information

        shipping = None

    form = ShippingForm(instance=shipping)

    if request.method == 'POST':

        form = ShippingForm(request.POST, instance=shipping)

        if form.is_valid():

            # Assign the user FK on the object

            shipping_user = form.save(commit=False)

            # Adding the FK itself
            shipping_user.user = request.user

            shipping_user.save()

            return redirect('dashboard')

    context = {'form':form}

    return render(request, 'account/manage-shipping.html', context=context)

@login_required(login_url='my-login')
def track_orders(request):

    return render(request, 'account/track-orders.html')



@login_required(login_url='my-login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'account/change-password.html', {
        'form': form
    })