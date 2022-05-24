import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
# account_sid='AC98b3f8f8743972146b1f706fcdd4cf63'
# auth_token='b90dea7feb9ffe3311c2ea87d3313ca6'
# client = Client(account_sid, auth_token)
# message = client.messages.create(
#          body='This is the ship that made the Kessel Run in fourteen parsecs?',
#          from_='+18507905695',
#          to='+84967903498'
#      )
# message = client.messages.create(
#          body='This is the ship that made the Kessel Run in fourteen parsecs?',
#          from_='+18507905695',
#          to='+84967903498'
#      )
# message = client.messages \
#     .create(
#          body='This is the ship that made the Kessel Run in fourteen parsecs?',
#          from_='+18507905695',
#          to='+84386201456'
#      )

# print(message.body)