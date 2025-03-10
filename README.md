Azure VNET API

This repository contains a demo API built with Python to create and manage an Azure Virtual Network (VNET) with multiple subnets. The API includes authentication via an API key

Features

Create an Azure Virtual Network with multiple subnets
Store VNET details in a database
Retrieve stored VNET details via API endpoints
Secure API access using an API key

Prerequisites

An active Azure subscription
Azure CLI
Python 3.x and pip
A GitHub account

Setup Instructions

1. Clone the Repository

git clone https://github.com/your-username/azure-vnet-api.git
cd azure-vnet-api

2. Set Up a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install Dependencies

pip install -r requirements.txt

4. Configure API Key Authentication

Generate an API key for secure access.

Update config/settings.json with the API key.

5. Deploy the API

python api/main.py


Deployment on Azure


To deploy the API as an Azure App Service, use the provided ARM template:

az deployment group create --resource-group <resource-group-name> --template-file config/azuredeploy.json

Contributing


Feel free to open issues and submit pull requests to improve the project.
