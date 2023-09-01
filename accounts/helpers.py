import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
class SENDINBLUE_API:
    URL = "https://api.brevo.com/v3/"
    API_KEY = os.getenv("SENDINBLUE_API_KEY")
    HEADERS = {'Content-Type': 'application/json', 'api-key': API_KEY}


def send_mail_sendinblue(template_id: int, to: str, sender: str=os.getenv('EMAIL_HOST_USER'), bcc=None,
              reply_to=os.getenv('EMAIL_HOST_USER'), **kwargs):
    data = {'templateId': template_id,
            'sender': {'email': sender, 'name': 'Vincent'},
            'to': [{'email': to}],
            'replyTo': {'email': reply_to, 'name': 'Vincent'},
            'params': kwargs}

    if bcc:
        data['bcc'] = [{'email': bcc}]

    return requests.post(
        f"{SENDINBLUE_API.URL}/smtp/email",
        headers=SENDINBLUE_API.HEADERS,
        data=json.dumps(data),
    )