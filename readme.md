# Ethereum Contract Dependency Graph

## Overview
This project is a Python application that builds a dependency graph for an Ethereum contract. It identifies the contract's deployer, other contracts deployed by the same deployer, and the addresses that frequently interact with the contract.

## Features
- Accepts an Ethereum contract address as input.
- Retrieves the deployer of the specified contract.
- Lists other contracts deployed by the same deployer.
- Identifies and displays the addresses that have made the most interactions with the contract.

## Technologies Used
- Python 3.x
- Requests library for making HTTP requests to the Etherscan API.

## Setup
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository
   
2.  Create a virtual environment
```python -m venv .venv```

3. Activate the virtual environment:
```source .venv/bin/activate```

4. Install required packages:
```pip install requests```

5. Obtain an Etherscan API key:

* Sign up at Etherscan.
* Generate an API key from your account dashboard.

6. Update the API key in the code:
* Open the Python script and replace your_api_key with your actual Etherscan API key.

## Contribution
Feel free to fork the repository and submit pull requests for any improvements or features you'd like to add!