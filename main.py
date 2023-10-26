import os
import json
from web3 import Web3
from web3.exceptions import ContractLogicError
import asyncio
from config import contract_address,wallets_file_path,rpc,private_key

share_amount_to_sell = 1
with open("contractABI.json", 'r') as abi_file:
    contract_abi = json.load(abi_file)

w3 = Web3(Web3.HTTPProvider(rpc))
w3.eth.default_account = w3.eth.account.from_key(private_key).address
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

async def sell_keys_from_wallets(wallet_addresses):
    tasks = []
    for specific_address in wallet_addresses:
        checksum_address = Web3.to_checksum_address(specific_address)
        tasks.append(sell_shares(checksum_address, share_amount_to_sell))

    await asyncio.gather(*tasks)

async def sell_shares(specific_address, share_amount):
    if not specific_address:
        return

    try:
        nonce = w3.eth.get_transaction_count(w3.eth.default_account)

        tx = {
            'chainId': 8453,
            'from': w3.eth.default_account,
            'to': contract_address,
            'nonce': nonce,
            'value': 0,
            'data': contract.encodeABI(fn_name="sellShares", args=[specific_address, share_amount]),
            'maxFeePerGas': 0,
            'maxPriorityFeePerGas': 0
        }
        gas = w3.eth.gas_price
        tx['maxPriorityFeePerGas'] = gas
        tx['maxFeePerGas'] = gas
        tx['gas'] = w3.eth.estimate_gas(tx)
        sign = w3.eth.account.from_key(private_key).sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(sign.rawTransaction)
        tx_url = f'https://basescan.org/tx/{w3.to_hex(tx_hash)}'
        if not await check_status_tx(tx_hash, tx_url):
            print(f'Tx {tx_url} wasn\'t confirmed, trying to sell one more time...')
            return

        print("------------------------------------------")
        print(f"SUCCESFULLY SOLD {share_amount} KEYS")
        print(f"Key address - {specific_address}")
        print(f"Transaction - {tx_url}")
        print("------------------------------------------")

    except ContractLogicError as e:
        print(f"Contract execution error for address {specific_address}: {str(e)}")

async def check_status_tx(tx_hash, tx_url):
    try:
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print(f'Transaction {tx_url} was successfully confirmed.')
            return True
        else:
            print(f'Transaction {tx_url} failed or was reverted.')
            return False
    except Exception as e:
        print(f'Error checking transaction status for {tx_url}: {str(e)}')
        return False

if __name__ == "__main__":
    if os.path.exists(wallets_file_path):
        with open(wallets_file_path, 'r') as wallets_file:
            wallet_addresses = wallets_file.read().splitlines()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(sell_keys_from_wallets(wallet_addresses))
    else:
        print("File with wallets not found")