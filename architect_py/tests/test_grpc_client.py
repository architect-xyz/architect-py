import asyncio
import os

from architect_py.grpc_client import GRPCClient
from architect_py.graphql_client.client import GraphQLClient


async def main():
    host = os.getenv("ARCHITECT_HOST") or "app.architect.co"
    port = int(os.getenv("ARCHITECT_PORT") or 4567)
    api_key = os.getenv("ARCHITECT_API_KEY")
    api_secret = os.getenv("ARCHITECT_API_SECRET")

    if api_key is None or api_secret is None:
        raise ValueError(
            "You must set ARCHITECT_API_KEY and ARCHITECT_API_SECRET to run tests"
        )

    graphql_client = GraphQLClient(
        host=host, port=port, api_key=api_key, api_secret=api_secret
    )

    grpc_client = GRPCClient(graphql_client)
    await grpc_client.grpc_channel("app.architect.co")


if __name__ == "__main__":
    asyncio.run(main())
