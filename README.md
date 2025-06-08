# XRPL NGO Management System

A command-line interface for managing Non-Governmental Organizations (NGOs) on the XRPL (XRP Ledger) testnet. This system enables NGO registration, donation management, payroll processing, and expense tracking using blockchain technology.

## Features

### 🏢 NGO Management
- **NGO Registration**: Create and register new NGOs with comprehensive metadata
- **Trustline Creation**: Automatic RLUSD trustline setup for registered NGOs
- **Organization Profiles**: Store location, staff count, focus areas, and supplier information

### 💰 Financial Operations
- **Donation Processing**: Accept XRP donations with custom memos
- **Payroll Management**: Batch process employee salary payments
- **Expense Tracking**: Upload receipts as NFTs to IPFS for transparency

### 🔗 Blockchain Integration
- **XRPL Testnet**: All transactions processed on XRP Ledger testnet
- **NFT Receipts**: Upload expense receipts to IPFS and mint as NFTs
- **Transaction Transparency**: All operations recorded on the blockchain

## Prerequisites

- Python 3.7+
- XRPL testnet wallet with test XRP
- Pinata account for IPFS uploads (for receipt functionality)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd xrpl-ngo-management
```

2. Install required dependencies:
```bash
pip install xrpl-py requests
```

3. Set up environment variables (optional for receipt uploads):
```bash
export PINATA_API_KEY="your_pinata_api_key"
export PINATA_SECRET_API_KEY="your_pinata_secret_key"
```

## Quick Start

1. Run the main application:
```bash
python main.py
```

2. Choose from the main menu options:
   - Create a new NGO
   - View existing NGOs
   - Donate to an NGO
   - Act as an NGO (manage operations)
   - Exit

## Usage Guide

### Creating an NGO

1. Select "Create a new NGO" from the main menu
2. Fill in the registration form:
   - Organization name and wallet address
   - Location information (country, city)
   - Staff details (count, monthly salaries)
   - Focus areas (multiple entries supported)
   - Supplier information
3. Provide your wallet seed for trustline creation
4. The system will create an RLUSD trustline with NGO metadata

### Making Donations

1. Select "Donate to an NGO" from the main menu
2. Provide:
   - Your donor wallet seed
   - Donation amount in XRP
   - Optional memo (project ID, donor info)
   - NGO's donation wallet address
3. Transaction will be processed and recorded on XRPL

### NGO Operations

When acting as an NGO, you can:

#### View Donations
- Check incoming donations and transaction history

#### Upload Expense Receipts
1. Provide your NGO wallet seed
2. Enter the file path to your receipt
3. Receipt is uploaded to IPFS via Pinata
4. An NFT is minted on XRPL with the IPFS URI

#### Process Payroll
1. Enter your NGO wallet seed
2. Add a memo for the payroll batch (e.g., "June Payroll")
3. Enter employee wallet addresses and amounts
4. Batch process all salary payments

## Configuration

### XRPL Settings
- **Testnet RPC**: `https://s.altnet.rippletest.net:51234`
- **RLUSD Issuer**: `rQhWct2fv4Vc4KRjRgMrxa8xPN9Zx9iLKV`
- **Trust Limit**: 1,000,000 RLUSD

### IPFS Integration
- **Provider**: Pinata Cloud
- **Endpoint**: `https://api.pinata.cloud/pinning/pinFileToIPFS`

## File Structure

```
xrpl-ngo-management/
├── main.py                 # Main CLI application
├── xrpl_txs/
│   ├── NGOCreation.py     # NGO registration logic
│   ├── donation.py        # Donation processing
│   ├── invoiceNft.py      # Receipt NFT minting
│   ├── payroll.py         # Salary payment processing
│   └── trustline.py       # RLUSD trustline management
└── README.md
```

## Transaction Types

### NGO Registration
- **Type**: TrustSet transaction
- **Memo**: NGO metadata (JSON format)
- **Purpose**: Create RLUSD trustline with organization data

### Donations
- **Type**: Payment transaction
- **Currency**: XRP
- **Memo**: Donation note/project ID

### Payroll
- **Type**: Payment transaction
- **Currency**: XRP
- **Memo**: Payroll batch identifier

### Expense Receipts
- **Type**: NFTokenMint transaction
- **URI**: IPFS hash of uploaded receipt
- **Purpose**: Transparent expense tracking

## Security Considerations

- **Testnet Only**: This system operates on XRPL testnet for development/testing
- **Seed Management**: Wallet seeds are entered manually; implement secure storage for production
- **Transaction Verification**: Always verify transaction hashes on XRPL explorer
- **File Security**: Receipt files are uploaded to public IPFS; ensure no sensitive data

## Development

### Adding New Features

1. Create new modules in the `xrpl_txs/` directory
2. Import and integrate in `main.py`
3. Follow existing patterns for XRPL client usage
4. Include proper error handling and user feedback

### Testing

- Use XRPL testnet for all transactions
- Obtain test XRP from the testnet faucet
- Verify all transactions on the testnet explorer

## Troubleshooting

### Common Issues

**Trustline Creation Fails**
- Ensure wallet has sufficient XRP for transaction fees
- Check if trustline already exists

**NFT Minting Fails**
- Verify Pinata API credentials
- Ensure file path is correct and accessible
- Check wallet has enough XRP for fees

**Payment Failures**
- Verify recipient wallet addresses
- Ensure sufficient balance for amount + fees
- Check network connectivity

### Transaction Explorer

All transactions can be viewed on the XRPL testnet explorer:
`https://testnet.xrpl.org/transactions/{transaction_hash}`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with proper error handling
4. Test thoroughly on XRPL testnet
5. Submit a pull request

## License

[Add your chosen license here]

## Support

For issues and questions:
- Check the troubleshooting section
- Review XRPL documentation: https://xrpl.org/
- Open an issue in the repository

---

**⚠️ Disclaimer**: This system is designed for XRPL testnet use only. Do not use with mainnet wallets or real funds without proper security audits and modifications.