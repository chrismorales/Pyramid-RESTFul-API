from pyramid_mailer.message import Message
from pyramid_mailer import get_mailer


class Emailer():
    """
        This class will handle sending emails base off of where the user
        is coming from.
    """
    def __init__(self, recipient, request):
        """ Instantiate the get_mailer function """
        self.recipient = recipient
        self.request = request

    def send_message(self):
        """ Sends message base of URL """
        # Query DB for appropriate message and parameters to whom to send to
        TITLE = "Congratulations! Welcome to Fashion Designer!"
        MESSAGE = "Please click on the link in order to activate your account!"
        SENDER = "nogareru@gmail.com"
        mailer = get_mailer(self.request)
        try:
            message = Message(subject=TITLE,
                              sender=SENDER,
                              recipients=[self.recipient],
                              body=MESSAGE)
        except:
            raise 'Sending mail error!'
        mailer.send_immediately(message, fail_silently=False)
        return "Mail Sent!"

    def send_password_reset_link(self, hash_link_key):
        # generate a link with a timestamp
        # send the link to user
        mailer = get_mailer(self.request)
        try:
            message = Message(
                subject=TITLE,
                sender=SENDER,
                recipients=[self.recipient],
                body=MESSAGE)
        except:
            raise 'Sending password reset link error'
        mailer.send_immediately(message, fail_silently=False)
        return "Reset Link Sent"