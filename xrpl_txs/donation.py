import os
import json
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment, Memo
from xrpl.transaction import autofill, sign, submit_and_wait
from xrpl.utils import str_to_hex, xrp_to_drops

# ---------------------
# Config
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234"
client = JsonRpcClient(JSON_RPC_URL)

# ---------------------
def create_memo(key, value):
    return Memo(
        memo_type=str_to_hex(key),
        memo_data=str_to_hex(value)
    )

def send_xrp_payment(wallet, amount_xrp, destination, memo=None):
    drops = str(xrp_to_drops(float(amount_xrp)))


    tx = Payment(
        account=wallet.classic_address,
        destination=destination,
        amount=drops,
        memos=[memo] if memo else None
    )

    tx = autofill(tx, client)
    signed_tx = sign(tx, wallet)
    return submit_and_wait(signed_tx, client)

def donate():
    print("=== XRP DONATION SCRIPT ===")

    seed = input("Donor wallet seed: ").strip()
    amount = input("Amount to donate (XRP): ").strip()
    note = input("Memo (optional, like project ID or donor info): ").strip()
    donation_wallet = input("Donation wallet address: ").strip()

    wallet = Wallet.from_seed(seed)
    print(f"Using wallet: {wallet.classic_address}")
    memo = create_memo("donation", note) if note else None

    try:
        response = send_xrp_payment(wallet, amount, donation_wallet, memo)
        result = response.result

        print(json.dumps(result, indent=2))
        tx_hash = result.get("hash")
        if tx_hash:
            print(f"🔗 Explorer: https://testnet.xrpl.org/transactions/{tx_hash}")

        if result["meta"]["TransactionResult"] == "tesSUCCESS":
            print("✅ Donation successful.")
        else:
            print("❌ Donation failed:", result['meta']['TransactionResult'])

    except Exception as e:
        print("❌ Error during donation:", str(e))


if __name__ == "__main__":
    main()
