import os
import binascii
import json
import requests

from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import NFTokenMint
from xrpl.transaction import autofill, sign, submit_and_wait


# -------- Configuration --------
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
WALLET_SECRET = "sEdSMox8K3oEoHGUHEGkgugKRnUEyLB"
PINATA_API_KEY = "f0b9f53a248209ce82b8"
PINATA_SECRET_API_KEY = "1b69c4981301fbcf6c74d6bbd6489f8456563230243fe4ffd5f5189873df462e"


# -------- Upload File to IPFS --------
def upload_to_ipfs(file_path: str) -> str:
    url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    with open(file_path, "rb") as f:
        files = {"file": f}
        headers = {
            "pinata_api_key": PINATA_API_KEY,
            "pinata_secret_api_key": PINATA_SECRET_API_KEY
        }
        res = requests.post(url, files=files, headers=headers)
        res.raise_for_status()
        return res.json()["IpfsHash"]

# -------- Mint NFT on XRPL --------
def mint_receipt_nft(client: JsonRpcClient, wallet: Wallet, uri: str):
    uri_hex = binascii.hexlify(uri.encode()).decode().upper()
    tx = NFTokenMint(
        account=wallet.classic_address,
        uri=uri_hex,
        nftoken_taxon=0,
        flags=8  # tfTransferable
    )

    tx = autofill(tx, client)
    signed_tx = sign(tx, wallet)
    return submit_and_wait(signed_tx, client)


# -------- Main Flow --------
def uploadInvoiceAsNFT():
    if not all([WALLET_SECRET, PINATA_API_KEY, PINATA_SECRET_API_KEY]):
        print("❌ One or more required env vars are missing.")
        return

    client = JsonRpcClient(JSON_RPC_URL)
    print("\n=== Wallet Information ===")
    wallet_seed = input("Enter your wallet seed: ")
    wallet = Wallet.from_seed(wallet_seed)
    print("Wallet address:", wallet.classic_address)

    try:
        # 1. Upload file to IPFS
        RECEIPT_FILE_PATH = input("Enter the path to your receipt file: ")
        cid = upload_to_ipfs(RECEIPT_FILE_PATH)
        ipfs_uri = f"ipfs://{cid}"
        print(f"📦 Uploaded to IPFS: {ipfs_uri}")

        # 2. Mint NFT
        response = mint_receipt_nft(client, wallet, ipfs_uri)
        result = response.result

        print("✅ NFT Mint Transaction Submitted:")
        print(json.dumps(result, indent=2))

        tx_hash = result.get("hash")
        if tx_hash:
            print(f"🔗 Explorer: https://testnet.xrpl.org/transactions/{tx_hash}")

    except Exception as e:
        print("❌ Error:", str(e))

# -------- Run it --------
if __name__ == "__main__":
    main()
