# import json
# import hashlib

# from xrpl.clients import JsonRpcClient
# from xrpl.models.transactions import Payment, Memo
# from xrpl.wallet import generate_faucet_wallet
# from xrpl.transaction import submit_and_wait
# from xrpl.utils import str_to_hex, xrp_to_drops
# from xrpl.wallet import Wallet

# # -------------------------
# # 🔗 XRPL Testnet Client
# client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

# # -------------------------
# # 📝 Sample NGO Metadata
# ngo_data = {
#     "org_name": "AidForAll",
#     "wallet": "rTEST_WALLET",  # replace later with actual
#     "location": {"country": "Kenya", "city": "Nairobi"},
#     "staff_count": 14,
#     "monthly_salaries_usd": 6000,
#     "focus_areas": ["health", "disaster"],
#     "suppliers": [
#         {"name": "Nairobi Food Co.", "type": "goods", "country": "Kenya"}
#     ]
# }

# # -------------------------
# # 🧠 Create hash of the JSON payload
# ngo_json = json.dumps(ngo_data, sort_keys=True)
# ngo_hash = hashlib.sha256(ngo_json.encode()).hexdigest()
# print("NGO Hash:", ngo_json)

# # -------------------------
# wallet = Wallet.from_seed("sEd7sxaGSepuzTvqf5aGhejMnfsyfVA")

# print("Using wallet:", wallet.classic_address)

# print("Wallet Address:", wallet.classic_address)

# # -------------------------
# # 📦 Create Memo
# memo = Memo(
#     memo_type=str_to_hex("ngo_onboarding"),
#     memo_data=str_to_hex(ngo_json)
# )

# # -------------------------
# # 💸 Create Payment TX (to self)
# payment_tx = Payment(
#     account=wallet.classic_address,
#     destination="rPT1Sjq2YGrBMTttX4GZHjKu9dyfzbpAYe",  # confirmed valid
#     amount="1",  # 1 drop
#     memos=[memo]
# )




# # -------------------------
# # 🚀 Submit TX
# try:
#     response = submit_and_wait(payment_tx, client, wallet)
#     tx_hash = response.result["hash"]
#     print("✅ TX Hash:", tx_hash)
#     print("🔍 Explorer:", f"https://testnet.xrpl.org/transactions/{tx_hash}")
# except Exception as e:
#     print("❌ Submission failed:", str(e))


import json
import hashlib

from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import TrustSet, Memo
from xrpl.transaction import autofill, sign, submit_and_wait
from xrpl.models.requests import AccountLines
from xrpl.utils import str_to_hex

# -------------------------
# 🔗 Connect to XRPL Testnet
client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")

# -------------------------
# 📝 NGO Metadata Payload
ngo_data = {
    "org_name": "AidForAll",
    "wallet": "rTEST_WALLET",
    "location": {"country": "Kenya", "city": "Nairobi"},
    "staff_count": 14,
    "monthly_salaries_usd": 6000,
    "focus_areas": ["health", "disaster"],
    "suppliers": [
        {"name": "Nairobi Food Co.", "type": "goods", "country": "Kenya"}
    ]
}

ngo_json = json.dumps(ngo_data, sort_keys=True)
ngo_hash = hashlib.sha256(ngo_json.encode()).hexdigest()

# -------------------------
# 👛 Load Wallet
test_wallet = Wallet.from_seed("sEdSMox8K3oEoHGUHEGkgugKRnUEyLB")
print("Wallet:", test_wallet.classic_address)

# -------------------------
# 🪙 RLUSD Trustline Parameters
RLUSD_ISSUER = "rQhWct2fv4Vc4KRjRgMrxa8xPN9Zx9iLKV"
RLUSD_CURRENCY = "RLUSD".ljust(20, '\x00').encode("utf-8").hex().upper()
TRUST_LIMIT = "1000000"

# -------------------------
# 🧠 Check if trustline exists
existing = client.request(AccountLines(account=test_wallet.classic_address))
trustline_exists = any(
    line["currency"] == RLUSD_CURRENCY and line["account"] == RLUSD_ISSUER
    for line in existing.result.get("lines", [])
)

if trustline_exists:
    print("Trustline already exists. Skipping.")
else:
    # -------------------------
    # 📝 Add NGO onboarding memo
    memo = Memo(
        memo_type=str_to_hex("ngo_onboarding"),
        memo_data=str_to_hex(ngo_json)
    )

    # -------------------------
    # 🧾 TrustSet TX
    tx = TrustSet(
        account=test_wallet.classic_address,
        limit_amount={
            "currency": RLUSD_CURRENCY,
            "issuer": RLUSD_ISSUER,
            "value": TRUST_LIMIT
        },
        memos=[memo]
    )

    # -------------------------
    # 🚀 Submit TX
    try:
        tx = autofill(tx, client)
        signed_tx = sign(tx, test_wallet)
        response = submit_and_wait(signed_tx, client)
        result = response.result

        print("TrustSet Transaction Result:")
        print(json.dumps(result, indent=2))

        if result["meta"]["TransactionResult"] == "tesSUCCESS":
            print("✅ Trustline created.")
            print("🔗 Explorer:", f"https://testnet.xrpl.org/transactions/{result['hash']}")
        else:
            print("❌ Failed:", result["meta"]["TransactionResult"])

    except Exception as e:
        print("❌ Submission error:", str(e))
