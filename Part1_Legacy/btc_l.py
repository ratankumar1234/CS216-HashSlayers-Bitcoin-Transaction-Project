
import requests
import json

# --- Configuration ---
RPC_USER = "iitstudent"
RPC_PASS = "securepassword123"
RPC_PORT = 18443
WALLET_NAME = "assignment_wallet"

RPC_URL = f"http://{RPC_USER}:{RPC_PASS}@127.0.0.1:{RPC_PORT}/wallet/testwallet"
FEE = 0.0001


def rpc(method, params=None):
    if params is None:
        params = []
    payload = {
        "jsonrpc": "1.0",
        "id": "assignment",
        "method": method,
        "params": params
    }
    response = requests.post(RPC_URL, json=payload)
    result = response.json()
    if result.get("error"):
        print(f"RPC Error in {method}: {result['error']}")
        return None
    return result["result"]


def rpc_node(method, params=None):
    if params is None:
        params = []
    url = f"http://{RPC_USER}:{RPC_PASS}@127.0.0.1:{RPC_PORT}"
    payload = {
        "jsonrpc": "1.0",
        "id": "assignment",
        "method": method,
        "params": params
    }
    response = requests.post(url, json=payload)
    result = response.json()
    if result.get("error"):
        return None
    return result["result"]


def main():
    print("\n--- PART 1 : Wallet Setup ---")
    wallet_name = WALLET_NAME
    wallets = rpc_node("listwallets")

    if wallet_name not in wallets:
        rpc_node("createwallet", [wallet_name])
        print("Wallet created")
    else:
        print("Wallet already loaded")

    # Generate Legacy addresses
    addr_A = rpc("getnewaddress", ["A", "legacy"])
    addr_B = rpc("getnewaddress", ["B", "legacy"])
    addr_C = rpc("getnewaddress", ["C", "legacy"])

    print("\nAddresses Generated (Legacy P2PKH)")
    print("Address A:", addr_A)
    print("Address B:", addr_B)
    print("Address C:", addr_C)

    miner_addr = rpc("getnewaddress", ["Miner", "legacy"])
    print("\nMining 101 blocks...")
    rpc("generatetoaddress", [101, miner_addr])

    print("\nFunding Address A")
    fund_txid = rpc("sendtoaddress", [addr_A, 2.0])
    rpc("generatetoaddress", [1, miner_addr])
    print("Funding TXID:", fund_txid)


    print("\n--- PART 2 : Transaction A → B ---")
    unspent = rpc("listunspent", [1, 9999999, [addr_A]])
    if not unspent:
        print("No UTXO found for A")
        return
    utxo = unspent[0]

    inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]}]
    outputs = {addr_B: utxo["amount"] - FEE}
    
    raw_tx = rpc("createrawtransaction", [inputs, outputs])
    
    # Extract Challenge Script (ScriptPubKey) from raw tx
    decoded = rpc("decoderawtransaction", [raw_tx])
    scriptPubKey_asm = decoded["vout"][0]["scriptPubKey"]["asm"]
    scriptPubKey_hex = decoded["vout"][0]["scriptPubKey"]["hex"]
    
    # Calculate ScriptPubKey metrics
    spk_bytes = len(scriptPubKey_hex) // 2
    spk_weight = spk_bytes * 4
    spk_vbytes = spk_bytes

    signed_tx = rpc("signrawtransactionwithwallet", [raw_tx])
    
    # Extract FULL Transaction metrics from signed tx
    decoded_signed_AB = rpc("decoderawtransaction", [signed_tx["hex"]])
    size_AB = decoded_signed_AB["size"]
    vsize_AB = decoded_signed_AB["vsize"]
    weight_AB = decoded_signed_AB["weight"]

    txid_AB = rpc("sendrawtransaction", [signed_tx["hex"]])
    rpc("generatetoaddress", [1, miner_addr])
    print("Transaction A→B TXID:", txid_AB)


    print("\n--- PART 3 : Transaction B → C ---")
    unspent_B = rpc("listunspent", [1, 9999999, [addr_B]])
    utxo_B = next((u for u in unspent_B if u["txid"] == txid_AB), None)

    if utxo_B is None:
        print("No UTXO found for B")
        return

    inputs_B = [{"txid": utxo_B["txid"], "vout": utxo_B["vout"]}]
    outputs_B = {addr_C: utxo_B["amount"] - FEE}
    
    raw_tx_BC = rpc("createrawtransaction", [inputs_B, outputs_B])
    signed_BC = rpc("signrawtransactionwithwallet", [raw_tx_BC])
    
    # Extract Response Script (ScriptSig) and FULL Tx metrics
    decoded_BC = rpc("decoderawtransaction", [signed_BC["hex"]])
    
    scriptSig_asm = decoded_BC["vin"][0]["scriptSig"]["asm"]
    scriptSig_hex = decoded_BC["vin"][0]["scriptSig"]["hex"]
    
    # Calculate ScriptSig metrics
    ssig_bytes = len(scriptSig_hex) // 2
    ssig_weight = ssig_bytes * 4
    ssig_vbytes = ssig_bytes
    
    size_BC = decoded_BC["size"]
    vsize_BC = decoded_BC["vsize"]
    weight_BC = decoded_BC["weight"]

    txid_BC = rpc("sendrawtransaction", [signed_BC["hex"]])
    rpc("generatetoaddress", [1, miner_addr])
    print("Transaction B→C TXID:", txid_BC)


    print("\n=========================================================")
    print("   ASSIGNMENT DATA REPORT: P2PKH (LEGACY) REQUIREMENTS   ")
    print("=========================================================")
    
    print("\n1. Check the size of P2PKH transactions (Part 1):")
    print("---------------------------------------------------------")
    print(f"Transaction A→B (Funding B):")
    print(f"  - Size:   {size_AB} bytes")
    print(f"  - Weight: {weight_AB}")
    print(f"  - Vsize:  {vsize_AB} vbytes")
    
    print(f"\nTransaction B→C (Spending from B):")
    print(f"  - Size:   {size_BC} bytes")
    print(f"  - Weight: {weight_BC}")
    print(f"  - Vsize:  {vsize_BC} vbytes")
    print("  * Note: In legacy transactions, Size and Vsize are identical.")

    print("\n2. P2PKH Script Structures and Sizes (Challenge/Response):")
    print("---------------------------------------------------------")
    print("Challenge Script (ScriptPubKey on Output to B):")
    print(f"  - ASM:    {scriptPubKey_asm}")
    print(f"  - Size:   {spk_bytes} bytes")
    print(f"  - Weight: {spk_weight}")
    print(f"  - Vsize:  {spk_vbytes} vbytes")

    print("\nResponse Script (ScriptSig on Input from B):")
    print(f"  - ASM:    {scriptSig_asm}")
    print(f"  - Size:   {ssig_bytes} bytes")
    print(f"  - Weight: {ssig_weight}")
    print(f"  - Vsize:  {ssig_vbytes} vbytes")
    print("=========================================================\n")


if __name__ == "__main__":
    main()
