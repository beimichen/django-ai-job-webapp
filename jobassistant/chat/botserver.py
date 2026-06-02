from jobassistant.cover_letter.models import CoverLetter

from celery.result import AsyncResult
import re
from datetime import datetime
from tools import *
from .tasks import bot_chat_response

now = datetime.now()


class BotServer:
    def __init__(self, url, headers, sender_id):
        print('Bot initiated')
        self.url = url
        self.headers = headers
        self.sender_id = sender_id

    def initiate_chat(self, chat_tracker_data, env_url):

        start_chat_message = '{"sender": ', '"', self.sender_id, '"', ', "message":', '"', '/start', '"', '}'
        message = ''.join(start_chat_message)
        chat = json.loads(chat_tracker_data)
        chat['start_time'] = now.strftime("%d/%m/%Y %H:%M:%S")
        try:
            events_length = len(chat['events'])

            if events_length == 1:

                sender_id = self.sender_id
                bot_response = bot_chat_response.s(self.url, message, self.headers).apply_async()
                response = AsyncResult(bot_response.id)
                response = response.get(timeout=30)

                print('initiated chat')

                file_name = sender_id + '.json'
                data_type = 'chat'
                data = chat
                store_data_s3(data, data_type, sender_id, file_name, env_url)
                return response
            else:
                print('already started')
        except Exception as e:
            print(e)
            print(e.args)

    def send_message(self, message, user, rasa_core_tracker):

        message = message.encode('ascii', 'ignore')  # resolves the >128bit issue
        message = message.decode('utf-8')
        message = re.sub(r'(?<=[.,])(?=[^\s])', r' ', message)  # add space after commas

        if message == 'correct':
            message = '/inform_correct'
            message_formatted = '{"sender": ', '"', self.sender_id, '"', ', "message":', '"', message, '"', '}'
            # message_formatted = {
            #     'sender': self.sender_id,
            #     'message': message
            # }
        elif message == 'incorrect':
            message = '/inform_incorrect'
            message_formatted = '{"sender": ', '"', self.sender_id, '"', ', "message":', '"', message, '"', '}'
            # message_formatted = {
            #     'sender': self.sender_id,
            #     'message': message
            # }
        elif user is True and message == 'yes, let me personalize it':
            # user = '_logged_in'
            message = '/inform_continue'
            message_formatted = '{"sender": ', '"', self.sender_id, '"', ', "message":', '"', message, '"', '}'
            # message_formatted = {
            #     'sender': self.sender_id,
            #     'message': message
            # }
        elif user is False and message == 'yes, let me personalize it':
            # user = '_not_logged_in'
            message = '/inform_signup'
            message_formatted = '{"sender": ', '"', self.sender_id, '"', ', "message":', '"', message, '"', '}'
            # message_formatted = {
            #     'sender': self.sender_id,
            #     'message': message
            # }
        elif user is False and message == 'no, thank you':
            # user = '_not_logged_in'
            message = '/inform_discontinue'
            message_formatted = '{"sender": ', '"', self.sender_id, '"', ', "message":', '"', message, '"', '}'
            # message_formatted = {
            #     'sender': self.sender_id,
            #     'message': message
            # }
        elif user is True and message == 'no, thank you':
            message = '/inform_discontinue'
            message_formatted = '{"sender": ', '"', self.sender_id, '"', ', "message":', '"', message, '"', '}'
            # message_formatted = {
            #     'sender': self.sender_id,
            #     'message': message
            # }
        else:
            message_formatted = '{"sender": ', '"', self.sender_id, '"', ', "message":', '"', message, '"', '}'
            # message_formatted = {
            #     'sender': self.sender_id,
            #     'message': message
            # }

        str_message_formatted = ''.join(message_formatted)
        message_to_bot = str_message_formatted
        print(message_to_bot)

        # Bot response processing from celery task
        bot_response = bot_chat_response.s(self.url, message_to_bot, self.headers).apply_async()
        response = AsyncResult(bot_response.id)
        response = response.get(timeout=30)

        data = requests.get(rasa_core_tracker)
        chat = data.json()

        list_questions = chat['slots']['list_type_questions']  # last item in job question type slot from rasa

        if list_questions is not None:
            print(list_questions)
            return response, list_questions
        else:
            print('question_list_type is None')
            list_questions = "none yet"
            return response, list_questions

    @staticmethod
    def store_chat_part_one_tracker_data(sender, chat_tracker_data, bucket, env_url):

        # Chat history is compiled from browser and sent to this class function to process: call in view

        file_name = sender + '.json'
        s3_file = bucket.Object(file_name)
        chat_from_s3 = json.loads(fetch_data_from_s3_file(s3_file))  # chat recorded in s3
        chat_time_started = chat_from_s3['start_time']


        chat_from_rasa = json.loads(chat_tracker_data) # current chat
        chat_from_rasa['start_time'] = chat_time_started
        chat_from_rasa['basic_cover_letter_time'] = now.strftime("%d/%m/%Y %H:%M:%S")

        file_name = sender + '.json'
        data_type = 'chat'
        data = chat_from_rasa
        store_data_s3(data, data_type, sender, file_name, env_url)
        return 'success'

    @staticmethod
    def store_chat_full_tracker_data(user, chat_tracker_data, sender, bucket, env_url):

        # Chat history is compiled from browser and sent to this class function to process: call in view

        file_name = sender + '.json'
        s3_file = bucket.Object(file_name)
        chat_obj = fetch_data_from_s3_file(s3_file)
        chat_from_s3 = json.loads(chat_obj)  # chat recorded in s3
        chat_time_started = chat_from_s3['start_time']
        basic_cover_letter_time = chat_from_s3['basic_cover_letter_time']

        chat_from_rasa = json.loads(chat_tracker_data)
        chat_from_rasa['complete'] = 'True'
        full_cover_letter = chat_from_rasa['slots']['full_cover_letter']
        job = chat_from_rasa['slots']['job']
        company = chat_from_rasa['slots']['org']
        contact = chat_from_rasa['slots']['person']
        industry = chat_from_rasa['slots']['industry']
        cover_letter_pdf_url = chat_from_rasa['slots']['cover_letter_url']
        resume_pdf_url = chat_from_rasa['slots']['resume_url']
        sender_id = chat_from_rasa['slots']['sender_id']
        CoverLetter.objects.create_cover_letter(parent_user=user, text=full_cover_letter, form_id=sender_id, job=job,
                                                contact=contact, industry=industry, company=company,
                                                cover_letter_pdf_url=cover_letter_pdf_url, resume_pdf_url=resume_pdf_url
                                                )
        chat_from_rasa['chat_time_started'] = chat_time_started
        chat_from_rasa['basic_cover_letter_time'] = basic_cover_letter_time
        chat_from_rasa['full_coverletter_time'] = now.strftime("%d/%m/%Y %H:%M:%S")

        file_name = sender + '.json'
        data_type = 'chat'
        data = chat_from_rasa
        store_data_s3(data, data_type, sender, file_name, env_url)

        return 'success'

