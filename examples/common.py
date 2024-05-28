from architect_py.client import Client
from dotenv import load_dotenv
import os


def create_client():
    load_dotenv()
    host = os.environ["ARCHITECT_HOST"]
    api_key = os.getenv("ARCHITECT_API_KEY")
    api_secret = os.getenv("ARCHITECT_API_SECRET")
    implicit_use_tls = api_key is not None or api_secret is not None
    explicit_use_tls = os.getenv("ARCHITECT_USE_TLS")
    use_tls = False
    if explicit_use_tls == "true" or explicit_use_tls == "1":
        use_tls = True
    elif explicit_use_tls is None:
        use_tls = implicit_use_tls

    c = Client(
        host=host,
        api_key=api_key,
        api_secret=api_secret,
        use_tls=use_tls,
    )
    return c
