import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------
# TODO: Replace these with your actual Azure details
SUBSCRIPTION_ID = '6de86bda-15aa-40cf-bec8-b60d1d2f38f9'
RESOURCE_GROUP = 'YOUR_RESOURCE_GROUP'

# The specific tag we are looking for to identify Dev VMs
TARGET_TAG = 'Environment'
TARGET_VALUE = 'Dev'

# SAFETY SWITCH: Set to True to test the script without actually stopping VMs.
# Set to False when you are ready to run it for real.
DRY_RUN = True 

def main():
    print(f"Starting Cost Optimization Script (Dry Run: {DRY_RUN})...")

    # 1. Authentication
    # We use DefaultAzureCredential so this works locally (via Azure CLI) 
    # and in the cloud (via Managed Identity) without code changes.
    try:
        credential = DefaultAzureCredential()
        compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
    except Exception as e:
        print(f"CRITICAL ERROR: Failed to authenticate. {e}")
        return

    # 2. Get List of VMs
    try:
        vms = compute_client.virtual_machines.list(RESOURCE_GROUP)
    except Exception as e:
        print(f"CRITICAL ERROR: Could not list VMs. Check Resource Group name. {e}")
        return

    # 3. Iterate and Check
    for vm in vms:
        try:
            # Handle cases where a VM has no tags (returns None)
            tags = vm.tags or {}
            
            # Check if the specific tag key and value match (Environment: Dev)
            if tags.get(TARGET_TAG) == TARGET_VALUE:
                
                # Check the power state (we only want to stop running VMs)
                vm_instance = compute_client.virtual_machines.instance_view(RESOURCE_GROUP, vm.name)
                is_running = any(s.code == 'PowerState/running' for s in vm_instance.statuses)

                if is_running:
                    print(f"[MATCH] {vm.name} is RUNNING with tag {TARGET_TAG}={TARGET_VALUE}.")
                    
                    if not DRY_RUN:
                        print(f"        --> Stopping {vm.name}...")
                        compute_client.virtual_machines.begin_deallocate(RESOURCE_GROUP, vm.name)
                    else:
                        print(f"        --> (Dry Run) Would have stopped {vm.name}.")
                
                else:
                    print(f"[SKIP]  {vm.name} is already stopped.")
            
            else:
                # VM exists but doesn't have the 'Dev' tag
                print(f"[IGNORE] {vm.name} does not match target tags.")

        except Exception as e:
            # If one VM fails (e.g., locked), print error and continue to the next one
            print(f"ERROR processing {vm.name}: {e}")

    print("Script complete.")

if __name__ == "__main__":
    main()
