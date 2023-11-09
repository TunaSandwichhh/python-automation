from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

class Notification:
    def __init__(self, account_sid, auth_token, from_number):
        self.client = Client(account_sid, auth_token)
        self.from_number = from_number

    def send_sms(self, to_number, message):
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            print(f"Message sent: {message.sid}")
            return True, message.sid  # successful
        except TwilioRestException as e:
            print(f"Twilio Error: {e}")
            return False, None  # error