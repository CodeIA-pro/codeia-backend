from mailjet_rest import Client

def send_email(to, name, subject, HTMLPart):
    api_key = 'e6ac1f9b5118853737bb403b80d1cee3'
    api_secret = '6f1c08e6d0ea83d1af0603fa7a15040c'
    try:
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')
        data = {
            'Messages': [
                {
                "From": {
                    "Email": "support@codeia.pro",
                    "Name": "CodeIA"
                },
                "To": [
                    {
                    "Email": to,
                    "Name": name
                    }
                ],
                "Subject": subject,
                "TextPart": "",
                "HTMLPart": HTMLPart
                }
            ]
        }
        mailjet.send.create(data=data)
    except Exception as e:
        print(e)
        return False
    return True