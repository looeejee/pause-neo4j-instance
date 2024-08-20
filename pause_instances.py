import os
import requests
import json

def get_access_token(user, pwd):
    response = requests.post(
        'https://api.neo4j.io/oauth/token',
        auth=(user, pwd),
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={'grant_type': 'client_credentials'}
    )
    response.raise_for_status()
    return response.json()['access_token']

def get_instances(access_token):
    response = requests.get(
        "https://api.neo4j.io/v1/instances?tenantId=%2275c61c13-4974-526a-ab9e-61cbfea1841e%22",
        headers={
            "Authorization": f"Bearer {access_token}",
            'Content-Type': 'application/json'
        }
    )
    response.raise_for_status()
    return response.json()['data']

def pause_instance(access_token, dbid):
    response = requests.post(
        f"https://api.neo4j.io/v1/instances/{dbid}/pause",
        headers={
            "Authorization": f"Bearer {access_token}",
            'Content-Type': 'application/json'
        }
    )
    response.raise_for_status()
    print(f"Paused instance {dbid}")

def main():
    user = os.getenv('CLIENT_ID')
    pwd = os.getenv('CLIENT_PWD')

    access_token = get_access_token(user, pwd)
    instances = get_instances(access_token)

    for instance in instances:
        if "luigib" in instance['name']:
            pause_instance(access_token, instance['id'])

if __name__ == "__main__":
    main()
