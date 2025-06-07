import json
import hashlib

from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import TrustSet, Memo
from xrpl.transaction import autofill, sign, submit_and_wait
from xrpl.models.requests import AccountLines
from xrpl.utils import str_to_hex

def collect_ngo_data():
    print("\n=== NGO Registration Form ===")
    ngo_data = {}
    
    # Basic Information
    ngo_data["org_name"] = input("Enter organization name: ")
    ngo_data["wallet"] = input("Enter wallet address: ")
    
    # Location
    print("\nLocation Information:")
    ngo_data["location"] = {
        "country": input("Enter country: "),
        "city": input("Enter city: ")
    }
    
    # Staff Information
    ngo_data["staff_count"] = int(input("\nEnter number of staff members: "))
    ngo_data["monthly_salaries_usd"] = float(input("Enter total monthly salaries in USD: "))
    
    # Focus Areas
    print("\nEnter focus areas (one per line, press Enter twice to finish):")
    focus_areas = []
    while True:
        area = input("Focus area: ")
        if not area:
            break
        focus_areas.append(area)
    ngo_data["focus_areas"] = focus_areas
    
    # Suppliers
    print("\nEnter supplier information (press Enter for supplier name to finish):")
    suppliers = []
    while True:
        supplier_name = input("\nSupplier name (or press Enter to finish): ")
        if not supplier_name:
            break
        supplier = {
            "name": supplier_name,
            "type": input("Supplier type (goods/services): "),
            "country": input("Supplier country: ")
        }
        suppliers.append(supplier)
    ngo_data["suppliers"] = suppliers
    
    return ngo_data

# -------------------------
# 🔗 Connect to XRPL Testnet
client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")

# -------------------------
# 📝 Get NGO Metadata Payload


# -------------------------
# 🧠 Check if trustline exists
def create_ngo(): 
    ngo_data = collect_ngo_data()
    ngo_json = json.dumps(ngo_data, sort_keys=True)
    ngo_hash = hashlib.sha256(ngo_json.encode()).hexdigest()

    # -------------------------
    # 👛 Load Wallet
    print("\n=== Wallet Information ===")
    wallet_seed = input("Enter your wallet seed: ")
    test_wallet = Wallet.from_seed(wallet_seed)
    print("Wallet address:", test_wallet.classic_address)

    # -------------------------
    # 🪙 RLUSD Trustline Parameters
    RLUSD_ISSUER = "rQhWct2fv4Vc4KRjRgMrxa8xPN9Zx9iLKV"
    RLUSD_CURRENCY = "RLUSD".ljust(20, '\x00').encode("utf-8").hex().upper()
    TRUST_LIMIT = "1000000"
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
