# ⚡ CS 216: Bitcoin Transaction Lab Assignment

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Bitcoin](https://img.shields.io/badge/Bitcoin-Core-orange.svg)
![Regtest](https://img.shields.io/badge/Network-Regtest-green.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)

**Team Name:** HashSlayers
**Repository:**
https://github.com/ratankumar1234/CS216-HashSlayers-Bitcoin-Transaction-Project

---

# 📑 Table of Contents

* [Team Members](#-team-members)
* [Objective](#-objective)
* [Prerequisites](#-prerequisites)
* [Bitcoin Core Configuration](#️-bitcoin-core-configuration)
* [Starting the Bitcoin Node](#-starting-the-bitcoin-node)
* [Project Structure](#-project-structure)
* [Step-by-Step Execution Guide](#-step-by-step-execution-guide)
* [Running the Programs](#-running-the-programs)
* [Transaction Workflow](#-transaction-workflow)
* [Script Analysis](#-script-analysis)
* [Transaction Size Comparison](#-transaction-size-comparison)
* [Debugging with btcdeb](#-script-debugging-using-btcdeb)
* [Key Concepts Learned](#-key-concepts-learned)
* [Conclusion](#-conclusion)
* [References](#-references)

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

The objective of this assignment is to **programmatically create and validate Bitcoin transactions** using two address formats:

* **Legacy Transactions (P2PKH)**
* **SegWit Transactions (P2SH-P2WPKH)**

In this lab we explore:

* Interaction with a **Bitcoin Core node using RPC**
* Creation of **raw Bitcoin transactions**
* Understanding the **UTXO (Unspent Transaction Output) model**
* Analysis of **locking scripts (ScriptPubKey)** and **unlocking scripts (ScriptSig)**
* Understanding **SegWit witness data**
* Comparing transaction efficiency using:

  * Transaction **Size**
  * **Weight Units**
  * **Virtual Bytes (vbytes)**

This provides hands-on experience with how Bitcoin transactions are created and validated.

---

# 🛠 Prerequisites

Before running the scripts ensure the following software is installed.

## 1️⃣ Bitcoin Core

Download Bitcoin Core:

https://bitcoincore.org/en/download/

Required executables:

```
bitcoind
bitcoin-cli
```

---

## 2️⃣ Python

Python **3.8 or later**.

Check installation:

```bash
python --version
```

---

## 3️⃣ Python Dependencies

Install required library:

```bash
pip install requests
```

---

# ⚙️ Bitcoin Core Configuration

Edit **bitcoin.conf**

Location:

```
Windows:
C:\Users\<username>\AppData\Roaming\Bitcoin\bitcoin.conf
```

Example configuration (also included in the repository under `config/bitcoin.conf`):

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

| Parameter        | Description                        |
| ---------------- | ---------------------------------- |
| regtest          | Enables regression testing network |
| server           | Enables RPC commands               |
| rpcuser/password | Authentication                     |
| paytxfee         | Default transaction fee            |
| fallbackfee      | Backup fee estimation              |
| mintxfee         | Minimum relay fee                  |
| txconfirmtarget  | Target confirmation blocks         |

---

# 🚀 Starting the Bitcoin Node

Start the node in **regtest mode**.

```bash
bitcoind -regtest 
```

Verify the node is running:

```bash
bitcoin-cli -regtest getblockchaininfo
```

Create Wallet (only once)

```bash
.\bitcoin-cli -regtest createwallet "testwallet"
```
Load  Wallet 

```bash
\bitcoin-cli -regtest loadwallet "testwallet"
```

---

# 📂 Project Structure

The repository is organized into separate folders for each part of the assignment.

```
CS216-HashSlayers-Bitcoin-Transaction-Project
│
├── Part1_Legacy/
│   ├── btc_l.py
│   └── screenshots/
│       └── (decoded scripts & btcdeb screenshots)
│
├── Part2_SegWit/
│   ├── btc_s.py
│   └── screenshots/
│       └── (decoded scripts & btcdeb screenshots)
│
├── config/
│   └── bitcoin.conf
│
├── report/
│   └── Lab_Assignment_Report.pdf
│
├── .gitignore
└── README.md
```

### Folder Explanation

| Folder           | Purpose                                                    |
| ---------------- | ---------------------------------------------------------- |
| **Part1_Legacy** | Python implementation of Legacy (P2PKH) transactions       |
| **Part2_SegWit** | Python implementation of SegWit (P2SH-P2WPKH) transactions |
| **screenshots**  | Screenshots of script execution and btcdeb debugging       |
| **config**       | Bitcoin Core configuration file                            |
| **report**       | Final assignment report PDF                                |
| **README.md**    | Main project documentation                                 |

---

# 📌 Step-by-Step Execution Guide

After saving the `.py` files in the folders shown above, follow the **beginner-friendly step-by-step guide** below.

This guide explains:

* How to run **Bitcoin Core locally**
* How to **load wallets**
* How to **mine blocks in regtest**
* How to **run the Python scripts**
* How to fix common RPC errors

👉 Step-by-step guide:
https://chatgpt.com/share/69aec62c-e940-8000-92f3-978b8d1c5daf

---

# 🚀 Running the Programs

## Part 1 — Legacy Transactions (P2PKH)

Workflow:

1. Create / load wallet
2. Generate addresses **A, B, C**
3. Mine **regtest blocks**
4. Fund address **A**
5. Create transaction chain

```
A → B
B → C
```

Run:

```bash
python Part1_Legacy/btc_l.py
```

Outputs:

* Bitcoin addresses
* Transaction IDs
* Script structures
* Transaction size / weight / vbytes

---

## Part 2 — SegWit Transactions (P2SH-P2WPKH)

Addresses:

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

Run:

```bash
python Part2_SegWit/btc_s.py
```

Outputs:

* Transaction IDs
* ScriptSig
* Witness data
* ScriptPubKey
* Transaction metrics

---

# 🔄 Transaction Workflow

Legacy Transaction Flow:

```
Address A
   │
   ▼
Address B
   │
   ▼
Address C
```

SegWit Transaction Flow:

```
Address A'
   │
   ▼
Address B'
   │
   ▼
Address C'
```

---

# 🔍 Script Analysis

Bitcoin uses **Bitcoin Script**, a stack-based scripting language.

---

## Legacy Script (P2PKH)

ScriptPubKey:

```
OP_DUP OP_HASH160 <PubKeyHash> OP_EQUALVERIFY OP_CHECKSIG
```

ScriptSig:

```
<Signature> <Public Key>
```

Execution Steps:

1. Push Signature
2. Push Public Key
3. Duplicate public key
4. Hash public key
5. Compare with PubKeyHash
6. Verify signature

Result → **TRUE**

---

# SegWit Script (P2SH-P2WPKH)

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

SegWit separates signature data into a **witness field**, reducing transaction weight.

---

# 📊 Transaction Size Comparison

| Metric       | Legacy (P2PKH) | SegWit (P2SH-P2WPKH) |
| ------------ | -------------- | -------------------- |
| Size         | Higher         | Lower                |
| Weight       | Higher         | Lower                |
| Virtual Size | Larger         | Smaller              |

Formula:

```
Weight = (Non-Witness Bytes × 4) + Witness Bytes
vsize = Weight / 4
```

SegWit reduces effective transaction size → **lower fees & higher block capacity**.

---

# 🧪 Script Debugging using btcdeb

We verified scripts using **btcdeb**.

Example:

```bash
btcdeb --txin=[scriptSig] --txout=[scriptPubKey]
```

btcdeb allows:

* Step-by-step execution
* Stack inspection
* Script validation

---

# 📸 Screenshots

Repository includes:

* Raw transaction decoding
* Script structure
* btcdeb execution
* Transaction analysis

These screenshots are available inside the **screenshots folders** in each part of the project.

---

# 📚 Key Concepts Learned

This assignment covered:

* Bitcoin RPC interaction
* Raw transaction construction
* UTXO model
* Legacy vs SegWit architecture
* Script validation
* Witness data structure
* Transaction size optimization

---

# ✅ Conclusion

This lab demonstrated the full lifecycle of Bitcoin transactions.

We successfully:

* Created **Legacy and SegWit transactions**
* Validated Bitcoin **scripts**
* Compared **transaction efficiency**

SegWit significantly improves scalability by reducing transaction weight and fees.

---

# 📎 References

Bitcoin Developer Documentation
https://developer.bitcoin.org

Bitcoin RPC Reference
https://developer.bitcoin.org/reference/rpc/

SegWit BIP-141
https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki
