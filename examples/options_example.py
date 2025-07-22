import asyncio
from decimal import Decimal

from architect_py import *

from .config import connect_async_client


async def main():
    c: AsyncClient = await connect_async_client()

    assert c.paper_trading, "This example requires paper trading to be enabled."

    underlying = "TSLA US Equity"
    underlying_tradable_product = TradableProduct(underlying, "USD")
    venue = "US-EQUITIES"

    expirations = await c.get_options_expirations(underlying=underlying, venue=venue)
    print(f"expirations: {expirations.expirations}")

    expiration = expirations.expirations[0]

    wraps = await c.get_options_wraps(underlying=underlying, venue=venue)
    print(f"wraps: {wraps.wraps}")

    wrap = next((s for s in wraps.wraps if s in underlying), None)
    # get first element not in the underlying, otherwise give None
    # in this case 1TSLA or 2TSLA

    if wrap:
        print(f"wrap: {wrap}")

    chain = await c.get_options_chain(
        expiration=expirations.expirations[0],
        underlying=underlying,
        venue=venue,
    )

    print(f"chain calls: {chain.calls[:5]}")
    print(f"chain puts: {chain.puts[:5]}")

    options_chain_greeks = await c.get_options_chain_greeks(
        expiration=expiration, underlying=underlying, venue=venue
    )
    print(f"options chain greeks for {underlying}: {options_chain_greeks}")

    if wrap:
        chain = await c.get_options_chain(
            expiration=expiration,
            underlying=underlying,
            wrap=wrap,
            venue=venue,
        )
        print(f"chain calls with wrap: {chain.calls[:5]}")
        print(f"chain puts with wrap: {chain.puts[:5]}")

        options_chain_greeks = await c.get_options_chain_greeks(
            expiration=expiration, underlying=underlying, wrap=wrap, venue=venue
        )
        print(
            f"options chain greeks with wrap for {underlying}: {options_chain_greeks}"
        )

    ticker = await c.get_ticker(symbol=underlying_tradable_product, venue=venue)
    print(f"ticker: {ticker}")

    option_contract = chain.calls[0]

    tradable_product = c.get_option_symbol(option_contract)

    ticker = await c.get_ticker(symbol=tradable_product, venue=venue)
    print(f"option ticker for {tradable_product}: {ticker}")

    contract_greeks = await c.get_options_contract_greeks(
        contract=tradable_product, venue=venue
    )
    print(f"option greeks for {tradable_product}: {contract_greeks}")

    accounts = await c.list_accounts()
    assert len(accounts) > 0, "No accounts found"
    account = accounts[0].account.name

    order = await c.place_order(
        symbol=tradable_product,
        execution_venue=venue,
        dir=OrderDir.BUY,
        quantity=Decimal(1),
        price=ticker.bid_price,
        order_type=OrderType.LIMIT,
        account=account,
    )
    print(f"Placed order: {order}")

    await c.close()


asyncio.run(main())
