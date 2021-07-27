from web3 import Web3, HTTPProvider
from vyper import compile_codes
import json
from datetime import datetime
from decimal import Decimal

source = open("contracts/ProductIdentification.vy", 'r')
contract_source_code = source.read()
source.close()
smart_contract = {}
smart_contract['pid'] = contract_source_code
format = ['abi', 'bytecode']
compiled_code = compile_codes(smart_contract, format, 'dict')
abi, bytecode = compiled_code['pid']['abi'], compiled_code['pid']['bytecode']
w3 = Web3(HTTPProvider('HTTP://127.0.0.1:7545'))
contract = {
    'contract_addr': '0x632442372726AD0A21Cb4C10862F48D219dA1A61',
    'sender': '0x82C8e96B7C196AaB49cc4f84B7b73d95435c791d',
    'private_key': '78db86f815229c527912c9f74b610dccc49a89af3db84c096e62374a1d7999c9'
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
        'gas': 2000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=_sec)
    signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return w3.eth.waitForTransactionReceipt(signed_txn_hash)

def clean_bytes(_input):
    return _input.decode().rstrip('\x00')


def get_company_account_name(_sender):
    w3.eth.defaultAccount = _sender
    return clean_bytes(pid.functions.get_company_account_name().call())

def get_company_name_list(_sender):
    w3.eth.defaultAccount = _sender
    tmp = pid.functions.get_list_of_company_acc().call()
    new_list = []
    for key, val in enumerate(tmp):
        if '0x000' in val:
            return new_list
        new_list.append(get_company_account_name(val))
    return new_list

print("Names", get_company_name_list(pid.functions.contract_owner().call()))

def generate_pk(_product_name):
    now = str(datetime.now().timestamp())
    return(_product_name + now)

def register_product(_pk, _name, _category, _release_year, _price, _country, _description, _serial_list, _sender, _key):
    w3.eth.defaultAccount = _sender
    nonce = w3.eth.getTransactionCount(_sender)
    txn = pid.functions.register_product(_pk, _name, _category, _release_year, _price, _country, _description, _serial_list).buildTransaction({
        'gas': 3000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=_key)
    signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return w3.eth.waitForTransactionReceipt(signed_txn_hash)

def update_product(_target_pk, _name, _category, _price, _description, _sender, _key):
    w3.eth.defaultAccount = _sender
    nonce = w3.eth.getTransactionCount(_sender)
    txn = pid.functions.update_product(_target_pk, _name, _category, _price,_description).buildTransaction({
        'gas': 3000000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=_key)
    signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return w3.eth.waitForTransactionReceipt(signed_txn_hash)


def get_product_prop(_pk, _sender):
    w3.eth.defaultAccount = _sender
    tmp = pid.functions.get_product_prop(_pk).call()
    tmp[5] = [val for val in tmp[5] if val != 0]
    data = {
        'name': clean_bytes(tmp[0][0]),
        'category': clean_bytes(tmp[0][1]),
        'release_year': tmp[1],
        'price': tmp[2],
        'country': clean_bytes(tmp[3]),
        'description': tmp[4],
        'serial_lists': tmp[5]
    } 
    return data

# Get List of Products return a list of all the product primary key under the company account
def get_list_of_products(_sender):
    w3.eth.defaultAccount = _sender
    tmp = pid.functions.get_list_of_products(generate_arr([], b'0', 1000)).call()
    new_list = []
    for key, val in enumerate(tmp):
        if str(clean_bytes(val)) != '0':
            new_list.append(clean_bytes(val))
    return new_list

# Return the first product of the company acc
def get_first_product(_sender):
    w3.eth.defaultAccount = _sender
    return pid.functions.get_first_product().call()

# Return the last product of the company acc
def get_last_product(_sender):
    w3.eth.defaultAccount = _sender
    return pid.functions.get_last_product().call()

def validate_product_serial(_pk, _serial_key, _sender): 
    tmp = get_product_prop(_pk.encode(), _sender)
    return _serial_key in tmp['serial_lists']

def get_secret_key(_sender, _pw):
    w3.eth.defaultAccount = _sender
    return pid.functions.get_secret_key(_pw).call()


p_name = "Google Pixel"
pk = generate_pk(p_name).encode('UTF-8')
# print(register_product(pk, p_name.encode(), "SmartPhone".encode(), 2021, 78421, "US".encode(), "Android phone", generate_arr([12323, 23123, 5123], 0, 10), contract['sender'], contract['private_key']))

# print(get_product_prop(pk, contract['sender']))
# valid = validate_product_serial(pk, 5123, contract['sender'])
# print(get_product_prop(pk.encode(), contract['sender'])) 
# update_product(pk.encode(), "Nexus 5t".encode(), "Cell phone".encode(), 2222, "Dumb phone", contract['sender'], contract['private_key'])



# register_company_account(contract['sender'], b"Zero Wing", contract['private_key'], b'Asd,car15')

# print(get_secret_key(contract['sender'], b"Asd,car15"))
# print(get_company_account_name(contract['sender']))

