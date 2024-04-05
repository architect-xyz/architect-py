from graphql_client.client import Client
from dotenv import load_dotenv
import os


def create_client():
    load_dotenv()
    api_key = os.environ["ARCHITECT_API_KEY"]
    api_secret = os.environ["ARCHITECT_API_SECRET"]
    auth_header = f"Basic {api_key} {api_secret}"
    c = Client(
        url=os.environ["ARCHITECT_GRAPHQL_URL"],
        headers={"Authorization": auth_header},
        ws_url=os.environ["ARCHITECT_GRAPHQL_WS_URL"],
        ws_connection_init_payload={"authorization": auth_header},
    )
    return c
