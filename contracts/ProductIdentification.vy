# Account
struct Account:
    name: String[30]
    secret_key: String[100]
    password: String[30]
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

struct Unit:
    serial_code: String[30]

accounts_details: HashMap[address, Account]
products_details: HashMap[address, Product[1000]]
units_details: HashMap[String[30], Unit]

accounts_lists: address[1000]
account_index: uint256
product_index: uint256

contract_owner: public(address)


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
def get_secret_key(_password:String[30]) -> String[100]:
    assert self.exists_account(msg.sender), "You have not create an account yet"
    assert self.accounts_details[msg.sender].password == _password, "Incorrect password"
    return self.accounts_details[msg.sender].secret_key

@external
def register_company_account(_name:String[30], _secret_key:String[100], _password: String[30]):
    assert not self.exists_account(msg.sender), "You already register an account"
    assert self.account_index < 1000
    self.accounts_details[msg.sender] = Account({name: _name, secret_key: _secret_key, password: _password, product_index: 0})
    self.accounts_lists[self.account_index] = msg.sender
    self.account_index += 1

@external
def register_product(
    _name:bytes32, 
    _category:String[30], 
    _release_year:uint256, 
    _price:decimal, 
    _total_units:uint256, 
    _country:String[30], 
    _description:String[100]
    ):
    assert self.exists_account(msg.sender), "Please create your account first"
    assert self.product_index < 1000
   
    self.products_details[msg.sender][self.accounts_details[msg.sender].product_index] = Product({
        pk: sha256(_name),
        name: _name, 
        category: _category, 
        release_year: _release_year, 
        price: _price, 
        total_units: _total_units, 
        country: _country, 
        description: _description
        })
    self.accounts_details[msg.sender].product_index += 1

@view
@external
def get_list_of_products() -> bytes32[1000]:
    list_of_products: bytes32[1000] = [1000] 
    for i in self.products_details[msg.sender]:
        list_of_products[i] = products_details[msg.sender][i].name
    return list_of_products
    # return self.products_details[msg.sender][0].name
