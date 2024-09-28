import requests
import os
from dotenv import load_dotenv


load_dotenv()
# Constants
ETHERSCAN_API_URL = 'https://api.etherscan.io/api'
API_KEY = os.getenv("ETHERSCAN_API_KEY")


def get_contract_creation(contract_address):
    """Fetch the contract creation transaction details."""
    params = {
        'module': 'contract',
        'action': 'getcontractcreation',
        'contractaddresses': contract_address,
        'apikey': API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    data = response.json()

    if data['status'] == '1':
        creation_tx = data['result'][0]['txHash']
        deployer_address = data['result'][0]['contractCreator']
        return deployer_address, creation_tx
    else:
        print(f"Error fetching contract creation data: {data['message']}")
        return None, None


def get_deployer_contracts(deployer_address):
    """Fetch contracts deployed by the same deployer address."""
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': deployer_address,
        'apikey': API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    data = response.json()

    if data['status'] == '1':
        contracts = [tx['to'] for tx in data['result'] if
                     tx['to'] != '' and tx['contractAddress'] != '']
        return contracts
    else:
        print(f"Error fetching deployer contracts: {data['message']}")
        return []


def get_frequent_callers(contract_address):
    """Fetch addresses interacting with the contract the most."""
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': contract_address,
        'apikey': API_KEY
    }
    response = requests.get(ETHERSCAN_API_URL, params=params)
    data = response.json()

    if data['status'] == '1':
        callers = {}
        for tx in data['result']:
            caller = tx['from']
            if caller in callers:
                callers[caller] += 1
            else:
                callers[caller] = 1

        frequent_callers = sorted(callers.items(), key=lambda item: item[1],
                                  reverse=True)
        return frequent_callers[:5]  # Return top 5 frequent callers
    else:
        print(f"Error fetching frequent callers: {data['message']}")
        return []


def build_dependency_graph(contract_address):
    """Build a dependency graph for the given contract."""
    print(f"Building dependency graph for contract: {contract_address}")

    # Step 1: Get the deployer of the contract
    deployer_address, creation_tx = get_contract_creation(contract_address)
    if not deployer_address:
        return

    print(
        f"Contract {contract_address} was deployed by {deployer_address} in "
        f"transaction {creation_tx}")

    # Step 2: Get other contracts deployed by the same deployer
    deployer_contracts = get_deployer_contracts(deployer_address)
    print(f"Contracts deployed by {deployer_address}: {deployer_contracts}")

    # Step 3: Get frequent callers of the input contract
    frequent_callers = get_frequent_callers(contract_address)
    print(
        f"Frequent callers of contract {contract_address}: {frequent_callers}")

    # Output the dependency graph
    graph = {
        "contract_address": contract_address,
        "deployer": deployer_address,
        "deployer_contracts": deployer_contracts,
        "frequent_callers": frequent_callers
    }

    return graph


# Example usage
if __name__ == "__main__":
    # Uniswap V2 Router (decentralized exchange)
    contract_address = "0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f"
    # Ethereum contract address
    dependency_graph = build_dependency_graph(contract_address)
    print(dependency_graph)
