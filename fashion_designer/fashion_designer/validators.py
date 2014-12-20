class Email(object):

    def __init__(self, email):
        self.email = email

    def validate_email(self):
        if '@' not in self.email or '.' not in self.email:
               return "Invalid Email"

