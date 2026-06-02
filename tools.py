import os
import boto3
import requests
import json
from datetime import datetime
from ast import literal_eval

now = datetime.now()


def check_environment(bucket_request):
    try:
        environment = os.environ['ENV_NAME']  # "https://www.jobassistant.com"
        admin = os.environ['superuser']
        password = os.environ['superuserpass']
        if environment == 'Local':
            try:
                env_url = 'http://127.0.0.1:8000'
                local_aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
                local_aws_secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]
                session = boto3.Session(
                    aws_access_key_id=local_aws_access_key_id,
                    aws_secret_access_key=local_aws_secret_key,
                )
                s3 = session.resource('s3', region_name='us-west-2')
                if bucket_request == 'cover-letter-edit':
                    bucket = s3.Bucket('YOUR_S3_BUCKET')
                elif bucket_request == 'dashboard':
                    bucket = s3.Bucket('YOUR_S3_BUCKET')
                elif bucket_request == 'chat':
                    bucket = s3.Bucket('YOUR_S3_BUCKET')
                return env_url, admin, password, bucket
            except Exception as e:
                print(e)
                print(e.args)
                print(
                    'please set up local environments: "AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY". These are used to '
                    'access s3 buckets from your local environment.')
                pass
        elif environment == 'Staging':
            env_url = 'https://www.jobassistant.com'
            s3 = boto3.resource('s3', region_name='us-west-2')
            if bucket_request == 'cover-letter-edit':
                bucket = s3.Bucket('YOUR_S3_BUCKET')
            if bucket_request == 'cover-letter-edit':
                bucket = s3.Bucket('YOUR_S3_BUCKET')
            elif bucket_request == 'dashboard':
                bucket = s3.Bucket('YOUR_S3_BUCKET')
            elif bucket_request == 'chat':
                bucket = s3.Bucket('YOUR_S3_BUCKET')
            return env_url, admin, password, bucket
        elif environment == 'Production':
            env_url = 'https://wwww.jobassistant.com'
            s3 = boto3.resource('s3', region_name='us-west-2')
            if bucket_request == 'cover-letter-edit':
                bucket = s3.Bucket('YOUR_S3_BUCKET')
            elif bucket_request == 'dashboard':
                bucket = s3.Bucket('YOUR_S3_BUCKET')
            elif bucket_request == 'chat':
                bucket = s3.Bucket('YOUR_S3_BUCKET')
            return env_url, admin, password, bucket
    except Exception as e:
        print(e)
        print(e.args)
        print('Please set up environment variables: "ENV_NAME","superuser" and "superuserpass"')
        pass


def get_token(admin, password, environment):
    payload = {'username': admin, 'password': password}
    print(password)
    token_url = environment + "/resume/api-token-auth/"
    print(token_url)
    r = requests.post(token_url, data=payload)
    token = r.text
    token = literal_eval(token)
    token = token["token"]
    headers = {'Authorization': 'Token ' + token}
    return headers


def store_data_s3(data, data_type, sender_id, file_name, env_url):
    s3 = boto3.resource('s3', region_name='us-west-2')
    if data_type == 'company':
        __file_name = data + '_' + sender_id + '.json'
        object = {
            'company': data,
            'timestamp': now.strftime("%d/%m/%Y %H:%M:%S"),
            'sender_id': sender_id
        }
        if env_url == 'https://www.jobassistant.com':
            s3object = s3.Object('jobassistant-entity-companies', __file_name)
        else:
            s3object = s3.Object('jobassistant-entity-companies-staging', __file_name)
    elif data_type == 'job':
        __file_name = data + '_' + sender_id + '.json'
        object = {
            'job_title': data,
            'timestamp': now.strftime("%d/%m/%Y %H:%M:%S"),
            'sender_id': sender_id
        }
        if env_url == 'https://www.jobassistant.com':
            s3object = s3.Object('jobassistant-entity-jobs', __file_name)
        else:
            s3object = s3.Object('jobassistant-entity-jobs-staging', __file_name)
    else:
        object = data
        if env_url == 'https://www.jobassistant.com':
            s3object = s3.Object('YOUR_S3_BUCKET', file_name)
        else:
            s3object = s3.Object('YOUR_S3_BUCKET', file_name)
    try:
        s3object.put(
            Body=(bytes(json.dumps(object).encode('UTF-8')))
        )
        return 'success'
    except Exception as e:
        print(e)
        print(e.args)


def fetch_data_from_s3_file(s3_file):
    try:
        data = s3_file.get()['Body'].read().decode('utf-8')
        return data
    except Exception as e:
        print(e)
        print(e.args)
        print('Please check S3 settings')
        pass


def get_resume_api_endpoints(environment, django_user_id):
    resume_personal_url = environment + "/resume/personal-api/" + django_user_id + "/"
    resume_experience_url = environment + "/resume/experience-api/" + django_user_id + "/"
    resume_education_url = environment + "/resume/education-api/" + django_user_id + "/"
    resume_reference_url = environment + "/resume/reference-api/" + django_user_id + "/"
    urls = {
        'resume_personal_url': resume_personal_url,
        'resume_experience_url': resume_experience_url ,
        'resume_education_url': resume_education_url,
        'resume_reference_url': resume_reference_url
    }
    print(urls['resume_personal_url'])
    return urls


def get_rasa_core_urls(environment, sender_uuid_with_django_user_id, sender_uuid):

    if environment == 'https://www.jobassistant.com':
        rasa_core_url = "http://YOUR_HOST:5005" + '/webhooks/rest/webhook'
        rasa_core_tracker_url = 'http://YOUR_HOST:5005/conversations/' \
                                + sender_uuid_with_django_user_id + '/tracker'
        non_auth_rasa_core_tracker_url = 'http://YOUR_HOST:5005/conversations/' + \
                                         sender_uuid + "None" + "/tracker"
    elif environment == 'https://staging.jobassistant.com':  # TODO: Create staging version of rasa core
        rasa_core_url = "http://YOUR_HOST:5005" + '/webhooks/rest/webhook'
        rasa_core_tracker_url = "http://YOUR_HOST:5005" + sender_uuid_with_django_user_id + "/tracker"
        non_auth_rasa_core_tracker_url = "http://YOUR_HOST:5005" + sender_uuid + "None" + "/tracker"
    elif environment == 'http://127.0.0.1:8000':
        rasa_core_url = "http://127.0.0.1:5005" + '/webhooks/rest/webhook'
        rasa_core_tracker_url = "http://127.0.0.1:5005/conversations/" + sender_uuid_with_django_user_id + "/tracker"
        non_auth_rasa_core_tracker_url = "http://127.0.0.1:5005/conversations/" + sender_uuid + "None" + "/tracker"

    return rasa_core_url, rasa_core_tracker_url, non_auth_rasa_core_tracker_url
