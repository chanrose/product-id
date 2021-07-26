from web3 import Web3, HTTPProvider
from vyper import compile_codes
import json
from datetime import datetime
from decimal import Decimal

source = open("contracts/ProductIdentification.vy", 'r')
contract_source_code = source.read()
source.close()
smart_contract = {}
smart_contract['aiucoin'] = contract_source_code
format = ['abi', 'bytecode']
compiled_code = compile_codes(smart_contract, format, 'dict')
abi, bytecode = compiled_code['aiucoin']['abi'], compiled_code['aiucoin']['bytecode']
w3 = Web3(HTTPProvider('HTTP://127.0.0.1:7545'))
contract = {
    'contract_addr': '0x7dBC2f3449d03CdC0Fc180c85435c9104AaF0e1a',
    'sender': '0xA9De700656B15946d72779ce89062345702Bd853',
    'private_key': '7581ac9c227dffd844ae3d6a8f81a8e78cee5256541fbe9192a2f4c28a3e6599'
}
pid = w3.eth.contract(address=contract['contract_addr'], abi=abi)
w3.eth.defaultAccount = contract['sender']
owner = pid.functions.contract_owner().call()

def generate_arr(arr, placeholder, size):
    while size > len(arr):
        arr.append(placeholder)
    return arr

def register_company_account(_sender, _name, _sec, _pw):
    nonce = w3.eth.getTransactionCount(_sender)
    txn = pid.functions.register_company_account(_name, _sec, _pw).buildTransaction({
        'gas': 100000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=_sec)
    signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    w3.eth.waitForTransactionReceipt(signed_txn_hash)

def get_company_account_name(_sender):
    return pid.functions.get_company_account_name().call()

def generate_pk(_product_name, _company_name):
    return (_product_name + _company_name + str(datetime.now().timestamp())).encode()

def register_product_py(_company_name, _name, _category, _release_year, _price, _country, _description, _serial_list, _sender, _sec ):
    pk = generate_pk(_name, _company_name)
    nonce = w3.eth.getTransactionCount(_sender)
    txn = pid.functions.register_product(pk, _name.encode(), _category.encode(), 2000, Decimal(12412.35), _country.encode(), _description, [1, 2, 3, 4 ,5 ,6, 7, 8, 9, 10]).buildTransaction({
        'gas': 100000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=_sec)
    signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    w3.eth.waitForTransactionReceipt(signed_txn_hash)

company_name = get_company_account_name(contract['sender'])
register_product_py("zero wing", "OnePlus 6t", "Smartphone", 2018, '600.01', "Cambodia", "Android smart phone", generate_arr([1239814, 1209599, 234123, 234123, 124125123], 0, 10), contract['sender'], contract['private_key']) 



# Register company
# register_company_account(contract['sender'], b"Zero Wing", contract['private_key'], b"Asd,car15")


# print(get_company_account_name(contract['sender']))
