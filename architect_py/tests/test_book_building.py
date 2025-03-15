from decimal import Decimal
import pytest

from architect_py.grpc_client.Marketdata.L2BookUpdate import Diff, Snapshot
from architect_py.grpc_client.grpc_client import L2_update_from_diff


@pytest.mark.asyncio
async def test_book_build():
    snapshot = Snapshot(
        a=[],
        b=[],
        sid=0,
        sn=0,
        ts=0,
        tn=0,
    )

    L2_update_from_diff(
        snapshot,
        Diff(
            a=[[Decimal(1), Decimal(1)]],
            b=[],
            sid=0,
            sn=0,
            ts=0,
            tn=0,
        ),
    )

    assert snapshot == Snapshot(
        a=[[Decimal(1), Decimal(1)]],
        b=[],
        sid=0,
        sn=0,
        ts=0,
        tn=0,
    )

    snapshot = Snapshot(
        a=[[Decimal(3), Decimal(3)], [Decimal(4), Decimal(4)]],
        b=[[Decimal(1), Decimal(1)], [Decimal(2), Decimal(2)]],
        sid=0,
        sn=0,
        ts=0,
        tn=0,
    )

    diff = Diff(
        a=[[Decimal(3), Decimal(3)], [Decimal(4), Decimal(4)]],
        b=[[Decimal(1), Decimal(1)], [Decimal(2), Decimal(2)]],
        sid=0,
        sn=0,
        ts=0,
        tn=0,
    )
