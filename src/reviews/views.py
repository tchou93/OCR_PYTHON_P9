from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError

from reviews.forms import ReviewForm, TicketForm
from reviews.models import Ticket, Review
from itertools import chain

from django.db.models import CharField, Value

from users.models import UserFollow


@login_required
def create_review_solo(request):
    if request.method == 'POST':
        r_form = ReviewForm(request.POST)
        t_form = TicketForm(request.POST, request.FILES)
        if r_form.is_valid() and t_form.is_valid():
            new_ticket = Ticket.objects.create(title=request.POST['title'],
                                               description=request.POST['description'],
                                               user=request.user,
                                               image=request.FILES['image'])
            new_review = Review.objects.create(ticket=new_ticket,
                                               rating=request.POST['rating'],
                                               user=request.user,
                                               headline=request.POST['headline'],
                                               body=request.POST['body'])
            messages.success(request, 'La revue a été crée.')
            return redirect('flux')
    else:
        r_form = ReviewForm()
        t_form = TicketForm()

    return render(request, 'reviews/create_review_solo.html', {'r_form': r_form,
                                                               't_form': t_form
                                                               })


@login_required
def create_review(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    target = "review"
    if request.method == 'POST':
        r_form = ReviewForm(request.POST)
        if r_form.is_valid():
            new_review = Review.objects.create(ticket=ticket,
                                               rating=request.POST['rating'],
                                               user=request.user,
                                               headline=request.POST['headline'],
                                               body=request.POST['body'])
            messages.success(request, 'La revue a été crée.')
            return redirect('flux')
    else:
        r_form = ReviewForm()

    return render(request, 'reviews/create_review.html', {'r_form': r_form,
                                                          'post': ticket,
                                                          'target': target
                                                          })


@login_required
def update_ticket(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    if request.method == 'POST':
        t_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if t_form.is_valid():
            t_form.save()
            messages.success(request, 'Le ticket a été mis à jour.')
            return redirect('posts')
    else:
        t_form = TicketForm(instance=ticket)

    return render(request, 'reviews/update_ticket.html', {'t_form': t_form})


@login_required
def create_ticket(request):
    if request.method == 'POST':
        t_form = TicketForm(request.POST, request.FILES)
        if t_form.is_valid():
            try:
                image = request.FILES['image']
            except MultiValueDictKeyError:
                image = None

            new_ticket = Ticket.objects.create(title=request.POST['title'],
                                               description=request.POST['description'],
                                               user=request.user,
                                               image=image)
            messages.success(request, 'Le ticket a été crée.')
            return redirect('flux')
    else:
        t_form = TicketForm()

    return render(request, 'reviews/create_ticket.html', {'t_form': t_form})


@login_required
def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, id=pk)
    ticket.delete()
    messages.success(request, 'Le ticket a été supprimé.')
    return redirect('posts')


@login_required
def update_review(request, pk):
    review = get_object_or_404(Review, id=pk)
    ticket = review.ticket
    if request.method == 'POST':
        r_form = ReviewForm(request.POST, instance=review)
        if r_form.is_valid():
            r_form.save()
            messages.success(request, 'La revue a été mis à jour.')
            return redirect('posts')
    else:
        r_form = ReviewForm(instance=review)

    return render(request, 'reviews/update_review.html', {'r_form': r_form,
                                                          'ticket': ticket})


@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, id=pk)
    review.delete()
    return redirect('posts')


def func_followed_users(user):
    return [userfollow.followed_user for userfollow in UserFollow.objects.filter(user=user)]


def get_users_viewable_reviews(user):
    followed_users = func_followed_users(user)

    review_answered_ticket_user_ids = []
    for ticket in Ticket.objects.filter(user=user):
        for review in Review.objects.all():
            if review.ticket == ticket:
                review_answered_ticket_user_ids.append(review.id)

    followed_users_reviews_ids = \
        [followed_user_review.id for followed_user_review in Review.objects.filter(user__in=followed_users)]
    followed_user_reviews_ids = \
        [user_review.id for user_review in Review.objects.filter(user=user)]
    reviews = Review.objects.filter(
        id__in=followed_users_reviews_ids + followed_user_reviews_ids + review_answered_ticket_user_ids)
    return reviews


def get_users_viewable_tickets(user):
    followed_users = func_followed_users(user)

    followed_users_tickets_ids = \
        [followed_user_ticket.id for followed_user_ticket in Ticket.objects.filter(user__in=followed_users)]
    followed_user_tickets_ids = \
        [user_ticket.id for user_ticket in Ticket.objects.filter(user=user)]
    tickets = Ticket.objects.filter(id__in=followed_users_tickets_ids + followed_user_tickets_ids)
    return tickets


@login_required
def posts(request):
    user_all_tickets = Ticket.objects.filter(user=request.user)
    user_all_reviews = Review.objects.filter(user=request.user)
    target = "Posts"

    return render(request, 'reviews/posts.html', {'user_all_tickets': user_all_tickets,
                                                  'user_all_reviews': user_all_reviews,
                                                  'target': target
                                                  })


def flux(request):
    if not request.user.is_authenticated:
        return redirect('login')
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request.user)

    user_all_reviews = Review.objects.filter(user=request.user)
    ticket_already_answered = [user_review.ticket_id for user_review in user_all_reviews]
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))

    # combine and sort the two types of posts
    all_posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    target = "Flux"
    return render(request, 'reviews/flux.html', context={'all_posts': all_posts,
                                                         'target': target,
                                                         'ticket_already_answered': ticket_already_answered
                                                         })
