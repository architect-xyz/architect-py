import pytest

from architect_py import AsyncClient


@pytest.mark.asyncio
async def test_list_accounts(async_client: AsyncClient):
    accounts = await async_client.list_accounts()
    assert accounts is not None
    assert len(accounts) > 0


@pytest.mark.asyncio
async def test_get_account_summary(async_client: AsyncClient):
    accounts = await async_client.list_accounts()
    assert accounts is not None
    assert len(accounts) > 0

    summary = await async_client.get_account_summary(account=accounts[0].account.name)
    assert summary is not None
    assert summary.balances is not None
    assert len(summary.balances) > 0
    assert summary.positions is not None

    await async_client.close()
