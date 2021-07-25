# Account
struct Account:
    name: bytes32
    secret_key: String[64]
    password: bytes32
    product_index: uint256

struct Product:
    pk: bytes32
    name: bytes32
    category: String[30]
    release_year: uint256
    price: decimal
    total_units: uint256
    country: String[30]
    description: String[100]
    owner: address

# For Company Account Address
accounts_details: HashMap[address, Account]
accounts_lists: address[1000]
account_index: uint256

contract_owner: public(address)

# Product
# Primary Key -> Product
products_details: HashMap[address, Product[1000]]
products_pk: bytes32[1000]
products_pk_index: uint256

# Units
units_details: HashMap[bytes32, bytes32[1000]]

@external
def __init__():
    self.contract_owner = msg.sender

@view
@internal
def exists_account(_address:address) -> bool:
    for a in self.accounts_lists:
        if a == _address:
            return True
    return False

@view
@external
def get_secret_key(_password:bytes32) -> String[64]:
    assert self.exists_account(msg.sender), "You have not create an account yet"
    assert self.accounts_details[msg.sender].password == _password, "Incorrect password"
    return self.accounts_details[msg.sender].secret_key

@external
def register_company_account(_name:bytes32, _secret_key:String[64], _password: bytes32):
    assert not self.exists_account(msg.sender), "You already register an account"
    assert self.account_index < 1000
    self.accounts_details[msg.sender] = Account({name: _name, secret_key: _secret_key, password: _password, product_index: 0})
    self.accounts_lists[self.account_index] = msg.sender
    self.account_index += 1

# PK should be the hash format of timestamp + company name + product name
@external
def register_product(
    _pk:bytes32,
    _name:bytes32, 
    _category:String[30], 
    _release_year:uint256, 
    _price:decimal, 
    _total_units:uint256, 
    _country:String[30], 
    _description:String[100]
    ):
    assert self.exists_account(msg.sender), "Please create your account first"
   
    self.products_details[msg.sender][self.accounts_details[msg.sender].product_index] = Product({
        pk: _pk,
        name: _name, 
        category: _category, 
        release_year: _release_year, 
        price: _price, 
        total_units: _total_units, 
        country: _country, 
        description: _description,
        owner: msg.sender
        })
    self.accounts_details[msg.sender].product_index += 1

@view
@external
def get_list_of_products(_arr:bytes32[1000]) -> bytes32[1000]:
    list_of_products: bytes32[1000] = _arr
    temp_index: uint256 = 0
    max_index: uint256 = self.accounts_details[msg.sender].product_index
    length: int256 = 100
    for i in range(100):
        if temp_index > max_index:
            break
        list_of_products[temp_index] = self.products_details[msg.sender][i].name
        temp_index += 1
    return list_of_products

@view
@external
def get_product(_pk:bytes32) -> bytes32:
    max_len: uint256 = self.accounts_details[msg.sender].product_index
    for i in range(1000):
        if i >= max_len:
            break
        if self.products_details[msg.sender][i].pk == _pk:
            return self.products_details[msg.sender][i].name
    return 0x0000000000000000000000000000000000000000000000000000000000000000

@view
@external
def get_first_product() -> bytes32:
    return self.products_details[msg.sender][0].name

@view
@external
def get_last_product() -> bytes32:
    return self.products_details[msg.sender][self.accounts_details[msg.sender].product_index - 1].name


@view
@external
def get_my_products() -> String[30]:
    return "Hello there"
