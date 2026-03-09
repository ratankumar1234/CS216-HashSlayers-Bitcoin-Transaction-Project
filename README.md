# CS 216: Bitcoin Transaction Lab Assignment
**Team Name:** HashSlayers  
**Repository:** [ratankural1234/CS216-HashSlayers-Bitcoin-Transaction-Project](https://github.com/ratankumar1234/CS216-HashSlayers-Bitcoin-Transaction-Project)

---

## 👥 Team Members
| Name | Roll Number |
| :--- | :--- |
| [Raghav Sharma(Leader)] | [240001056] |
| [Abhishek Kumar Verma] | [240001005] |
| [Ratan Kumar] | [240001059] |
| [Rohan Chauhan] | [240001061] |

---

## 🎯 Objective
[cite_start]The objective of this assignment is to programmatically create and validate Bitcoin transactions using **Legacy (P2PKH)** and **SegWit (P2SH-P2WPKH)** address formats[cite: 24]. [cite_start]We explore the process of interacting with `bitcoind` via RPC, analyzing locking/unlocking scripts, and comparing transaction efficiency in terms of `vbytes` and `weight`[cite: 25, 26].

---

## 🛠️ Prerequisites & Setup
To run these scripts, you need a local Bitcoin Core installation and a Python environment.

### 1. Configure Bitcoin Core (`bitcoin.conf`)
[cite_start]Ensure your `bitcoin.conf` is set up for `regtest` mode with the following parameters as required by the assignment [cite: 64-70]:
```ini
regtest=1
server=1
rpcuser=iitstudent
rpcpassword=securepassword123
paytxfee=0.0001
fallbackfee=0.0002
mintxfee=0.00001
txconfirmtarget=6
