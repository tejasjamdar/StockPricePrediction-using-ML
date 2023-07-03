from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC7605f035a761d0f97cf1481be35d3b2e'
auth_token = 'fc13608cdfa71594c4d0111ed50ec0fb'
client = Client(account_sid, auth_token)

def sendSMS(sender,recipient,body):
    message = client.messages \
                    .create(
                        body=body,
                        from_=sender,
                        to=recipient
                    )

    print(message.sid)