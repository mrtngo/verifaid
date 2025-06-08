# import streamlit as st
# from xrpl.clients import JsonRpcClient
# from xrpl.models.requests import AccountTx
# import json

# # XRPL Testnet Node
# client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

# st.set_page_config("XRPL Wallet Explorer", layout="centered")
# st.title("📡 XRPL Wallet Explorer (Enhanced Debug)")

# wallet = st.text_input("Enter XRPL wallet address (Testnet):")

# # Debug options
# debug_mode = st.checkbox("Enable Debug Mode", value=True)
# show_raw_response = st.checkbox("Show Complete Raw Response")

# if wallet:
#     try:
#         resp = client.request(AccountTx(account=wallet, limit=10))  # Reduced for debugging
        
#         # Show the complete raw response structure
#         if show_raw_response:
#             st.subheader("🔍 Complete Raw API Response")
#             st.json(resp.result)
#             st.write("---")
        
#         # Check if we got any data
#         if not hasattr(resp, 'result') or not resp.result:
#             st.error("No result data from API")
#             st.stop()
        
#         st.write(f"**API Response Keys:** {list(resp.result.keys())}")
        
#         txs = resp.result.get("transactions", [])
        
#         if not txs:
#             st.warning("No transactions found in the response.")
#             st.write(f"**Available keys in result:** {list(resp.result.keys())}")
#             st.stop()
        
#         st.write(f"**Found {len(txs)} transactions**")
        
#         # Deep inspection of first transaction
#         if debug_mode and len(txs) > 0:
#             st.subheader("🔍 Deep Analysis of First Transaction")
#             first_tx = txs[0]
            
#             st.write(f"**First transaction type:** {type(first_tx)}")
#             st.write(f"**First transaction keys:** {list(first_tx.keys()) if isinstance(first_tx, dict) else 'Not a dict'}")
            
#             # Show the complete first transaction
#             st.json(first_tx)
            
#             # Try to access data in different ways
#             st.write("**Trying different access patterns:**")
            
#             # Pattern 1: Direct access
#             if isinstance(first_tx, dict):
#                 tx_type_direct = first_tx.get("TransactionType")
#                 amount_direct = first_tx.get("Amount")
#                 hash_direct = first_tx.get("hash")
#                 st.write(f"- Direct access: Type={tx_type_direct}, Amount={amount_direct}, Hash={hash_direct}")
                
#                 # Pattern 2: Through 'tx' key
#                 if "tx" in first_tx:
#                     tx_data = first_tx["tx"]
#                     tx_type_nested = tx_data.get("TransactionType") if isinstance(tx_data, dict) else None
#                     amount_nested = tx_data.get("Amount") if isinstance(tx_data, dict) else None
#                     hash_nested = tx_data.get("hash") if isinstance(tx_data, dict) else None
#                     st.write(f"- Via 'tx' key: Type={tx_type_nested}, Amount={amount_nested}, Hash={hash_nested}")
                
#                 # Pattern 3: Through 'transaction' key
#                 if "transaction" in first_tx:
#                     tx_data = first_tx["transaction"]
#                     tx_type_tx = tx_data.get("TransactionType") if isinstance(tx_data, dict) else None
#                     amount_tx = tx_data.get("Amount") if isinstance(tx_data, dict) else None
#                     hash_tx = tx_data.get("hash") if isinstance(tx_data, dict) else None
#                     st.write(f"- Via 'transaction' key: Type={tx_type_tx}, Amount={amount_tx}, Hash={hash_tx}")
                
#                 # Look for all fields that might contain transaction type
#                 type_fields = []
#                 amount_fields = []
#                 hash_fields = []
                
#                 def find_fields(obj, prefix=""):
#                     if isinstance(obj, dict):
#                         for key, value in obj.items():
#                             full_key = f"{prefix}.{key}" if prefix else key
#                             if "type" in key.lower() or "transaction" in key.lower():
#                                 type_fields.append(f"{full_key}: {value}")
#                             if "amount" in key.lower():
#                                 amount_fields.append(f"{full_key}: {value}")
#                             if "hash" in key.lower():
#                                 hash_fields.append(f"{full_key}: {value}")
#                             if isinstance(value, dict):
#                                 find_fields(value, full_key)
                
#                 find_fields(first_tx)
                
#                 if type_fields:
#                     st.write(f"**All type-related fields found:** {type_fields}")
#                 if amount_fields:
#                     st.write(f"**All amount-related fields found:** {amount_fields}")
#                 if hash_fields:
#                     st.write(f"**All hash-related fields found:** {hash_fields}")
        
#         # Now try to process all transactions with what we learned
#         results = []
#         total_sent = 0
#         total_received = 0
        
#         for i, entry in enumerate(txs):
#             # Initialize default values
#             tx_type = "Unknown"
#             tx_hash = "—"
#             direction = "-"
#             counterparty = "-"
#             amount = None
#             memo = ""
#             result = "N/A"
            
#             # Extract data based on the discovered structure
#             tx_json = None
#             meta_data = None
            
#             if isinstance(entry, dict):
#                 # The transaction data is in tx_json
#                 tx_json = entry.get("tx_json", {})
#                 meta_data = entry.get("meta", {})
                
#                 # Get the hash from the top level
#                 tx_hash = entry.get("hash", "—")
            
#             # Extract transaction info from tx_json
#             if tx_json and isinstance(tx_json, dict):
#                 tx_type = tx_json.get("TransactionType", "Unknown")
                
#                 # Get account info for direction calculation
#                 tx_account = tx_json.get("Account", "")
#                 tx_destination = tx_json.get("Destination", "")
                
#                 # Handle Payment transactions
#                 if tx_type == "Payment":
#                     # First try to get amount from meta.delivered_amount
#                     amt = None
#                     if isinstance(meta_data, dict):
#                         delivered_amt = meta_data.get("delivered_amount")
#                         if delivered_amt:
#                             amt = delivered_amt
                    
#                     # Fallback to tx_json.Amount
#                     if not amt:
#                         amt = tx_json.get("Amount")
                    
#                     if isinstance(amt, str) and amt.isdigit():
#                         try:
#                             xrp = int(amt) / 1_000_000
#                             amount = round(xrp, 6)
                            
#                             # Determine direction
#                             if tx_destination == wallet:
#                                 direction = "IN"
#                                 counterparty = tx_account
#                                 total_received += xrp
#                             elif tx_account == wallet:
#                                 direction = "OUT"
#                                 counterparty = tx_destination
#                                 total_sent += xrp
#                         except Exception as e:
#                             amount = f"Parse Error: {e}"
#                     elif isinstance(amt, dict):
#                         direction = "Token Payment"
#                         amount = f"{amt.get('value', '?')} {amt.get('currency', '?')}"
#                 elif tx_type == "OfferCreate":
#                     direction = "Offer Created"
#                     taker_gets = tx_json.get("TakerGets")
#                     if isinstance(taker_gets, str) and taker_gets.isdigit():
#                         xrp = int(taker_gets) / 1_000_000
#                         amount = f"Offer: {xrp:.6f} XRP"
#                 elif tx_type in ["TrustSet", "AccountSet", "SetRegularKey"]:
#                     direction = "Account Setup"
            
#             # Extract result from meta
#             if isinstance(meta_data, dict):
#                 result = meta_data.get("TransactionResult", "N/A")
            
#             results.append({
#                 "Type": tx_type,
#                 "Direction": direction,
#                 "Amount (XRP)": amount if amount is not None else "-",
#                 "Counterparty": counterparty if counterparty else "-",
#                 "Memo": memo if memo else "-",
#                 "Hash": tx_hash,
#                 "Result": result
#             })
            
#             # Debug output for first few transactions
#             if debug_mode and i < 3:
#                 st.write(f"**Transaction {i+1} processed:**")
#                 st.write(f"- Type: {tx_type} (from tx_json.TransactionType)")
#                 st.write(f"- Hash: {tx_hash} (from entry.hash)")
#                 st.write(f"- Amount: {amount} (from meta.delivered_amount or tx_json.Amount)")
#                 st.write(f"- Direction: {direction}")
#                 st.write(f"- Account: {tx_account}")
#                 st.write(f"- Destination: {tx_destination}")
#                 st.write("---")
        
#         # Display summary metrics
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("📥 Total XRP Received", f"{total_received:.6f}")
#         with col2:
#             st.metric("📤 Total XRP Sent", f"{total_sent:.6f}")
        
#         # Display results
#         if results:
#             st.subheader("Transaction History")
#             st.dataframe(results, use_container_width=True)
#         else:
#             st.info("No transactions could be processed.")
            
#     except Exception as e:
#         st.error(f"❌ Error fetching transactions: {e}")
        
#         # Show detailed error
#         import traceback
#         st.code(traceback.format_exc())

import streamlit as st
from xrpl.clients import JsonRpcClient
from xrpl.models.requests import AccountTx
import json

# XRPL Testnet Node
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

st.set_page_config("XRPL Wallet Explorer", layout="centered")
st.title("📡 XRPL Wallet Explorer (Enhanced Debug)")

wallet = st.text_input("Enter XRPL wallet address (Testnet):")

# Debug options
debug_mode = st.checkbox("Enable Debug Mode", value=True)
show_raw_response = st.checkbox("Show Complete Raw Response")

if wallet:
    try:
        resp = client.request(AccountTx(account=wallet, limit=10))  # Reduced for debugging
        
        # Show the complete raw response structure
        if show_raw_response:
            st.subheader("🔍 Complete Raw API Response")
            st.json(resp.result)
            st.write("---")
        
        # Check if we got any data
        if not hasattr(resp, 'result') or not resp.result:
            st.error("No result data from API")
            st.stop()
        
        st.write(f"**API Response Keys:** {list(resp.result.keys())}")
        
        txs = resp.result.get("transactions", [])
        
        if not txs:
            st.warning("No transactions found in the response.")
            st.write(f"**Available keys in result:** {list(resp.result.keys())}")
            st.stop()
        
        st.write(f"**Found {len(txs)} transactions**")
        
        # Deep inspection of first transaction
        if debug_mode and len(txs) > 0:
            st.subheader("🔍 Deep Analysis of First Transaction")
            first_tx = txs[0]
            
            st.write(f"**First transaction type:** {type(first_tx)}")
            st.write(f"**First transaction keys:** {list(first_tx.keys()) if isinstance(first_tx, dict) else 'Not a dict'}")
            
            # Show the complete first transaction
            st.json(first_tx)
            
            # Try to access data in different ways
            st.write("**Trying different access patterns:**")
            
            # Pattern 1: Direct access
            if isinstance(first_tx, dict):
                tx_type_direct = first_tx.get("TransactionType")
                amount_direct = first_tx.get("Amount")
                hash_direct = first_tx.get("hash")
                st.write(f"- Direct access: Type={tx_type_direct}, Amount={amount_direct}, Hash={hash_direct}")
                
                # Pattern 2: Through 'tx' key
                if "tx" in first_tx:
                    tx_data = first_tx["tx"]
                    tx_type_nested = tx_data.get("TransactionType") if isinstance(tx_data, dict) else None
                    amount_nested = tx_data.get("Amount") if isinstance(tx_data, dict) else None
                    hash_nested = tx_data.get("hash") if isinstance(tx_data, dict) else None
                    st.write(f"- Via 'tx' key: Type={tx_type_nested}, Amount={amount_nested}, Hash={hash_nested}")
                
                # Pattern 3: Through 'transaction' key
                if "transaction" in first_tx:
                    tx_data = first_tx["transaction"]
                    tx_type_tx = tx_data.get("TransactionType") if isinstance(tx_data, dict) else None
                    amount_tx = tx_data.get("Amount") if isinstance(tx_data, dict) else None
                    hash_tx = tx_data.get("hash") if isinstance(tx_data, dict) else None
                    st.write(f"- Via 'transaction' key: Type={tx_type_tx}, Amount={amount_tx}, Hash={hash_tx}")
                
                # Look for all fields that might contain transaction type
                type_fields = []
                amount_fields = []
                hash_fields = []
                
                def find_fields(obj, prefix=""):
                    if isinstance(obj, dict):
                        for key, value in obj.items():
                            full_key = f"{prefix}.{key}" if prefix else key
                            if "type" in key.lower() or "transaction" in key.lower():
                                type_fields.append(f"{full_key}: {value}")
                            if "amount" in key.lower():
                                amount_fields.append(f"{full_key}: {value}")
                            if "hash" in key.lower():
                                hash_fields.append(f"{full_key}: {value}")
                            if isinstance(value, dict):
                                find_fields(value, full_key)
                
                find_fields(first_tx)
                
                if type_fields:
                    st.write(f"**All type-related fields found:** {type_fields}")
                if amount_fields:
                    st.write(f"**All amount-related fields found:** {amount_fields}")
                if hash_fields:
                    st.write(f"**All hash-related fields found:** {hash_fields}")
        
        # Now try to process all transactions with what we learned
        results = []
        total_sent = 0
        total_received = 0
        
        for i, entry in enumerate(txs):
            # Initialize default values
            tx_type = "Unknown"
            tx_hash = "—"
            direction = "-"
            counterparty = "-"
            amount = None
            memo = ""
            result = "N/A"
            
            # Extract data based on the discovered structure
            tx_json = None
            meta_data = None
            
            if isinstance(entry, dict):
                # The transaction data is in tx_json
                tx_json = entry.get("tx_json", {})
                meta_data = entry.get("meta", {})
                
                # Get the hash from the top level
                tx_hash = entry.get("hash", "—")
            
            # Extract transaction info from tx_json
            if tx_json and isinstance(tx_json, dict):
                tx_type = tx_json.get("TransactionType", "Unknown")
                
                # Get account info for direction calculation
                tx_account = tx_json.get("Account", "")
                tx_destination = tx_json.get("Destination", "")
                
                # Handle Payment transactions
                if tx_type == "Payment":
                    # First try to get amount from meta.delivered_amount
                    amt = None
                    if isinstance(meta_data, dict):
                        delivered_amt = meta_data.get("delivered_amount")
                        if delivered_amt:
                            amt = delivered_amt
                    
                    # Fallback to tx_json.Amount
                    if not amt:
                        amt = tx_json.get("Amount")
                    
                    if isinstance(amt, str) and amt.isdigit():
                        try:
                            xrp = int(amt) / 1_000_000
                            amount = round(xrp, 6)
                            
                            # Determine direction
                            if tx_destination == wallet:
                                direction = "IN"
                                counterparty = tx_account
                                total_received += xrp
                            elif tx_account == wallet:
                                direction = "OUT"
                                counterparty = tx_destination
                                total_sent += xrp
                        except Exception as e:
                            amount = f"Parse Error: {e}"
                    elif isinstance(amt, dict):
                        direction = "Token Payment"
                        amount = f"{amt.get('value', '?')} {amt.get('currency', '?')}"
                elif tx_type == "OfferCreate":
                    direction = "Offer Created"
                    taker_gets = tx_json.get("TakerGets")
                    if isinstance(taker_gets, str) and taker_gets.isdigit():
                        xrp = int(taker_gets) / 1_000_000
                        amount = f"Offer: {xrp:.6f} XRP"
                elif tx_type in ["TrustSet", "AccountSet", "SetRegularKey"]:
                    direction = "Account Setup"
            
            # Extract result from meta
            if isinstance(meta_data, dict):
                result = meta_data.get("TransactionResult", "N/A")
            
            results.append({
                "Type": tx_type,
                "Direction": direction,
                "Amount (XRP)": str(amount) if amount is not None else "-",
                "Counterparty": counterparty if counterparty else "-",
                "Memo": memo if memo else "-",
                "Hash": tx_hash,
                "Result": result
            })
            
            # Debug output for first few transactions
            if debug_mode and i < 3:
                st.write(f"**Transaction {i+1} processed:**")
                st.write(f"- Type: {tx_type} (from tx_json.TransactionType)")
                st.write(f"- Hash: {tx_hash} (from entry.hash)")
                st.write(f"- Amount: {amount} (from meta.delivered_amount or tx_json.Amount)")
                st.write(f"- Direction: {direction}")
                st.write(f"- Account: {tx_account}")
                st.write(f"- Destination: {tx_destination}")
                st.write("---")
        
        # Display summary metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric("📥 Total XRP Received", f"{total_received:.6f}")
        with col2:
            st.metric("📤 Total XRP Sent", f"{total_sent:.6f}")
        
        # Display results
        if results:
            st.subheader("Transaction History")
            st.dataframe(results, use_container_width=True)
        else:
            st.info("No transactions could be processed.")
            
    except Exception as e:
        st.error(f"❌ Error fetching transactions: {e}")
        
        # Show detailed error
        import traceback
        st.code(traceback.format_exc())