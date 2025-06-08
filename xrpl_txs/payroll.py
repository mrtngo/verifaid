import json
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment, Memo
from xrpl.transaction import autofill, sign, submit_and_wait
from xrpl.utils import str_to_hex, xrp_to_drops

# XRPL Testnet client
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")


def create_memo(key, value):
    return Memo(
        memo_type=str_to_hex(key),
        memo_data=str_to_hex(value)
    )


def send_xrp(wallet, destination, amount_xrp, memo_text=None):
    drops = str(xrp_to_drops(float(amount_xrp)))
    memo = create_memo("payroll", memo_text) if memo_text else None

    tx = Payment(
        account=wallet.classic_address,
        destination=destination,
        amount=drops,
        memos=[memo] if memo else None
    )

    tx = autofill(tx, client)
    signed = sign(tx, wallet)
    return submit_and_wait(signed, client)


def payroll():
    print("=== BATCH XRP PAYROLL ===")
    seed = input("Sender wallet seed: ").strip()
    memo_text = input("Memo for all payments (e.g. 'June Payroll'): ").strip()

    wallet = Wallet.from_seed(seed)
    print(f"Using wallet: {wallet.classic_address}\n")

    while True:
        dest = input("Employee wallet (or 'done' to finish): ").strip()
        if dest.lower() == "done":
            print("✅ Payroll completed.")
            break

        amount = input(f"Amount to send to {dest} (XRP): ").strip()

        try:
            response = send_xrp(wallet, dest, amount, memo_text)
            result = response.result

            print(json.dumps(result, indent=2))
            tx_hash = result.get("hash")
            status = result["meta"]["TransactionResult"]

            print(f"🔗 https://testnet.xrpl.org/transactions/{tx_hash}")
            print(f"✅ Payment to {dest}: {amount} XRP - {status}\n")

        except Exception as e:
            print(f"❌ Error sending to {dest}: {str(e)}\n")


if __name__ == "__main__":
    main()
