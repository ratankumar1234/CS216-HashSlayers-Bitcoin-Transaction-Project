# ⚡ CS 216: Bitcoin Transaction Lab Assignment

**Team Name:** HashSlayers
**Repository:** [CS216-HashSlayers-Bitcoin-Transaction-Project](https://github.com/ratankumar1234/CS216-HashSlayers-Bitcoin-Transaction-Project)

---

# 👥 Team Members

| Name                       | Roll Number |
| :------------------------- | :---------- |
| **Raghav Sharma (Leader)** | 240001056   |
| **Abhishek Kumar Verma**   | 240001005   |
| **Ratan Kumar**            | 240001059   |
| **Rohan Chauhan**          | 240001061   |

---

# 🎯 Objective

The objective of this assignment is to **programmatically create and validate Bitcoin transactions** using two different Bitcoin address formats:

* **Legacy Transactions (P2PKH)**
* **SegWit Transactions (P2SH-P2WPKH)**

Through this lab we explore:

* Interaction with a **Bitcoin Core node using RPC**
* Creation of **raw Bitcoin transactions**
* Understanding **UTXO (Unspent Transaction Output) model**
* Analysis of **locking scripts (ScriptPubKey)** and **unlocking scripts (ScriptSig)**
* Understanding **SegWit witness data**
* Comparing transaction efficiency using:

  * Transaction **Size**
  * **Weight Units**
  * **Virtual Bytes (vbytes)**

This provides hands-on experience with how Bitcoin transactions are constructed, validated, and optimized.

---

# 🛠️ Prerequisites

Before running the scripts ensure the following tools are installed.

## 1️⃣ Bitcoin Core

Download Bitcoin Core from:

https://bitcoincore.org/en/download/

Make sure the following executables are available in your system:

```
bitcoind
bitcoin-cli
```

---

## 2️⃣ Python

Python **3.8 or later** is recommended.

Check installation:

```bash
python --version
```

---

## 3️⃣ Python Dependencies

Install the required Python package:

```bash
pip install requests
```

---

# ⚙️ Bitcoin Core Configuration

To interact with Bitcoin Core using RPC we must configure **bitcoin.conf**.

Typical location:

```
Windows:
C:\Users\<username>\AppData\Roaming\Bitcoin\bitcoin.conf
```

Add the following configuration:

```ini
regtest=1
server=1
rpcuser=iitstudent
rpcpassword=securepassword123
paytxfee=0.0001
fallbackfee=0.0002
mintxfee=0.00001
txconfirmtarget=6
```

Explanation:

| Parameter             | Description                          |
| --------------------- | ------------------------------------ |
| regtest               | Enables Bitcoin regression test mode |
| server                | Allows RPC commands                  |
| rpcuser / rpcpassword | Authentication for RPC               |
| paytxfee              | Default transaction fee              |
| fallbackfee           | Fee used if estimation fails         |
| mintxfee              | Minimum fee for relaying             |
| txconfirmtarget       | Target block confirmation            |

---

# 🚀 Starting the Bitcoin Node

Start the Bitcoin daemon in **regtest mode**.

```bash
bitcoind -regtest -daemon
```

Verify that the node is running:

```bash
bitcoin-cli -regtest getblockchaininfo
```

If this command returns blockchain information, the node is running successfully.

---

# 📂 Project Structure

```
CS216-HashSlayers-Bitcoin-Transaction-Project
│
├── Part1_Legacy
│   └── btc_l.py
│
├── Part2_SegWit
│   └── btc_s.py
│
├── screenshots
│   └── btcdeb_execution.png
│
└── README.md
```

---

# 📌 Important Setup Guide (Step-by-Step)

After saving the `.py` scripts into the folders shown above, follow the **step-by-step beginner guide** below to run the project locally.

This guide explains:

* How to start **Bitcoin Core in regtest**
* How to **load wallets**
* How to **run the Python scripts**
* How to fix common errors

👉 **Step-by-step guide:**
https://chatgpt.com/share/69aec62c-e940-8000-92f3-978b8d1c5daf

---

# 🚀 Running the Programs

## Part 1 — Legacy Transactions (P2PKH)

This script demonstrates the creation of **Legacy Bitcoin transactions**.

Workflow:

1. Create or load wallet
2. Generate addresses **A, B, C**
3. Mine **regtest blocks**
4. Fund address **A**
5. Create transaction chain:

```
A → B
B → C
```

Run the script:

```bash
python Part1_Legacy/btc_l.py
```

The script outputs:

* Generated Bitcoin addresses
* Transaction IDs
* Script structures
* Transaction size
* Weight
* Virtual size

---

# Part 2 — SegWit Transactions (P2SH-P2WPKH)

This script demonstrates **SegWit wrapped in P2SH transactions**.

Addresses used:

```
A'
B'
C'
```

Transaction chain:

```
A' → B'
B' → C'
```

Run the script:

```bash
python Part2_SegWit/btc_s.py
```

The script outputs:

* Transaction IDs
* ScriptSig
* Witness Data
* ScriptPubKey
* Transaction size metrics

---

# 🔍 Script Analysis

Bitcoin transactions are validated using **Bitcoin Script**, which is a **stack-based programming language**.

---

## Legacy Script Structure (P2PKH)

Locking Script (**ScriptPubKey**):

```
OP_DUP OP_HASH160 <PubKeyHash> OP_EQUALVERIFY OP_CHECKSIG
```

Unlocking Script (**ScriptSig**):

```
<Signature> <Public Key>
```

Execution Steps:

1. Push **Signature**
2. Push **Public Key**
3. Duplicate public key
4. Hash public key
5. Compare with stored PubKeyHash
6. Verify digital signature

If verification succeeds, the script returns **TRUE**.

---

# SegWit Script Structure (P2SH-P2WPKH)

ScriptPubKey:

```
OP_HASH160 <20-byte-hash> OP_EQUAL
```

ScriptSig:

```
<0x0014{20-byte-keyhash}>
```

Witness Data:

```
[ Signature , Public Key ]
```

SegWit separates signature data into the **Witness field**, reducing transaction weight.

---

# 📊 Transaction Size Comparison

SegWit transactions are more efficient because **witness data receives a discount in weight calculation**.

| Metric       | Legacy (P2PKH) | SegWit (P2SH-P2WPKH) |
| ------------ | -------------- | -------------------- |
| Size (bytes) | Higher         | Lower                |
| Weight       | Higher         | Lower                |
| Virtual Size | Larger         | Smaller              |

Formula:

```
Weight = (Non-Witness Bytes × 4) + Witness Bytes
vsize = Weight / 4
```

Because witness bytes count less, **SegWit transactions are cheaper and more scalable**.

---

# 🧪 Script Debugging using btcdeb

To verify Bitcoin scripts step-by-step we used **btcdeb (Bitcoin Script Debugger)**.

Example command:

```bash
btcdeb --txin=[scriptSig] --txout=[scriptPubKey]
```

btcdeb allows:

* Step-by-step script execution
* Stack inspection
* Verification of script correctness

This confirms that the transaction evaluates to **TRUE**.

---

# 📸 Screenshots

The repository includes screenshots showing:

* Raw transaction decoding
* Script structures
* btcdeb execution
* Transaction analysis

These screenshots demonstrate successful script validation.

---

# 📚 Key Concepts Learned

This assignment helped us understand:

* Bitcoin RPC interaction
* Raw transaction creation
* UTXO model
* Legacy vs SegWit transaction formats
* Script validation process
* Witness data structure
* Transaction size optimization

---

# ✅ Conclusion

This lab demonstrated how Bitcoin transactions can be created and analyzed programmatically.

We successfully:

* Built **Legacy and SegWit transactions**
* Analyzed Bitcoin **script validation**
* Compared **transaction efficiency**

SegWit significantly improves scalability by reducing transaction size and lowering fees.

---

# 📎 References

Bitcoin Developer Documentation
https://developer.bitcoin.org

Bitcoin Core RPC Reference
https://developer.bitcoin.org/reference/rpc/

SegWit BIP (BIP-141)
https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki
