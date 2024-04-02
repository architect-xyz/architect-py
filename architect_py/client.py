import gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.websockets import WebsocketsTransport
from typing import Optional


class Client:
    def __init__(
        self,
        rest_url: str = "http://localhost:4567",
        ws_url: str = "ws://localhost:4567",
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
    ):
        self.rest_url = rest_url
        self.ws_url = ws_url
        self.api_key = api_key
        self.api_secret = api_secret
        headers = {}
        if api_key and api_secret:
            headers = {"Authorization": f"Basic {api_key} {api_secret}"}
        transport = AIOHTTPTransport(url=f"{self.rest_url}/graphql", headers=headers)
        self.session = gql.Client(
            transport=transport, fetch_schema_from_transport=False
        )
        init_payload = {}
        if api_key and api_secret:
            init_payload = {"authorization": f"Basic {api_key} {api_secret}"}
        ws_transport = WebsocketsTransport(
            url=f"{self.ws_url}/graphql",
            init_payload=init_payload,
            connect_args={"ping_interval": None},
        )
        self.ws_session = gql.Client(
            transport=ws_transport, fetch_schema_from_transport=False
        )

    def execute(self, request: str, variables: dict = None):
        return self.session.execute(gql.gql(request), variable_values=variables)

    async def execute_async(self, request: str, variables: dict = None):
        return await self.session.execute_async(
            gql.gql(request), variable_values=variables
        )

    def subscribe(self, request: str, variables: dict = None):
        return self.ws_session.subscribe(gql.gql(request), variable_values=variables)

    async def subscribe_async(self, request: str, variables: dict = None):
        return self.ws_session.subscribe_async(
            gql.gql(request), variable_values=variables
        )
