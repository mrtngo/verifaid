from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import TrustSet, Memo
from xrpl.transaction import autofill, sign, submit_and_wait
from xrpl.models.requests import AccountLines

# --- 1. Connect to XRPL Testnet ---
client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")

# --- 2. Load your test wallet ---
# Replace with your own testnet seed
test_wallet = Wallet.from_seed("sEdSC14dqK2uyGfDj8DaWk7evGrRfeN")

# --- 3. Define RLUSD issuer and trustline config ---
RLUSD_ISSUER = "rQhWct2fv4Vc4KRjRgMrxa8xPN9Zx9iLKV"
RLUSD_CURRENCY = "RLUSD".ljust(20, '\x00').encode("utf-8").hex().upper()
TRUST_LIMIT = "1000000"

# --- 4. Check if trustline already exists ---
existing = client.request(AccountLines(account=test_wallet.classic_address))
trustline_exists = any(
    line["currency"] == RLUSD_CURRENCY and line["account"] == RLUSD_ISSUER
    for line in existing.result.get("lines", [])
)

if trustline_exists:
    print("Trustline already exists. Skipping TrustSet transaction.")
else:
    # --- 5. Construct TrustSet transaction ---
    tx = TrustSet(
        account=test_wallet.classic_address,
        limit_amount={
            "currency": RLUSD_CURRENCY,
            "issuer": RLUSD_ISSUER,
            "value": TRUST_LIMIT
        },
        memos=[
            Memo(
                memo_type="54797065",         # Hex for "Type"
                memo_data="527573744C696E65"  # Hex for "TrustLine"
            )
        ]
    )

    # --- 6. Autofill, sign, and submit transaction ---
    tx = autofill(tx, client)
    signed_tx = sign(tx, test_wallet)
    response = submit_and_wait(signed_tx, client)

    # --- 7. Output result ---
    result = response.result
    print("TrustSet Transaction Result:")
    print(result)

    if result["meta"]["TransactionResult"] == "tesSUCCESS":
        print("✅ Trustline successfully created.")
    else:
        print("❌ Failed to create trustline:", result["meta"]["TransactionResult"])
