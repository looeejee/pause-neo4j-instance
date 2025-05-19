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

def get_instances(access_token, tenant_id):
    response = requests.get(
        f"https://api.neo4j.io/v1/instances?tenantId={tenant_id}",
        headers={
            "Authorization": f"Bearer {access_token}",
            'Content-Type': 'application/json'
        }
    )
    response.raise_for_status()
    return response.json()['data']

def resume_instance(access_token, dbid):
    response = requests.post(
        f"https://api.neo4j.io/v1/instances/{dbid}/resume",
        headers={
            "Authorization": f"Bearer {access_token}",
            'Content-Type': 'application/json'
        }
    )
    
    # Check if the response indicates that the database is not running
    if response.status_code == 400:
        error_response = response.json()
        if "errors" in error_response:
            for error in error_response["errors"]:
                if error.get("reason") == "db-not-running":
                    print(f"Database {dbid} is not running. Skipping...")
                    return  # Skip to the next instance

    response.raise_for_status()  # Raise an error for other issues
    print(f"Paused instance {dbid}")

def main():
    user = os.getenv('CLIENT_ID')
    pwd = os.getenv('CLIENT_PWD')
    tenant_id = os.getenv('TENANT_ID')

    access_token = get_access_token(user, pwd)
    instances = get_instances(access_token, tenant_id)

    for instance in instances:
        if "luigib" in instance['name']:
            resume_instance(access_token, instance['id'])

if __name__ == "__main__":
    main()
