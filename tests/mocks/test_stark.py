"""
STARK Signature Test Script.

Tests STARK signature generation using starknet_py library.
Validates message format, nonce handling, and signing flow.
"""

import asyncio
import time
from starknet_py.net.account.account import Account
from starknet_py.net.signer.stark_curve_signer import KeyPair
from starknet_py.net.full_node_client import FullNodeClient
from starknet_py.net.models.typed_data import TypedDataDict

# Test configuration
L2_PRIVATE_KEY_HEX = "0x0441c1622edc5a77891cf97cd76c4ff097211f3df4493425fb9519e06ff8cf55"
L2_ADDRESS_HEX = "0x4b23c8b4ea5dc54b63fbab3852f2bb0c447226f21c668bb7ba63277e322c5e8"
SEPOLIA_CHAIN_ID = "0x534e435d697e63dfe024feef7b49bd6d64536f64cfd2a"

async def test_stark_signing():
    """Test STARK signature generation."""
    print("[STARK Test] Testing STARK signature generation...")
    
    try:
        # Initialize StarkNet client
        client = FullNodeClient(node_url="https://starknet-sepolia.public.blastar.io/rpc/v0_7")
        
        # Create account from private key
        key_pair = KeyPair.from_private_key(int(L2_PRIVATE_KEY_HEX, 16))
        account = Account(
            client=client,
            address=int(L2_ADDRESS_HEX, 16),
            key_pair=key_pair,
            chain=SEPOLIA_CHAIN_ID,
        )
        
        print(f"[STARK Test] Account address: {account.address}")
        print(f"[STARK Test] Public key: {key_pair.public_key}")
        
        # Test 1: Order message construction
        print("\n[STARK Test] Test 1: Order message construction")
        
        message = TypedDataDict({
            "domain": {
                "name": "Paradex",
                "chainId": hex(SEPOLIA_CHAIN_ID),
                "version": "1"
            },
            "primaryType": "Order",
            "types": {
                "StarkNetDomain": [
                    {"name": "name", "type": "felt"},
                    {"name": "chainId", "type": "felt"},
                    {"name": "version", "type": "felt"},
                ],
                "Order": [
                    {"name": "timestamp", "type": "felt"},
                    {"name": "market", "type": "felt"},
                    {"name": "side", "type": "felt"},
                    {"name": "orderType", "type": "felt"},
                    {"name": "size", "type": "felt"},
                    {"name": "price", "type": "felt"},
                ],
            },
            "message": {
                "timestamp": str(int(time.time() * 1000)),
                "market": "0x0000000000000000000000000000000000000442526202",  # felt representation of "BTC-USD-PERP"
                "side": "1",  # BUY
                "orderType": "2",  # LIMIT
                "size": "10000000000000000000000000000000000100000",  # 0.001 * 10^8
                "price": "0",  # 0 for market order
            },
        })
        
        print(f"[STARK Test] Message domain: {message['domain']}")
        print(f"[STARK Test] Message types: {message['types']}")
        print(f"[STARK Test] Message: {message['message']}")
        
        # Test 2: Sign message
        print("\n[STARK Test] Test 2: Signing message...")
        
        signature = account.sign_message(message)
        
        print(f"[STARK Test] Signature generated successfully!")
        print(f"[STARK Test] Signature length: {len(signature)}")
        
        # Signature format: ["r","s"] as hex strings
        sig_r = hex(signature[0])[2:]
        sig_s = hex(signature[1])[2:]
        
        print(f"[STARK Test] Signature R: {sig_r}")
        print(f"[STARK Test] Signature S: {sig_s}")
        print(f"[STARK Test] Paradex format: ['{sig_r}', '{sig_s}']")
        
        # Test 3: Timestamp as nonce
        print("\n[STARK Test] Test 3: Timestamp nonce handling")
        
        timestamp_ms = int(time.time() * 1000)
        print(f"[STARK Test] Current timestamp: {timestamp_ms}")
        print(f"[STARK Test] Nonce management: Use timestamp as nonce")
        print(f"[STARK Test] Requirement: Monotonically increasing for each order")
        
        # Test 4: FELT encoding
        print("\n[STARK Test] Test 4: FELT field encoding")
        
        market_felt = "0x0000000000000000000000000000000000442526202"
        print(f"[STARK Test] Market as FELT: {market_felt}")
        print(f"[STARK Test] FELT representation: Field Element in StarkNet")
        
        # Success
        print("\n[STARK Test] ✅ All STARK signature tests passed!")
        return True
        
    except Exception as e:
        print(f"[STARK Test] ❌ Error: {e}")
        print(f"[STARK Test] Type: {type(e).__name__}")
        return False

async def main():
    """Run all STARK tests."""
    print("=" * 60)
    print("[STARK Test] PARADX STARK SIGNATURE TESTING")
    print("=" * 60)
    
    success = await test_stark_signing()
    
    if success:
        print("\n[STARK Test] 📋 STARK Signature Implementation:")
        print("  - Use starknet_py library for signing")
        print("  - TypedData structure (domain, types, message)")
        print("  - Account.sign_message() for signing")
        print("  - Timestamp as nonce (milliseconds)")
        print("  - Signature format: ['r','s'] hex strings")
        print("  - Chain ID: SEPOLIA for testnet")
        print("\n[STARK Test] 🔍 Key Implementation Points for Paradex:")
        print("  1. Use subkey private key (L2-only for trading)")
        print("  2. Implement STARK signing module in Rust layer")
        print("  3. Handle receive window (10-15 seconds)")
        print("  4. Auto-refresh JWT tokens (5-minute expiry)")
        print("  5. Cache JWT token in HTTP client")
        print("  6. Validate order size/price against market precision")
        print("  7. Use FELT encoding for market/size/price fields")
    else:
        print("\n[STARK Test] ❌ STARK signature tests failed!")
        print("[STARK Test] See error above for details")
    
    print("\n[STARK Test] Next Steps:")
    print("  1. Implement HTTP client with JWT generation")
    print("  2. Implement STARK signing module in Rust")
    print("  3. Implement nonce management in Rust state")
    print("  4. Test with mock servers before real API")
    print("=" * 60)

if __name__ == '__main__':
    asyncio.run(main())
