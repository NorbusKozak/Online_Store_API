import smtplib
import os
from email.message import EmailMessage

def send_activation_email(user_email: str, user_name: str):

    sender_email = os.getenv("EMAIL_SENDER")
    sender_password = os.getenv("EMAIL_PASSWORD")

    if not sender_email or not sender_password:
        print("Error of mail login.")
        return None

    msg = EmailMessage()
    msg.set_content(f"Hello {user_name}, welcome to the ShopAPI Family!\n\nWe are very thrilled to have you there.\nIf you have any questions don't hesitate to ask us on this email! \n\n ShopAPI Team.")
    msg['Subject'] = f"Welcome {user_name} :D"
    msg['From'] = sender_email
    msg['To'] = user_email

    try:
        with smtplib.SMTP('smtp.gmail.com', port=587) as server:
            server.ehlo()
            server.starttls()
            server.login(user=sender_email, password=sender_password)
            server.send_message(msg=msg)
            print(f"Succesfully send welcome email to {user_name}")
    except Exception as e:
        print(f"Error: {e}")