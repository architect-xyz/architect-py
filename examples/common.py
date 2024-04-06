from architect_py.client import Client
from dotenv import load_dotenv
import os


def create_client():
    load_dotenv()
    host = os.environ["ARCHITECT_HOST"]
    api_key = os.environ["ARCHITECT_API_KEY"]
    api_secret = os.environ["ARCHITECT_API_SECRET"]
    c = Client(
        host=host,
        api_key=api_key,
        api_secret=api_secret,
    )
    return c
