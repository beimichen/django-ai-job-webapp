from celery.decorators import task
from celery.utils.log import get_task_logger

# from redis import Redis
# from rq import Queue

import requests
import json
from django.http import HttpResponse


# q = Queue(connection=Redis())


@task(name="bot_chat_response")
def bot_chat_response(url, data, headers):
    try:
        r = requests.post(url, data=data, headers=headers)
        response = r.text
        response = json.loads(response)
        print(response)

        if 'buttons' in response[0]:
            bot_response = response[0].get('text')
            bot_buttons = response[0].get('buttons')
            print(bot_response)
            print(bot_buttons)
            return [bot_response, bot_buttons]
        else:
            bot_response = response[0].get("text")
            print(bot_response)
            return bot_response
    except:
        bot_response = "Something went wrong. Please start a new chat."
        return bot_response


