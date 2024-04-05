from graphql_client.client import Client
from os import environ

def create_client():
    api_key = environ["ARCHITECT_API_KEY"] 
    api_secret = environ["ARCHITECT_API_SECRET"]
    auth_header = f"Basic {api_key} {api_secret}"
    c = Client(
        url=environ["ARCHITECT_GRAPHQL_URL"],
        headers={"Authorization": auth_header},
        ws_url=environ["ARCHITECT_GRAPHQL_WS_URL"],
        ws_connection_init_payload={"authorization": auth_header},
    )
    return c