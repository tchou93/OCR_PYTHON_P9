from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, SubscriptionForm
from .models import UserFollow


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le compte a été crée.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            followed_user = User.objects.filter(username=request.POST['followed_user']).first()
            if request.user == followed_user:
                messages.error(request, "Impossible de souscrire avec soi même !")
            else:
                if followed_user is None:
                    messages.error(request, f"L'utilisateur {request.POST['followed_user']} n'existe pas")
                else:
                    (_, already_followed) = UserFollow.objects.get_or_create(user=request.user,
                                                                             followed_user=followed_user)
                    if not already_followed:
                        messages.error(request, f"Vous suivez déjà {followed_user}")
    else:
        form = SubscriptionForm()

    followed_users = [user.followed_user for user in UserFollow.objects.filter(user=request.user)]
    followed_bys = [followed_user.user for followed_user in UserFollow.objects.filter(followed_user=request.user)]

    return render(request, 'users/subcription.html', context={'form': form,
                                                              'followed_users': followed_users,
                                                              'followed_bys': followed_bys})


@login_required
def unsubscribe(request, pk):
    user = User.objects.get(id=pk)
    follow = UserFollow.objects.filter(user=request.user, followed_user=user)
    follow.delete()

    return redirect('subscription')
