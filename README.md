# Cloud Infrastructure Scripts

A collection of Python scripts for automating Microsoft Azure infrastructure management, cost optimization, and administrative tasks. 

This repository serves as a portfolio of cloud engineering tools designed to solve real-world operational challenges using the Azure SDK for Python.

## 📂 Catalog of Scripts

| Script Name | Description | Key Services |
| :--- | :--- | :--- |
| **`vm-auto-stop.py`** | Automates cost savings by identifying and deallocating specific Dev/Test Virtual Machines. | Compute, Tags |
| *(Coming Soon)* | *Future scripts for Storage Account management and Network security checks.* | ... |

---

## 🚀 Feature: VM Auto-Stopper (`vm-auto-stop.py`)

This script helps reduce cloud spend by automatically finding Virtual Machines that are meant for development (tagged `Environment: Dev`) and ensuring they are deallocated.

**Key Logic:**
1. Authenticates securely using `DefaultAzureCredential`.
2. Scans a target Resource Group for VMs.
3. Filters for VMs with specific tags (e.g., `Environment: Dev`).
4. Checks the **Instance View** to see if the VM is currently `Running`.
5. **Action:** Deallocates the VM to stop billing.
6. **Safety:** Includes a `DRY_RUN` flag to simulate actions without affecting production.

---

## 🛠️ Prerequisites

To run these scripts, you will need:

* **Python 3.8+**
* **Azure CLI** (for local authentication)
* **Azure Subscription** (with permissions to manage resources)

### Required Libraries
```bash
pip install azure-identity azure-mgmt-compute
