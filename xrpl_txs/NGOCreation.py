import json
import hashlib

from xrpl.clients import JsonRpcClient
from xrpl.models.transactions import Payment, Memo
from xrpl.wallet import generate_faucet_wallet
from xrpl.transaction import submit_and_wait
from xrpl.utils import str_to_hex, xrp_to_drops
from xrpl.wallet import Wallet

# -------------------------
# 🔗 XRPL Testnet Client
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

# -------------------------
# 📝 Sample NGO Metadata
ngo_data = {
    "org_name": "AidForAll",
    "wallet": "rTEST_WALLET",  # replace later with actual
    "location": {"country": "Kenya", "city": "Nairobi"},
    "staff_count": 14,
    "monthly_salaries_usd": 6000,
    "focus_areas": ["health", "disaster"],
    "suppliers": [
        {"name": "Nairobi Food Co.", "type": "goods", "country": "Kenya"}
    ]
}

# -------------------------
# 🧠 Create hash of the JSON payload
ngo_json = json.dumps(ngo_data, sort_keys=True)
ngo_hash = hashlib.sha256(ngo_json.encode()).hexdigest()
print("NGO Hash:", ngo_json)

# -------------------------
wallet = Wallet.from_seed("sEd7sxaGSepuzTvqf5aGhejMnfsyfVA")

print("Using wallet:", wallet.classic_address)

print("Wallet Address:", wallet.classic_address)

# -------------------------
# 📦 Create Memo
memo = Memo(
    memo_type=str_to_hex("ngo_onboarding"),
    memo_data=str_to_hex(ngo_json)
)

# -------------------------
# 💸 Create Payment TX (to self)
payment_tx = Payment(
    account=wallet.classic_address,
    destination="rPT1Sjq2YGrBMTttX4GZHjKu9dyfzbpAYe",  # confirmed valid
    amount="1",  # 1 drop
    memos=[memo]
)




# -------------------------
# 🚀 Submit TX
try:
    response = submit_and_wait(payment_tx, client, wallet)
    tx_hash = response.result["hash"]
    print("✅ TX Hash:", tx_hash)
    print("🔍 Explorer:", f"https://testnet.xrpl.org/transactions/{tx_hash}")
except Exception as e:
    print("❌ Submission failed:", str(e))
