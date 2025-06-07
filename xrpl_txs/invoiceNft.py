from xrpl.models.transactions import NFTokenMint

# -------- Configuration --------
# XRPL Testnet endpoint
JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"
# Your funded Testnet wallet seed (set as env var for security)
WALLET_SECRET = os.getenv("TEST_WALLET_SECRET")
# Pinata API credentials (set as env vars)
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY")
# Path to the receipt image to mint as an NFT
RECEIPT_FILE_PATH = "receipt.png"

# -------- Helper Functions --------
def upload_to_ipfs(file_path: str) -> str:
    """
    Uploads a file to IPFS via Pinata and returns the IPFS CID.
    """
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

def mint_receipt_nft(client: JsonRpcClient, wallet: Wallet, uri: str):
    """
    Mints an XRPL NFT with the provided URI (e.g., ipfs://CID).
    """
    # Convert URI to hex (uppercase) for XRPL URI field
    uri_hex = binascii.hexlify(uri.encode()).decode().upper()
    tx = NFTokenMint(
        account=wallet.classic_address,
        uri=uri_hex,
        nftoken_taxon=0  # You can choose a taxon value per project or use 0
    )
    signed_tx = safe_sign_and_autofill_transaction(tx, wallet, client)
    return send_reliable_submission(signed_tx, client)

# -------- Main Flow --------
def main():
    # Initialize XRPL client and wallet
    client = JsonRpcClient(JSON_RPC_URL)
    wallet = Wallet(seed=WALLET_SECRET, sequence=None)

    # 1. Upload receipt to IPFS
    cid = upload_to_ipfs(RECEIPT_FILE_PATH)
    ipfs_uri = f"ipfs://{cid}"
    print(f"Uploaded to IPFS: {ipfs_uri}")

    # 2. Mint the NFT linking to the receipt
    response = mint_receipt_nft(client, wallet, ipfs_uri)
    print("NFT Mint Transaction Result:", response.result)