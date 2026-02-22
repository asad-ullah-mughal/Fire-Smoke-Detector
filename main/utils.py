from django.core.mail import send_mail

def send_fire_alert_email():
    subject = "🔥 Fire/Smoke Detection Alert"
    message = "Fire or smoke has been detected by the live camera system. Please take immediate action!"
    from_email = "your_email@gmail.com"
    recipient_list = ["recipient_email@gmail.com"]  # you can add multiple emails here

    send_mail(subject, message, from_email, recipient_list)
