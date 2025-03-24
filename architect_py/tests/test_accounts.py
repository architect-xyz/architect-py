from decimal import Decimal
import pytest

from architect_py.async_client import AsyncClient

from collections import defaultdict


@pytest.mark.asyncio
async def test_account(async_client: AsyncClient):
    return

    accounts = await async_client.list_accounts()
    assert accounts is not None
    assert len(accounts) > 0

    unaggregated_summary = await async_client.get_account_summary(
        account=accounts[0].account.id
    )

    symbol_to_position = defaultdict(Decimal)
    for symbol, positions in unaggregated_summary.positions.items():
        for position in positions:
            symbol_to_position[symbol] += position.quantity

    aggregated_summary = await async_client.get_account_summary(
        account=accounts[0].account.id
    )

    assert unaggregated_summary is not None
    assert aggregated_summary is not None
