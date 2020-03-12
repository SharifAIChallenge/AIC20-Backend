import datetime
import random
import string
from typing import List

import requests

import coreapi
from django.conf import settings
from django.db.models import FileField
from django.db.models.fields.files import FieldFile

from apps.challenge.models import Game, Map


def random_token():
    chars = string.ascii_letters + string.digits
    return ''.join((random.choice(chars)) for i in range(15))


def create_infra_client():
    credentials = {'Authorization': 'Token {}'.format(settings.INFRA_AUTH_TOKEN)}
    print(credentials)
    transports = [coreapi.transports.HTTPTransport(credentials=credentials)]
    client = coreapi.Client(transports=transports)
    schema = client.get(settings.INFRA_API_SCHEMA_ADDRESS)
    return client, schema


def read_in_chunks(file: FieldFile, chunk_size=65536):
    while True:
        data = file.read(chunk_size)
        if not data:
            break
        yield data


def upload1(file):
    index = 0
    headers = {}
    print("=======================================")
    for chunk in read_in_chunks(file=file):
        offset = index + len(chunk)
        headers['Content-Type'] = 'application/octet-stream'
        headers['Content-length'] = file.size
        headers['Content-Range'] = 'bytes %s-%s/%s' % (index, offset, file.size)
        headers['Authorization'] = f'Token {settings.INFRA_AUTH_TOKEN}'
        index = offset
        try:
            r = requests.put(settings.INFRA_IP + "/api/storage/new_file/", data=chunk, headers=headers)
            print("r: %s, Content-Range: %s" % (r, headers['Content-Range']))
            print(r)
        except Exception as e:
            print(e)
    print("==========================================")


def upload2(file):
    from requests_toolbelt import MultipartEncoder
    import requests

    payload = MultipartEncoder({'file': file})

    r = requests.put(
        settings.INFRA_IP + "/api/storage/new_file/",
        data=payload,
        headers={"Content-Type": payload.content_type, 'Authorization': f'Token {settings.INFRA_AUTH_TOKEN}'})

    print(r.json())


def upload_file(file):
    """
    This function uploads a file to infrastructure synchronously
    :param file: File field from TeamSubmission model
    :return: file token or raises error with error message
    """
    print("ommad upload kone", file.size)
    response = requests.put(settings.INFRA_IP + "/api/storage/new_file/", files={'file': file},
                            headers={'Authorization': f'Token {settings.INFRA_AUTH_TOKEN}'})
    print(response.status_code, response.json(), "==== Upload File ====")

    return response.json()['token']


def upload_file_with_url(file):
    """
    This function uploads a file to infrastructure synchronously
    Site will be as server and infrastructure will download it 
    with the url came from site
    
    :param file: File field from TeamSubmission model
    :return: file token or raises error with error message
    """
    print("ommad upload kone", file.size)
    response = requests.post(settings.INFRA_IP + "/api/storage/new_file_from_url/",
                             json={'url': 'https://aichallenge.sharif.edu' + file.url},
                             headers={'Authorization': f'Token {settings.INFRA_AUTH_TOKEN}'})
    print(response.status_code, response.json(), "==== Upload File ====")

    return response.json()['token']


def download_file(file_token):
    """
    Downloads file from infrastructure synchronously
    :param file_token: the file token obtained already from infra.
    :return: sth that TeamSubmission file field can be assigned to
    """
    response = requests.get(settings.INFRA_IP + f"/api/storage/get_file/{file_token}/", allow_redirects=True,
                            headers={'Authorization': f'Token {settings.INFRA_AUTH_TOKEN}'})
    print(response.status_code, "==== Download File ====")
    return response


def compile_submissions(submissions):
    """
        Tell the infrastructure to compile a list of submissions
    :return: list of dictionaries each have token, success[, errors] keys
    """

    print("oomad compile kone")
    parameters = list()
    for submission in submissions:
        parameters.append({
            "game": 'AI2020',
            "operation": "compile",
            "parameters": {
                "language": submission.language,
                "code_zip": submission.infra_token
            }
        })
    response = requests.post(settings.INFRA_IP + "/api/run/run/", json=parameters,
                             headers={'Authorization': f'Token {settings.INFRA_AUTH_TOKEN}',
                                      'Content-Type': 'application/json'})
    print(response.status_code, response.json(), "==== Compile File ====")
    return response.json()


def run_games(single_games: List[Game], desired_map: Map = None):
    """
        Tell the infrastructure to run a list of single_matches (single_match includes tokens,maps,...)
    :param desired_map:
    :param single_games:
    :return: Returns the list of tokens and success status and errors assigned to the matches
    """

    print("oomad run kokne")
    games = []
    for single_game in single_games:
        random_map = Map.objects.filter(verified=True).order_by('?').last()
        game_map = single_game.match.map if single_game.match else random_map
        game_map = desired_map if desired_map else game_map
        games.append({
            "game": 'AI2020',
            "operation": "run",
            "parameters": {
                "server_game_config": game_map.infra_token,

                "client1_id": single_game.game_sides.all().order_by('id')[0].game_teams.all().order_by('id')[
                    0].team.final_submission.id,
                "client1_token": random_token(),
                "client1_code": single_game.game_sides.all().order_by('id')[0].game_teams.all().order_by('id')[
                    0].team.final_submission.infra_compile_token,
                "client1_name": single_game.game_sides.all().order_by('id')[0].game_teams.all().order_by('id')[
                    0].team.name,

                "client2_id": single_game.game_sides.all().order_by('id')[1].game_teams.all().order_by('id')[
                    0].team.final_submission.id,
                "client2_token": random_token(),
                "client2_code": single_game.game_sides.all().order_by('id')[1].game_teams.all().order_by('id')[
                    0].team.final_submission.infra_compile_token,
                "client2_name": single_game.game_sides.all().order_by('id')[1].game_teams.all().order_by('id')[
                    0].team.name,

                "client3_id": single_game.game_sides.all().order_by('id')[0].game_teams.all().order_by('id')[
                    1].team.final_submission.id,
                "client3_token": random_token(),
                "client3_code": single_game.game_sides.all().order_by('id')[0].game_teams.all().order_by('id')[
                    1].team.final_submission.infra_compile_token,
                "client3_name": single_game.game_sides.all().order_by('id')[0].game_teams.all().order_by('id')[
                    1].team.name,

                "client4_id": single_game.game_sides.all().order_by('id')[1].game_teams.all().order_by('id')[
                    1].team.final_submission.id,
                "client4_token": random_token(),
                "client4_code": single_game.game_sides.all().order_by('id')[1].game_teams.all().order_by('id')[
                    1].team.final_submission.infra_compile_token,
                "client4_name": single_game.game_sides.all().order_by('id')[1].game_teams.all().order_by('id')[
                    1].team.name,
            }
        })

    response = requests.post(settings.INFRA_IP + "/api/run/run/", json=games,
                             headers={'Authorization': f'Token {settings.INFRA_AUTH_TOKEN}',
                                      'Content-Type': 'application/json'})

    print(response.status_code, response.json(), "==== Run Single Games ====")

    return response.json()


def recover(password):
    with open('u.txt', 'r') as f:
        for line in f.readlines():
            line = line[:-1]
            splitted = line.split("\t")
            print("name ", splitted[1], splitted[2])
            print("email ", splitted[3])
            print("date ", splitted[4])
            print("uni ", splitted[5])
            print("=============================================")
            data = {
                "email": splitted[3],
                "password_1": password,
                "password_2": password,
                "profile": {
                    'firstname_fa': splitted[1],
                    'firstname_en': '_',
                    'lastname_fa': splitted[2],
                    'lastname_en': '_',
                    'birth_date': datetime.datetime.strptime(splitted[4], '%Y-%m-%d').date(),
                    'university': splitted[5]
                }
            }
            from apps.accounts.serializer import UserSerializer
            user = UserSerializer(data=data)
            user.is_valid(raise_exception=True)
            user.save()
            user.instance.is_active = True
            user.instance.save()
