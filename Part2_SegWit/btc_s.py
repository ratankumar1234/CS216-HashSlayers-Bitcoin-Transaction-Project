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
    if params is None: params = []
    payload = {"jsonrpc": "1.0", "id": "assignment", "method": method, "params": params}
    response = requests.post(RPC_URL, json=payload)
    result = response.json()
    if result.get("error"):
        print(f"RPC Error in {method}: {result['error']}")
        return None
    return result["result"]

def rpc_node(method, params=None):
    if params is None: params = []
    url = f"http://{RPC_USER}:{RPC_PASS}@127.0.0.1:{RPC_PORT}"
    payload = {"jsonrpc": "1.0", "id": "assignment", "method": method, "params": params}
    response = requests.post(url, json=payload)
    result = response.json()
    if result.get("error"): return None
    return result["result"]

def main():
    print("\n--- PART 1 : Wallet Setup (SegWit) ---")
    wallet_name = WALLET_NAME
    wallets = rpc_node("listwallets")

    if wallet_name not in wallets:
        rpc_node("createwallet", [wallet_name])
    
    # Generate P2SH-SegWit addresses (A', B', C')
    addr_A = rpc("getnewaddress", ["A_SegWit", "p2sh-segwit"])
    addr_B = rpc("getnewaddress", ["B_SegWit", "p2sh-segwit"])
    addr_C = rpc("getnewaddress", ["C_SegWit", "p2sh-segwit"])

    print("\nAddresses Generated (P2SH-P2WPKH)")
    print("Address A':", addr_A)
    print("Address B':", addr_B)
    print("Address C':", addr_C)

    miner_addr = rpc("getnewaddress", ["Miner_SegWit", "legacy"])
    print("\nMining 101 blocks...")
    rpc("generatetoaddress", [101, miner_addr])

    print("\nFunding Address A'")
    fund_txid = rpc("sendtoaddress", [addr_A, 2.0])
    rpc("generatetoaddress", [1, miner_addr])
    print("Funding TXID:", fund_txid)


    print("\n--- PART 2 : Transaction A' → B' ---")
    unspent = rpc("listunspent", [1, 9999999, [addr_A]])
    if not unspent:
        print("No UTXO found for A'")
        return
    utxo = unspent[0]

    inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]}]
    outputs = {addr_B: utxo["amount"] - FEE}
    
    raw_tx = rpc("createrawtransaction", [inputs, outputs])
    
    # Extract Challenge Script (ScriptPubKey) for B'
    decoded = rpc("decoderawtransaction", [raw_tx])
    scriptPubKey_asm = decoded["vout"][0]["scriptPubKey"]["asm"]
    scriptPubKey_hex = decoded["vout"][0]["scriptPubKey"]["hex"]
    
    spk_bytes = len(scriptPubKey_hex) // 2
    spk_weight = spk_bytes * 4
    spk_vbytes = spk_bytes

    signed_tx = rpc("signrawtransactionwithwallet", [raw_tx])
    
    # Extract FULL Transaction metrics
    decoded_signed_AB = rpc("decoderawtransaction", [signed_tx["hex"]])
    size_AB = decoded_signed_AB["size"]
    vsize_AB = decoded_signed_AB["vsize"]
    weight_AB = decoded_signed_AB["weight"]

    txid_AB = rpc("sendrawtransaction", [signed_tx["hex"]])
    rpc("generatetoaddress", [1, miner_addr])
    print("Transaction A'→B' TXID:", txid_AB)


    print("\n--- PART 3 : Transaction B' → C' ---")
    unspent_B = rpc("listunspent", [1, 9999999, [addr_B]])
    utxo_B = next((u for u in unspent_B if u["txid"] == txid_AB), None)

    if utxo_B is None:
        print("No UTXO found for B'")
        return

    inputs_B = [{"txid": utxo_B["txid"], "vout": utxo_B["vout"]}]
    outputs_B = {addr_C: utxo_B["amount"] - FEE}
    
    raw_tx_BC = rpc("createrawtransaction", [inputs_B, outputs_B])
    signed_BC = rpc("signrawtransactionwithwallet", [raw_tx_BC])
    
    # Extract Response Script (ScriptSig + Witness)
    decoded_BC = rpc("decoderawtransaction", [signed_BC["hex"]])
    
    scriptSig_asm = decoded_BC["vin"][0]["scriptSig"]["asm"]
    scriptSig_hex = decoded_BC["vin"][0]["scriptSig"]["hex"]
    
    # SegWit specific: extract witness data
    witness_data = decoded_BC["vin"][0].get("txinwitness", [])
    witness_bytes = sum(len(w) // 2 for w in witness_data)
    
    ssig_bytes = len(scriptSig_hex) // 2
    
    # In SegWit, ScriptSig has 4x weight, Witness has 1x weight
    ssig_weight = ssig_bytes * 4
    witness_weight = witness_bytes * 1
    total_input_weight = ssig_weight + witness_weight
    
    size_BC = decoded_BC["size"]
    vsize_BC = decoded_BC["vsize"]
    weight_BC = decoded_BC["weight"]

    txid_BC = rpc("sendrawtransaction", [signed_BC["hex"]])
    rpc("generatetoaddress", [1, miner_addr])
    print("Transaction B'→C' TXID:", txid_BC)


    print("\n=========================================================")
    print("   ASSIGNMENT DATA REPORT: P2SH-SEGWIT REQUIREMENTS      ")
    print("=========================================================")
    
    print("\n1. Check the size of P2SH-P2WPKH transactions (Part 2):")
    print("---------------------------------------------------------")
    print(f"Transaction A'→B' (Funding B'):")
    print(f"  - Size:   {size_AB} bytes")
    print(f"  - Weight: {weight_AB}")
    print(f"  - Vsize:  {vsize_AB} vbytes")
    
    print(f"\nTransaction B'→C' (Spending from B'):")
    print(f"  - Size:   {size_BC} bytes")
    print(f"  - Weight: {weight_BC}")
    print(f"  - Vsize:  {vsize_BC} vbytes")
    print("  * Note: In SegWit transactions, Vsize is notably smaller than Size.")

    print("\n2. P2SH-SegWit Script Structures and Sizes:")
    print("---------------------------------------------------------")
    print("Challenge Script (ScriptPubKey on Output to B'):")
    print(f"  - ASM:    {scriptPubKey_asm}")
    print(f"  - Size:   {spk_bytes} bytes")
    print(f"  - Structure: OP_HASH160 <20-byte-hash> OP_EQUAL (P2SH format)")

    print("\nResponse Scripts (Spending from B'):")
    print(f"  - ScriptSig ASM: {scriptSig_asm}")
    print(f"    -> ScriptSig Size: {ssig_bytes} bytes | Weight: {ssig_weight}")
    print(f"  - Witness Data:  {witness_data}")
    print(f"    -> Witness Size: {witness_bytes} bytes | Weight: {witness_weight}")
    print(f"  - Total Input Weight: {total_input_weight}")
    print("=========================================================\n")

if __name__ == "__main__":
    main()
