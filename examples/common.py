from architect_py.client import Client
from dotenv import load_dotenv
import os


def create_client():
    load_dotenv()
    host = os.environ["ARCHITECT_HOST"]
    api_key = os.getenv("ARCHITECT_API_KEY")
    api_secret = os.getenv("ARCHITECT_API_SECRET")
    use_tls = False if (api_key == None and api_secret == None) else True

    c = Client(
        host=host,
        api_key=api_key,
        api_secret=api_secret,
        use_tls=use_tls,
    )
    return c
