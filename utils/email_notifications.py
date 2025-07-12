from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_search_results_email(to_email, results, subscription):
    subject = f"Результати пошуку для комбінації {subscription.digits or 'без комбінації'}"

    text_content = render_to_string('autonumbers/email_results.txt', {
        'results': results,
        'subscription': subscription,
    })

    html_content = render_to_string('autonumbers/email_results.html', {
        'results': results,
        'subscription': subscription,
    })

    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_subscription_confirmation_email(to_email, subscription):
    subject = "🔔 Ви підписалися на пошук номерів"

    text_content = render_to_string('autonumbers/email_subscription.txt', {
        'subscription': subscription,
    })

    html_content = render_to_string('autonumbers/email_subscription.html', {
        'subscription': subscription,
    })

    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.conf import settings
#
# def send_search_results_email(to_email, results, subscription):
#     subject = f"Результати пошуку для комбінації {subscription.digits or 'без комбінації'}"
#
#     # text версия
#     text_content = render_to_string('autonumbers/email_results.txt', {
#         'results': results,
#         'subscription': subscription,
#     })
#
#     # HTML-версия
#     html_content = render_to_string('autonumbers/email_results.html', {
#         'results': results,
#         'subscription': subscription,
#     })
#
#     msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [to_email])
#     msg.attach_alternative(html_content, "text/html")  # HTML-представлення
#     msg.send()

# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.conf import settings
#
# def send_search_results_email(to_email, results, subscription):
#     subject = f"Результати пошуку для комбінації {subscription.digits}"
#     message = render_to_string('autonumbers/email_results.txt', {
#         'results': results,
#         'subscription': subscription,
#     })
#
#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [to_email],
#         fail_silently=False,
#     )