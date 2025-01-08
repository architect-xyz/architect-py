import json
import random
import uuid
from collections import defaultdict
from datetime import datetime

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


class SimpleExternalCpty(WebSocket):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # in a prod environment, these should probably be global and not per-connection
        self.open_orders = {}
        self.balances = defaultdict(lambda: 0.0)

    def logAndSendMessage(self, data):
        print(f"> {data}")
        self.sendMessage(data)

    def handleMessage(self):
        print(f"< {self.data}")  # debug print the incoming message
        m = json.loads(self.data)
        try:
            if m["type"] == "GetSymbology":
                self.logAndSendMessage(
                    json.dumps(
                        {
                            "type": "Symbology",
                            "markets": ["FOO Crypto/ETH Crypto", "BAR Stock/USD"],
                        }
                    )
                )
            elif m["type"] == "GetOpenOrders":
                self.logAndSendMessage(
                    json.dumps(
                        {
                            "type": "OpenOrders",
                            "open_orders": list(self.open_orders.keys()),
                        }
                    )
                )
            elif m["type"] == "Order":
                what_to_do = random.choice([0, 1, 2])
                if what_to_do == 0:
                    # fill immediately: ack, fill, out
                    self.logAndSendMessage(
                        json.dumps(
                            {
                                "type": "Ack",
                                "order_id": m["id"],
                            }
                        )
                    )
                    # increment balances on this fill
                    base_product = m["market"].split("/")[0]
                    quote_product = m["market"].split("/")[1]
                    qty = float(m["quantity"])
                    if m["dir"] == "Buy":
                        self.balances[base_product] += qty
                        self.balances[quote_product] -= qty * float(m["price"])
                    elif m["dir"] == "Sell":
                        self.balances[base_product] -= qty
                        self.balances[quote_product] += qty * float(m["price"])
                    self.logAndSendMessage(
                        json.dumps(
                            {
                                "type": "Fill",
                                "kind": "Normal",
                                "fill_id": str(uuid.uuid4()),
                                "order_id": m["id"],
                                "quantity": m["quantity"],
                                "price": m["price"],
                                "dir": m["dir"],
                                "trade_time": datetime.now().isoformat(),
                            }
                        )
                    )
                    self.logAndSendMessage(
                        json.dumps(
                            {
                                "type": "Out",
                                "order_id": m["id"],
                            }
                        )
                    )
                elif what_to_do == 1:
                    # leave this order on the book--don't fill: ack only
                    self.logAndSendMessage(
                        json.dumps(
                            {
                                "type": "Ack",
                                "order_id": m["id"],
                            }
                        )
                    )
                    self.open_orders[m["id"]] = m
                elif what_to_do == 2:
                    # reject the order: reject
                    self.logAndSendMessage(
                        json.dumps(
                            {
                                "type": "Reject",
                                "order_id": m["id"],
                                "reason": "Insufficient funds",
                            }
                        )
                    )
            elif m["type"] == "Cancel":
                # check if order is on the book, if so, remove it and send an out message
                # otherwise complain
                if m["order_id"] in self.open_orders:
                    del self.open_orders[m["order_id"]]
                    self.logAndSendMessage(
                        json.dumps(
                            {
                                "type": "Out",
                                "order_id": m["order_id"],
                            }
                        )
                    )
                else:
                    # print order id not found
                    print(
                        f'trying to cancel: order id {m["order_id"]} not found in open orders'
                    )
            elif m["type"] == "GetBalances":
                balances = []
                for k, v in self.balances.items():
                    balances.append([k, str(v)])
                self.logAndSendMessage(
                    json.dumps(
                        {
                            "type": "Balances",
                            "id": m["id"],
                            "result": {"balances": balances},
                        }
                    )
                )
        except Exception as e:
            print(f"error processing message: {e}")

    def handleConnected(self):
        print(self.address, "connected")

    def handleClose(self):
        print(self.address, "closed")


def main():
    print("Starting external cpty server...")
    server = SimpleWebSocketServer("127.0.0.1", 8000, SimpleExternalCpty)
    server.serveforever()


if __name__ == "__main__":
    main()
