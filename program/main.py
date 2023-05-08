from functions import connections, private, public

from constants import ABORT_ALL_POSITIONS, FIND_COINTERGRATED

if __name__ == "__main__":
    try:
        print("Connecting to client...")
        client = connections.connect_dydx()
    except Exception as e:
        print(e)
        print("error connecting to client:", e)
        exit(1)

    # Abort all open positions
    if ABORT_ALL_POSITIONS:
        try:
            print("Closing all positions...")
            close_orders = private.abort_all_positions(client)
        except Exception as e:
            print(e)
            print("error Closing all positions:", e)
            exit(1)

    if FIND_COINTERGRATED:
        try:
            print("Fetching Market Prices, wait up to 5 mins")
            df_market_prices = public.construct_market_prices(client)
        except Exception as e:
            print(e)
            print("error construct_market_prices:", e)
            exit(1)