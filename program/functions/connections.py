from decouple import config
from dydx3 import Client
from web3 import Web3
from constants import (
    HOST,
    ETH_ADDRESS,
    DYDX_API_KEY,
    DYDX_API_SECRET,
    DYDX_API_PASSPHRASE,
    STARK_PK,
    PROVIDER,
)


# Connect to DYDX
def connect_dydx():
    # Connect to DYDX
    client = Client(
        host=HOST,
        api_key_credentials={
            "key": DYDX_API_KEY,
            "secret": DYDX_API_SECRET,
            "passphrase": DYDX_API_PASSPHRASE,
        },
        stark_private_key=STARK_PK,
        eth_private_key=config("ETH_PK"),
        default_ethereum_address=ETH_ADDRESS,
        web3=Web3(Web3.HTTPProvider(PROVIDER)),
    )

    acct = client.private.get_account()
    acct_id = acct.data["account"]["id"]
    quote_balance = acct.data["account"]["quoteBalance"]

    print("Connected to DYDX")
    print("Acct ID:", acct_id)
    print("Balance:", quote_balance)

    return client
