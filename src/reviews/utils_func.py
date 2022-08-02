from reviews.models import Ticket, Review
from users.models import UserFollow


def get_users_viewable_reviews(user):
    followed_users = [userfollow.followed_user for userfollow in UserFollow.objects.filter(user=user)]

    review_answered_ticket_user_ids = []
    for ticket in Ticket.objects.filter(user__in=followed_users + [user]):
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
    followed_users = [userfollow.followed_user for userfollow in UserFollow.objects.filter(user=user)]

    followed_users_tickets_ids = \
        [followed_user_ticket.id for followed_user_ticket in Ticket.objects.filter(user__in=followed_users)]
    followed_user_tickets_ids = \
        [user_ticket.id for user_ticket in Ticket.objects.filter(user=user)]
    tickets = Ticket.objects.filter(id__in=followed_users_tickets_ids + followed_user_tickets_ids)
    return tickets
