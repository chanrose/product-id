# Account
struct Account:
    name: bytes32
    secret_key: String[64]
    password: bytes32
    product_index: uint256

struct Product:
    pk: bytes32
    name: bytes32
    category: bytes32
    release_year: uint256
    price: decimal
    country: bytes32
    description: String[100]
    unit_serial_list: uint256[10]

# For Company Account Address
accounts_details: HashMap[address, Account]
accounts_lists: address[1000]
account_index: uint256

contract_owner: public(address)

# Product
# Primary Key -> Product
products_details: HashMap[address, Product[1000]]

event Account_Creation:
    _pub_key:indexed(address)
    _name:bytes32 
    _timestamp:uint256

event Product_Registration_Update:
    _pub_key:indexed(address)
    _pk:bytes32
    _name:bytes32 
    _timestamp:uint256

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
    log Account_Creation(msg.sender, _name, block.timestamp)

@view
@external
def get_company_account_name() -> bytes32:
    return self.accounts_details[msg.sender].name

# PK should be the hash format of timestamp + company name + product name
@external
def register_product(
    _pk:bytes32,
    _name:bytes32, 
    _category:bytes32, 
    _release_year:uint256, 
    _price:decimal, 
    _country:bytes32, 
    _description:String[100],
    _serial_lists:uint256[10]
    ):
    assert self.exists_account(msg.sender), "You are not authorize"
    self.products_details[msg.sender][self.accounts_details[msg.sender].product_index] = Product({
        pk: _pk,
        name: _name, 
        category: _category, 
        release_year: _release_year, 
        price: _price, 
        country: _country, 
        description: _description,
        unit_serial_list: _serial_lists
        })
    self.accounts_details[msg.sender].product_index += 1
    log Product_Registration_Update(msg.sender, _pk, _name, block.timestamp)


@external
def update_product(
    _target_product_pk:bytes32,
    _name:bytes32, 
    _category:bytes32, 
    _price:decimal, 
    _description:String[100],
    ):
    assert self.exists_account(msg.sender), "You are not authorize"
    max_len: uint256 = self.accounts_details[msg.sender].product_index
    for i in range(1000):
        if i >= max_len:
            break
        if self.products_details[msg.sender][i].pk == _target_product_pk:
            product: Product = self.products_details[msg.sender][i]
            product.name= _name
            product.category = _category
            product.price = _price
            product.description = _description
            self.products_details[msg.sender][i] = product
            log Product_Registration_Update(msg.sender, product.pk, _name, block.timestamp)


@view
@external
def get_list_of_products(_arr:bytes32[1000]) -> bytes32[1000]:
    assert self.exists_account(msg.sender), "You are not authorize"
    list_of_products: bytes32[1000] = _arr
    temp_index: uint256 = 0
    max_index: uint256 = self.accounts_details[msg.sender].product_index
    for i in range(1000):
        if temp_index > max_index:
            break
        list_of_products[temp_index] = self.products_details[msg.sender][i].pk
        temp_index += 1
    return list_of_products

@view
@external
def validate_product_serial(_pk:bytes32, _serial_key:uint256) -> (bool):
    max_len: uint256 = self.accounts_details[msg.sender].product_index
    for i in range(1000):
        if i >= max_len:
            break
        if self.products_details[msg.sender][i].pk == _pk:
            product: Product = self.products_details[msg.sender][i]
            for key in product.unit_serial_list:
                if key == _serial_key:
                    return True
    return False
 
@view
@external
def get_product_prop(_pk:bytes32) -> (bytes32[2], uint256, decimal, bytes32, String[100], uint256[10]):
    max_len: uint256 = self.accounts_details[msg.sender].product_index
    for i in range(1000):
        if i >= max_len:
            break
        if self.products_details[msg.sender][i].pk == _pk:
            product: Product = self.products_details[msg.sender][i]
            return ([product.name, product.category], product.release_year, product.price, product.country, product.description, product.unit_serial_list)
    temp: bytes32 = 0x0000000000000000000000000000000000000000000000000000000000000000
    # Just for the sake of returning... Don't blame me
    return ([temp, temp], 0, 0.0, temp, '', [0,0,0,0,0,0,0,0,0,0])
    

@view
@external
def get_first_product() -> bytes32:
    assert self.exists_account(msg.sender), "You are not authorize"
    return self.products_details[msg.sender][0].pk

@view
@external
def get_last_product() -> bytes32:
    assert self.exists_account(msg.sender), "You are not authorize"
    return self.products_details[msg.sender][self.accounts_details[msg.sender].product_index - 1].pk

