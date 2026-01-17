import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient

#SetUp is here. No ID should be visible! 
SUBSCRIPTION_ID = '6de86bda-15aa-40cf-bec8-b60d1d2f38f9'
RESOURCE_GROUP = 'VirtualMachineTest'

# Tag to look for
TARGET_TAG = 'Environment'
TARGET_VALUE = 'Dev'

# SAFETY SWITCH: True = Test Mode (Won't stop anything), False = Real Mode
DRY_RUN = True 

def main():
    print(f"Starting Cost Optimization Script (Dry Run: {DRY_RUN})")
#Step #1: Logging In
    print("Connecting to Azure...")
    
    credential = DefaultAzureCredential()

    compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)

Step #2: Logic Code
    print(f"Checking VMs in group: {RESOURCE_GROUP}...")

    # Get list of VMs
    vms = compute_client.virtual_machines.list(RESOURCE_GROUP)

    for vm in vms:
        try:
            # Use a blank if no tag if found. Prevents crashing the code
            tags = vm.tags or {}
            
            # Check for the "Environment: Dev" tag
            if tags.get(TARGET_TAG) == TARGET_VALUE:
                
                # Check if it is currently running
                vm_instance = compute_client.virtual_machines.instance_view(RESOURCE_GROUP, vm.name)
                is_running = any(s.code == 'PowerState/running' for s in vm_instance.statuses)

                if is_running:
                    print(f"[MATCH] {vm.name} is RUNNING.")
                    
                    if not DRY_RUN:
                        print(f"        --> Stopping {vm.name}...")
                        compute_client.virtual_machines.begin_deallocate(RESOURCE_GROUP, vm.name)
                    else:
                        print(f"        --> (Dry Run) Would have stopped {vm.name}.")
                
                else:
                    print(f"[SKIP]  {vm.name} is already stopped.")
            
            else:
                print(f"[IGNORE] {vm.name} (Tags do not match)")

        except Exception as e:
            print(f"ERROR processing {vm.name}: {e}")

    print("Script complete.")

if __name__ == "__main__":
    main()
