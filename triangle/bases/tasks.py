from django.core.mail import EmailMessage

__all__ = ["send_mail"]


def send_mail(title, text, emails):
    mail = EmailMessage(title, text, to=emails)
    mail.send()
