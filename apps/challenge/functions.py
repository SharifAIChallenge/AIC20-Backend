import random
import string
from typing import List

import requests

import coreapi
from django.conf import settings
from django.core.files import File

from apps.challenge.models import Game


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


def upload_file(file):
    """
    This function uploads a file to infrastructure synchronously
    :param file: File field from TeamSubmission model
    :return: file token or raises error with error message
    """
    print("ommad upload kone")
    response = requests.put(settings.INFRA_IP + "/api/storage/new_file/", files={'file': file},
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
    print(response.status_code, response.content, "==== Download File ====")
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


def run_games(single_games: List[Game]):
    """
        Tell the infrastructure to run a list of single_matches (single_match includes tokens,maps,...)
    :param single_games:
    :return: Returns the list of tokens and success status and errors assigned to the matches
    """

    print("oomad run kokne")
    games = []
    for single_game in single_games:
        games.append({
            "game": 'AI2020',
            "operation": "run",
            "parameters": {
                "server_game_config": single_game.match.map.infra_token,
                "client1_id": single_game.game_sides.part1.submission.id,
                "client1_token": random_token(),
                "client1_code": single_game.,
                "client1_name": single_game.match.part1.submission.team.team.id,
                "client2_id": single_game.match.part2.submission.id,
                "client2_token": random_token(),
                "client2_code": single_game.get_second_file(),
                "client2_name": single_game.match.part2.submission.team.team.id,
                "map_name": single_game.map.name
            }
        })

    response = requests.post(settings.INFRA_IP + "/api/run/run/", json=games,
                             headers={'Authorization': f'Token {settings.INFRA_AUTH_TOKEN}',
                                      'Content-Type': 'application/json'})
    print(response.status_code, response.json(), "==== Run Single Games ====")

    return response.json()
