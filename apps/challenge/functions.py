import random
import string
import requests

import coreapi
from django.conf import settings


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
    response = requests.get(settings.INFRA_IP + f"/api/storage/get_file/{file_token}/", allow_redirects=True)
    print(response.status_code, response.content, "==== Download File ====")
    return response


def compile_submissions(submissions):
    """
        Tell the infrastructure to compile a list of submissions
    :return: list of dictionaries each have token, success[, errors] keys
    """
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


def run_matches(single_matches):
    """
        Tell the infrastructure to run a list of single_matches (single_match includes tokens,maps,...)
    :param single_matches:
    :return: Returns the list of tokens and success status and errors assigned to the matches
    """

    games = []
    for single_match in single_matches:
        games.append({
            "game": single_match.get_game_id(),
            "operation": "run",
            "parameters": {
                "server_game_config": single_match.get_map(),
                "client1_id": single_match.match.part1.submission.id,
                "client1_token": random_token(),
                "client1_code": single_match.get_first_file(),
                "client1_name": single_match.match.part1.submission.team.team.id,
                "client2_id": single_match.match.part2.submission.id,
                "client2_token": random_token(),
                "client2_code": single_match.get_second_file(),
                "client2_name": single_match.match.part2.submission.team.team.id,
                "map_name": single_match.map.name
            }
        })

    # Send request to infrastructure to compile them

    client, schema = create_infra_client()

    match_details = client.action(schema,
                                  ['run', 'run', 'create'],
                                  params={
                                      'data': games
                                  })

    return match_details
