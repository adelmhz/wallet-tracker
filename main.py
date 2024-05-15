from solana.rpc.api import Client
from solders.pubkey import Pubkey

def track_transactions(wallet_address):
    # Initialize Solana RPC client
    rpc_client = Client("https://api.mainnet-beta.solana.com")

    # Convert the wallet address to Pubkey object
    wallet_pubkey = Pubkey.from_string(wallet_address)

    # Get recent transactions involving the wallet address
    transactions_resp = rpc_client.get_signatures_for_address(wallet_pubkey, limit=10)

    # Iterate through transactions
    for tx in transactions_resp.value:
        signature = tx.signature
        # Get transaction details
        transaction_info = rpc_client.get_confirmed_transaction2(signature)
        if transaction_info is not None:
            transaction = transaction_info["transaction"]["message"]["instructions"]
            
            # Check if the wallet is involved in this transaction
            involved = False
            for instruction in transaction:
                if instruction["programId"] == "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA" and wallet_pubkey.to_base58() in [key["pubkey"] for key in instruction["keys"]]:
                    involved = True
                    break
            
            # If wallet is involved, print transaction details
            if involved:
                print("Transaction ID:", signature)
                print("Block number:", transaction_info["slot"])
                print("Transaction Fee:", transaction_info["meta"]["fee"])
                print("Instructions:")
                for instruction in transaction:
                    print(instruction)
                print("---------------------------------------")

# Replace "YOUR_WALLET_ADDRESS" with the wallet address you want to track
track_transactions("CWaVauLM2CwFUCxcQUyVYFuQe5s23YpQtAchFHU7CoAT")
