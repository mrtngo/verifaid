import os
import json
import binascii

from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment, Memo
from xrpl.models.requests import AccountLines, BookOffers
from xrpl.transaction import autofill, sign, submit_and_wait
from xrpl.utils import str_to_hex, xrp_to_drops

# ---------------------
# Config
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234"
RLUSD_ISSUER = "rQhWct2fv4Vc4KRjRgMrxa8xPN9Zx9iLKV"
RLUSD_CURRENCY = "RLUSD".ljust(20, '\x00').encode().hex().upper()
DONATION_WALLET = "rNe5k36gwZVVfgb3QN1FqwwbEwyD5Wxgik"  # recipient wallet

client = JsonRpcClient(JSON_RPC_URL)


def has_rlusd_trustline(wallet_address):
    resp = client.request(AccountLines(account=wallet_address))
    for line in resp.result.get("lines", []):
        if line["currency"] == RLUSD_CURRENCY and line["account"] == RLUSD_ISSUER:
            return True
    return False


def get_rlusd_price_xrp():
    resp = client.request(BookOffers(
        taker_gets={"currency": RLUSD_CURRENCY, "issuer": RLUSD_ISSUER},
        taker_pays={"currency": "XRP"},
        limit=1
    ))
    offers = resp.result.get("offers", [])
    if not offers:
        raise Exception("No liquidity for RLUSD/XRP")
    return float(offers[0]["quality"])  # 1 RLUSD in XRP


def create_memo(key, value):
    return Memo(
        memo_type=str_to_hex(key),
        memo_data=str_to_hex(value)
    )


def send_rlusd_payment(wallet, amount_rlusd, memo=None):
    tx = Payment(
        account=wallet.classic_address,
        destination=DONATION_WALLET,
        amount={
            "currency": RLUSD_CURRENCY,
            "issuer": RLUSD_ISSUER,
            "value": str(amount_rlusd)
        },
        memos=[memo] if memo else None
    )
    tx = autofill(tx, client)
    signed_tx = sign(tx, wallet)
    return submit_and_wait(signed_tx, client)


def send_xrp_path_payment(wallet, amount_rlusd, memo=None):
    price = get_rlusd_price_xrp()
    xrp_amount = float(amount_rlusd) * price
    xrp_drops = str(int(xrp_to_drops(xrp_amount)))

    tx = Payment(
        account=wallet.classic_address,
        destination=DONATION_WALLET,
        amount={
            "currency": RLUSD_CURRENCY,
            "issuer": RLUSD_ISSUER,
            "value": str(amount_rlusd)
        },
        send_max=xrp_drops,
        memos=[memo] if memo else None
    )
    tx = autofill(tx, client)
    signed_tx = sign(tx, wallet)
    return submit_and_wait(signed_tx, client)


def main():
    print("=== RLUSD DONATION SCRIPT ===")

    seed = input("Donor wallet seed: ").strip()
    amount = input("Amount to donate (RLUSD): ").strip()
    note = input("Memo (optional, like project ID or donor info): ").strip()

    wallet = Wallet.from_seed(seed)
    print(f"Using wallet: {wallet.classic_address}")

    has_trustline = has_rlusd_trustline(wallet.classic_address)
    memo = create_memo("donation", note) if note else None

    try:
        if has_trustline:
            print("Sending RLUSD directly...")
            response = send_rlusd_payment(wallet, amount, memo)
        else:
            print("No RLUSD trustline found. Using XRP -> RLUSD path payment...")
            response = send_xrp_path_payment(wallet, amount, memo)

        result = response.result
        print(json.dumps(result, indent=2))

        tx_hash = result.get("hash")
        if tx_hash:
            print(f"🔗 Explorer: https://testnet.xrpl.org/transactions/{tx_hash}")
        if result["meta"]["TransactionResult"] == "tesSUCCESS":
            print("✅ Donation successful.")
        else:
            print("❌ Donation failed:", result["meta"]["TransactionResult"])

    except Exception as e:
        print("❌ Error during donation:", str(e))


if __name__ == "__main__":
    main()
