# 3. Define RLUSD issuer and currency code (Testnet)
RLUSD_ISSUER = "rQhWct2fv4Vc4KRjRgMrxa8xPN9Zx9iLKV"
RLUSD_CURRENCY = "RLUSD"
TRUST_LIMIT = "1000000"  # Maximum RLUSD this account can hold

# 4. Construct a TrustSet transaction to establish a trustline for RLUSD
trust_set_tx = TrustSet(
    account=test_wallet.classic_address,
    limit_amount={
        "currency": RLUSD_CURRENCY,
        "issuer": RLUSD_ISSUER,
        "value": TRUST_LIMIT
    }
)

# 5. Autofill (adds fee, sequence) and sign the transaction
signed_tx = safe_sign_and_autofill_transaction(trust_set_tx, test_wallet, client)

# 6. Submit the transaction to the network and wait for validation
response = send_reliable_submission(signed_tx, client)

# 7. Output the result
print("TrustSet Transaction Result:")
print(response.result)