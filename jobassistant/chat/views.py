# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

import re
import html

from .botserver import BotServer
from tools import *


@ensure_csrf_cookie
def room(request, sender_uuid):

    # Check what environment code is running in
    env_url, admin, password, bucket = check_environment('chat')

    # Check for username
    # token = request.POST.get('token')

    # When user responds to bot
    message = request.POST.get('message')

    # When user signs up and continues chat
    chat_continue = request.POST.get('chat_continue')

    # When the user gets to the end of basic chat, collect chat history from tracker
    chat_basic_complete = request.POST.get('chat_basic_complete')

    # When the user gets to the end of full chat, collect chat history from tracker
    chat_full_complete = request.POST.get('chat_full_complete')

    # When user is authenticated and continues with chat after onbaording
    chat_continue_authenticated = request.POST.get('chat_continue_authenticated')

    # When the user completes basic and is already logged in
    # chat_basic_complete_with_login = request.POST.get('chat_basic_complete_with_login')

    headers = {'content-type': 'application/json'}

    user_id = request.user.id
    sender_uuid_with_django_user_id = str(sender_uuid) + str(user_id)

    def format_data(url):
        data_json = requests.get(url)
        data_formatted = str(data_json.text)
        data = json.loads(data_formatted)
        return data

    rasa_core_url, rasa_core_tracker_url, non_auth_rasa_core_tracker_url = get_rasa_core_urls(
        env_url, sender_uuid_with_django_user_id,
        sender_uuid
    )

    # Detect if user is signed in and check against sender uuid + 'None' to verify if the user is newly signed up
    if request.user.is_authenticated:
        # Use rasa tracker's user_auth slot url to determine user is signed in during the chat - can detect change
        data = format_data(non_auth_rasa_core_tracker_url)  # check if the user was a new user or not at start of chat
        check_data = data['slots'].get('user_auth')

        if check_data is None:  # Try 'None' to check if this logged in user was new in middle of chat
            print('user was logged before')
            bot = BotServer(rasa_core_url, headers, sender_uuid_with_django_user_id)
        elif data['slots']['user_auth'] is False:  # False == 'None' meaning the user was new before and has signed up
            print("User signed up, chatting for the first time")
            # Use the same tracker ('None', new user) url before the sign up
            rasa_core_tracker_url = non_auth_rasa_core_tracker_url
            sender_uuid_with_django_user_id = sender_uuid + 'None'
            # Send the bot message with sender uuid with 'None' appended - this indicates user wasn't signed on before
            bot = BotServer(rasa_core_url, headers, sender_uuid_with_django_user_id)
    else:
        print('new user started chat')
        bot = BotServer(rasa_core_url, headers, sender_uuid_with_django_user_id)

    if message:
        user = request.user.is_authenticated

        # Reformat text for Rasa to understand
        message = re.sub(u"[\u201d\u201c\u2019\u2026\u2022\u2010\u2605\u007C\u2018]", "'", message)
        message = re.sub(u"[\xa0]", " ", message)
        message = re.sub(u"\u0026", "and", message)
        message = re.sub(u'[\u002D\u2010\u2011\u2012\u2013\u2014\u2015\uFE63\uFE58\uFF0D]', '_hyphen_', message)
        message = re.sub('[\r\n]', '___', message)
        message = message.replace('"',"'")
        message = html.escape(message)

        response, questions_list_type = bot.send_message(message=message, user=user, rasa_core_tracker=rasa_core_tracker_url)
        if isinstance(response, list):
            return JsonResponse({'bot_response': response[0], 'bot_buttons': response[1], 'questions_list_type': questions_list_type, 'bot_instruction_for_skip': ""})
        else:
            return JsonResponse({'bot_response': response, 'questions_list_type': questions_list_type, 'bot_instruction_for_skip': ""})
    elif chat_continue:
        user = request.user.is_authenticated
        continue_message = '/inform_continue_authenticated'
        response, questions_list_type = bot.send_message(message=continue_message, user=user, rasa_core_tracker=rasa_core_tracker_url)
        print(response)
        if isinstance(response, list):
            print(questions_list_type)
            return JsonResponse({'bot_response': response[0], 'bot_buttons': response[1], 'questions_list_type': questions_list_type,  'bot_instruction_for_skip': ""})
        else:
            print(questions_list_type)
            return JsonResponse({'bot_response': response, 'questions_list_type': questions_list_type,  'bot_instruction_for_skip': ""})
    elif chat_continue_authenticated:
        user = request.user.is_authenticated
        continue_message = '/inform_continue'
        response, questions_list_type = bot.send_message(message=continue_message, user=user, rasa_core_tracker=rasa_core_tracker_url)
        print(response)
        if isinstance(response, list):
            print(questions_list_type)
            return JsonResponse(
                {'bot_response': response[0], 'bot_buttons': response[1], 'questions_list_type': questions_list_type, 'bot_instruction_for_skip': ""})
        else:
            print(questions_list_type)
            return JsonResponse({'bot_response': response, 'questions_list_type': questions_list_type, 'bot_instruction_for_skip': ""})
    elif chat_basic_complete:
        chat_tracker_data = requests.get(rasa_core_tracker_url)
        chat_data = str(chat_tracker_data.text)
        BotServer.store_chat_part_one_tracker_data(chat_tracker_data=chat_data, sender=sender_uuid_with_django_user_id, bucket=bucket, env_url=env_url)
        return JsonResponse({'response': 'success'})
    elif chat_full_complete:
        chat_tracker_data = requests.get(rasa_core_tracker_url)
        chat_data = str(chat_tracker_data.text)
        chat_obj = json.loads(chat_data)
        cover_letter_pdf_url = chat_obj['slots']['cover_letter_url']
        dashboard_link = env_url + "/dashboard/"
        user = request.user
        print(user)
        BotServer.store_chat_full_tracker_data(user=user, chat_tracker_data=chat_data, sender=sender_uuid_with_django_user_id, bucket=bucket, env_url=env_url)
        return JsonResponse({
            'response': 'success',
            'cover_letter_url': cover_letter_pdf_url,
            'dashboard_link': dashboard_link
        })
    else:
        # Bot starts chat when chat starts
        print('started messaging')
        chat_tracker_data = requests.get(rasa_core_tracker_url)
        chat_data = str(chat_tracker_data.text)
        # Pass in rasa core chat log to determine if the chat has already started.
        bot.initiate_chat(chat_data, env_url)

    return render(request, 'chat/room.html', {
        'sender_uuid': mark_safe(json.dumps(sender_uuid)),
    })


room_view = room
