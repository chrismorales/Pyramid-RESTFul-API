from pyramid_mailer import get_mailer
from pyramid_mailer.message import Message


class Emailer(object):
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
        self.email_sender = get_mailer(self.request)
        message = Message(subject="",
                          sender="nogareru@gmail.com",
                          recipients=["lambda.designs.cm@gmail.com"],
                          body="Testing pyramid application")
        message.send_immediately(message, fail_silently=False)
        return "Mail Sent To User!"
