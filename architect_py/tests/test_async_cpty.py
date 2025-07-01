import asyncio
from typing import AsyncGenerator, Optional, Sequence
from unittest.mock import MagicMock

import grpc
import pytest

from architect_py.async_cpty import AsyncCpty
from architect_py.grpc.models.Cpty.CptyRequest import (
    CancelAllOrders,
    CancelOrder,
    Login,
    Logout,
    PlaceOrder,
)
from architect_py.grpc.models.definitions import (
    AccountIdOrName,
    CptyLoginRequest,
    CptyLogoutRequest,
    TraderIdOrEmail,
)
from architect_py.grpc.models.Oms.Cancel import Cancel
from architect_py.grpc.models.Oms.Order import Order


class MockAsyncCpty(AsyncCpty):
    """Mock implementation of AsyncCpty for testing"""

    def __init__(self, execution_venue: str):
        super().__init__(execution_venue)
        self.login_called = False
        self.logout_called = False
        self.place_order_called = False
        self.cancel_order_called = False
        self.cancel_all_orders_called = False
        self.cancel_all_params = None

    async def on_login(self, request: CptyLoginRequest):
        self.login_called = True

    async def on_logout(self, request: CptyLogoutRequest):
        self.logout_called = True

    async def on_place_order(self, order: Order):
        self.place_order_called = True

    async def on_cancel_order(self, cancel: Cancel, original_order: Optional[Order] = None):
        self.cancel_order_called = True

    async def on_cancel_all_orders(
        self,
        account: Optional[AccountIdOrName] = None,
        execution_venue: Optional[str] = None,
        trader: Optional[TraderIdOrEmail] = None,
    ):
        self.cancel_all_orders_called = True
        self.cancel_all_params = {
            "account": account,
            "execution_venue": execution_venue,
            "trader": trader,
        }


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_cancel_all_orders_handler():
    """Test that on_cancel_all_orders is called correctly"""
    cpty = MockAsyncCpty("TEST_VENUE")
    
    # Create mock context
    context = MagicMock(spec=grpc.aio.ServicerContext)
    context.send_initial_metadata = MagicMock(return_value=asyncio.Future())
    context.send_initial_metadata.return_value.set_result(None)
    context.set_code = MagicMock()
    context.add_done_callback = MagicMock()
    
    # Create request stream
    async def request_iterator() -> AsyncGenerator:
        yield Login(account="test_account", trader="test_trader")
        yield CancelAllOrders(
            account="test_account",
            execution_venue="TEST_VENUE",
            trader="test_trader"
        )
        yield Logout()
    
    # Process requests
    responses = []
    async for response in cpty.Cpty(request_iterator(), context):
        responses.append(response)
    
    # Verify handler was called
    assert cpty.cancel_all_orders_called
    assert cpty.cancel_all_params == {
        "account": "test_account",
        "execution_venue": "TEST_VENUE",
        "trader": "test_trader",
    }


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_cancel_all_orders_no_params():
    """Test cancel all orders with no parameters"""
    cpty = MockAsyncCpty("TEST_VENUE")
    
    context = MagicMock(spec=grpc.aio.ServicerContext)
    context.send_initial_metadata = MagicMock(return_value=asyncio.Future())
    context.send_initial_metadata.return_value.set_result(None)
    context.set_code = MagicMock()
    context.add_done_callback = MagicMock()
    
    async def request_iterator() -> AsyncGenerator:
        yield Login(account="test_account", trader="test_trader")
        yield CancelAllOrders()  # No parameters
    
    responses = []
    async for response in cpty.Cpty(request_iterator(), context):
        responses.append(response)
    
    assert cpty.cancel_all_orders_called
    assert cpty.cancel_all_params == {
        "account": None,
        "execution_venue": None,
        "trader": None,
    }


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_cancel_all_orders_account_only():
    """Test cancel all orders for specific account only"""
    cpty = MockAsyncCpty("TEST_VENUE")
    
    context = MagicMock(spec=grpc.aio.ServicerContext)
    context.send_initial_metadata = MagicMock(return_value=asyncio.Future())
    context.send_initial_metadata.return_value.set_result(None)
    context.set_code = MagicMock()
    context.add_done_callback = MagicMock()
    
    async def request_iterator() -> AsyncGenerator:
        yield Login(account="test_account", trader="test_trader")
        yield CancelAllOrders(account="specific_account")
    
    responses = []
    async for response in cpty.Cpty(request_iterator(), context):
        responses.append(response)
    
    assert cpty.cancel_all_orders_called
    assert cpty.cancel_all_params["account"] == "specific_account"
    assert cpty.cancel_all_params["execution_venue"] is None
    assert cpty.cancel_all_params["trader"] is None


@pytest.mark.asyncio
@pytest.mark.timeout(3)
async def test_cancel_all_orders_requires_login():
    """Test that CancelAllOrders is ignored without login"""
    cpty = MockAsyncCpty("TEST_VENUE")
    
    context = MagicMock(spec=grpc.aio.ServicerContext)
    context.send_initial_metadata = MagicMock(return_value=asyncio.Future())
    context.send_initial_metadata.return_value.set_result(None)
    context.set_code = MagicMock()
    context.add_done_callback = MagicMock()
    
    async def request_iterator() -> AsyncGenerator:
        yield CancelAllOrders()  # No login first
    
    responses = []
    async for response in cpty.Cpty(request_iterator(), context):
        responses.append(response)
    
    # Should not be called without login
    assert not cpty.cancel_all_orders_called