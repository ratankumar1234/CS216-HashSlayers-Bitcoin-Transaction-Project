import requests
import json

# --- Configuration ---
RPC_USER = "iitstudent"
RPC_PASS = "securepassword123"
RPC_PORT = 18443
RPC_HOST = "172.19.48.1" # FIXED IP FOR WSL
WALLET_NAME = "testwallet"

RPC_URL = f"http://{RPC_USER}:{RPC_PASS}@{RPC_HOST}:{RPC_PORT}/wallet/{WALLET_NAME}"
NODE_URL = f"http://{RPC_USER}:{RPC_PASS}@{RPC_HOST}:{RPC_PORT}"
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
    payload = {"jsonrpc": "1.0", "id": "assignment", "method": method, "params": params}
    response = requests.post(NODE_URL, json=payload)
    result = response.json()
    if result.get("error"): return None
    return result["result"]

def main():
    print("\n--- PART 1 : Wallet Setup (SegWit) ---")
    wallets = rpc_node("listwallets")
    if WALLET_NAME not in wallets:
        rpc_node("createwallet", [WALLET_NAME])
    
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
    if not unspent: return
    utxo = unspent[0]

    inputs = [{"txid": utxo["txid"], "vout": utxo["vout"]}]
    outputs = {addr_B: utxo["amount"] - FEE}
    
    raw_tx = rpc("createrawtransaction", [inputs, outputs])
    decoded = rpc("decoderawtransaction", [raw_tx])
    scriptPubKey_asm = decoded["vout"][0]["scriptPubKey"]["asm"]
    scriptPubKey_hex = decoded["vout"][0]["scriptPubKey"]["hex"]
    
    signed_tx = rpc("signrawtransactionwithwallet", [raw_tx])
    decoded_signed_AB = rpc("decoderawtransaction", [signed_tx["hex"]])
    size_AB = decoded_signed_AB["size"]
    vsize_AB = decoded_signed_AB["vsize"]
    weight_AB = decoded_signed_AB["weight"]

    txid_AB = rpc("sendrawtransaction", [signed_tx["hex"]])
    rpc("generatetoaddress", [1, miner_addr])
    print("Transaction A'→B' TXID:", txid_AB)
    print("Signed TX Hex A'→B' (Copy for btcdeb):", signed_tx["hex"]) # ADDED FOR DEBUGGING

    print("\n--- PART 3 : Transaction B' → C' ---")
    unspent_B = rpc("listunspent", [1, 9999999, [addr_B]])
    utxo_B = next((u for u in unspent_B if u["txid"] == txid_AB), None)
    if utxo_B is None: return

    inputs_B = [{"txid": utxo_B["txid"], "vout": utxo_B["vout"]}]
    outputs_B = {addr_C: utxo_B["amount"] - FEE}
    
    raw_tx_BC = rpc("createrawtransaction", [inputs_B, outputs_B])
    signed_BC = rpc("signrawtransactionwithwallet", [raw_tx_BC])
    decoded_BC = rpc("decoderawtransaction", [signed_BC["hex"]])
    
    scriptSig_asm = decoded_BC["vin"][0]["scriptSig"]["asm"]
    scriptSig_hex = decoded_BC["vin"][0]["scriptSig"]["hex"]
    
    witness_data = decoded_BC["vin"][0].get("txinwitness", [])
    witness_bytes = sum(len(w) // 2 for w in witness_data)
    ssig_bytes = len(scriptSig_hex) // 2
    
    size_BC = decoded_BC["size"]
    vsize_BC = decoded_BC["vsize"]
    weight_BC = decoded_BC["weight"]

    txid_BC = rpc("sendrawtransaction", [signed_BC["hex"]])
    rpc("generatetoaddress", [1, miner_addr])
    print("Transaction B'→C' TXID:", txid_BC)
    print("Signed TX Hex B'→C' (Copy for btcdeb):", signed_BC["hex"]) # ADDED FOR DEBUGGING

    print("\n=== ASSIGNMENT DATA REPORT: P2SH-SEGWIT ===")
    print(f"Tx A'→B' | Size: {size_AB}, Weight: {weight_AB}, Vsize: {vsize_AB}")
    print(f"Tx B'→C' | Size: {size_BC}, Weight: {weight_BC}, Vsize: {vsize_BC}")
    print("Challenge Script ASM:", scriptPubKey_asm)
    print("Response Script ASM:", scriptSig_asm)
    print("Witness Data:", witness_data)

if __name__ == "__main__":
    main()
