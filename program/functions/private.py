from datetime import datetime, timedelta
import time
from pprint import pprint
from functions import utils


# Place MArket order
def place_market_order(client, market, side, size, price, reduce_only):
    acct_response = client.private.get_account()
    position_id = acct_response.data["account"]["positionId"]
    server_time = client.public.get_time()
    expiration = datetime.fromisoformat(
        server_time.data["iso"].replace("Z", "")
    ) + timedelta(seconds=70)

    placed_order = client.private.create_order(
        position_id=position_id,  # required for creating the order signature
        market=market,
        side=side,
        order_type="MARKET",
        post_only=False,
        size=size,
        price=price,
        limit_fee="0.015",
        expiration_epoch_seconds=expiration.timestamp(),
        time_in_force="FOK",
        reduce_only=reduce_only,
    )
    return placed_order.data


# Place Market order
def abort_all_positions(client):
    # cancel all orders
    client.private.cancel_all_orders()
    # protect api from spam
    time.sleep(0.5)
    # Get markets for referance of tick size
    markets = client.public.get_markets().data
    time.sleep(0.5)

    # get all open positions
    positions = client.private.get_positions(status="OPEN")
    all_positions = positions.data["positions"]

    close_orders = []
    if len(all_positions) > 0:
        # Loop through each position
        for position in all_positions:
            # Determine Market
            market = position["market"]
            # Determine Side
            side = "BUY"
            if position["side"] == "LONG":
                side = "SELL"
            print(market, side)

            price = float(position["entryPrice"])
            accept_price = price * 1.7 if side == "BUY" else price * 0.3
            tick_size = markets["markets"][market]["tickSize"]
            accept_price = utils.format_number(accept_price, tick_size)

            # Close Order
            order = place_market_order(
                client, market, side, position["sumOpen"], accept_price, True
            )

            # append to closed order
            close_orders.append(order)
            time.sleep(0.2)

        return close_orders
