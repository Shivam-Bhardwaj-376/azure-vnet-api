from fastapi import FastAPI, Depends, HTTPException, Header
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
import os
import json

app = FastAPI()

# Load API Key from environment
API_KEY = os.getenv("API_KEY")

# Azure subscription details
SUBSCRIPTION_ID = os.getenv("AZURE_SUBSCRIPTION_ID")

# Authenticate with Managed Identity
credential = DefaultAzureCredential()

# Initialize Azure clients
resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
network_client = NetworkManagementClient(credential, SUBSCRIPTION_ID)


def read_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Return an empty dictionary if file is missing or corrupted


def write_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)


# Dependency to check API key
def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


# API route to create a VNET (Requires Authentication)
@app.post("/create-vnet/", dependencies=[Depends(verify_api_key)])
def create_vnet(resource_group: str, vnet_name: str):
    global network_client

    # Define VNET parameters
    vnet_params = {
        "location": "eastus",
        "address_space": {"address_prefixes": ["10.0.0.0/16"]},
        "subnets": [
            {"name": "subnet1", "address_prefix": "10.0.1.0/24"},
            {"name": "subnet2", "address_prefix": "10.0.2.0/24"}
        ]
    }

    # Create VNET in Azure
    vnet = network_client.virtual_networks.begin_create_or_update(
        resource_group, vnet_name, vnet_params
    ).result()

    # Read current data
    data = read_data()

    # Store VNET details in JSON
    data[vnet_name] = {
        "resource_group": resource_group,
        "location": "eastus",
        "address_prefixes": ["10.0.0.0/16"],
        "subnets": [
            {"name": "subnet1", "address_prefix": "10.0.1.0/24"},
            {"name": "subnet2", "address_prefix": "10.0.2.0/24"}
        ]
    }

    # Write updated data back to file
    write_data(data)

    return {
        "message": "VNET created successfully",
        "vnet_name": vnet_name,
        "location": "eastus",
        "subnets": data[vnet_name]["subnets"],
    }


# API route to get VNET details (Requires Authentication)
@app.get("/get-vnet/{vnet_name}", dependencies=[Depends(verify_api_key)])
def get_vnet(vnet_name: str):
    data = read_data()
    if vnet_name in data:
        return data[vnet_name]
    return {"error": "VNET not found"}
