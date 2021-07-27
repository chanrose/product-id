import pytest, brownie
import datetime

@pytest.fixture(scope='module', autouse=True)
def pid(ProductIdentification, accounts):
    pid_contract = ProductIdentification.deploy({'from': accounts[0]})
    yield pid_contract

@pytest.fixture(autouse=True)
def isolate(fn_isolation):
    pass

def register_company_account(contract, accounts, name, pk, password, owner=0):
    contract.register_company_account(
        name, 
        pk, 
        password, 
        {'from':accounts[owner]}
    )
    assert contract.get_company_account_name() == name

def get_secret_key(contract, accounts, password, owner=0):
    assert contract.get_secret_key(password, {'from':accounts[owner]}) == '86bd8dc76256e242240332d8133c2c8778a4600ca90b21f220c443ba8fd4d653'

def register_product(contract, accounts, pk, name, category, release_year, price, country, description, serial_list, owner=0):
    assert contract.get_company_account_name() == '0x47616c617879'
    contract.register_product(
        pk,
        name,
        category,
        release_year,
        price,
        country,
        description,
        serial_list,
        {'from':accounts[owner]}
    )

def get_list_of_product_pk(contract, accounts, pk, pk_list = [i for i in range(1000)], owner=0):
    assert contract.get_company_account_name() == '0x47616c617879'
    assert contract.get_list_of_products(pk_list, {'from':accounts[owner]})[0] == pk

def get_product_detail(contract, accounts, pk, pk_list = [i for i in range(1000)], owner=0):
    assert contract.get_company_account_name() == '0x47616c617879'
    assert contract.get_list_of_products(pk_list)[0] == pk
    assert contract.get_product_prop(pk, {'from': accounts[owner]})

def update_product(contract, accounts, pk, name, category, price, description, pk_list = [i for i in range(1000)], owner=0):
    assert contract.get_company_account_name() == '0x47616c617879'
    assert contract.get_list_of_products(pk_list)[0] == pk
    contract.update_product(
        pk,
        name,
        category,
        price,
        description,
        {'from':accounts[owner]}
    )

def get_first_product(contract, accounts, pk, owner=0):
    assert contract.get_company_account_name() == '0x47616c617879'
    assert contract.get_first_product({'from':accounts[owner]}) == pk

def get_last_product(contract, accounts, pk, owner=0):
    assert contract.get_company_account_name() == '0x47616c617879'
    assert contract.get_last_product({'from':accounts[owner]}) == pk

    

#*************************** test *************************************

def test_register_company_account(pid, accounts):
    register_company_account(
        pid, 
        accounts, 
        '0x47616c617879', 
        '86bd8dc76256e242240332d8133c2c8778a4600ca90b21f220c443ba8fd4d653', 
        '0x0190732A8203a0FE4a91052A8AB6A35624E054F1',
    )

def test_register_product(pid, accounts):
    register_company_account(
        pid, 
        accounts, 
        '0x47616c617879', 
        '86bd8dc76256e242240332d8133c2c8778a4600ca90b21f220c443ba8fd4d653', 
        '0x0190732A8203a0FE4a91052A8AB6A35624E054F1',
        0
    )
    register_product(
        pid,
        accounts,
        '0x6b6579',
        '0x53616d73756e67',
        '0x50686f6e65',
        2021,
        500.00,
        '0x546861696c616e64',
        'This is a smart phone from Thailand',
        [1, 2, 3, 4, 5, 6, 7, 0, 0 ,0]
    )

def test_get_secret_key(pid, accounts):
    register_company_account(
        pid, 
        accounts, 
        '0x47616c617879', 
        '86bd8dc76256e242240332d8133c2c8778a4600ca90b21f220c443ba8fd4d653', 
        '0x0190732A8203a0FE4a91052A8AB6A35624E054F1',
        0
    )
    get_secret_key(pid, accounts, '0x0190732A8203a0FE4a91052A8AB6A35624E054F1')

def test_get_list_of_product_pk(pid, accounts):
    register_company_account(
        pid, 
        accounts, 
        '0x47616c617879', 
        '86bd8dc76256e242240332d8133c2c8778a4600ca90b21f220c443ba8fd4d653', 
        '0x0190732A8203a0FE4a91052A8AB6A35624E054F1',
        0
    )
    register_product(
        pid,
        accounts,
        '0x6b6579',
        '0x53616d73756e67',
        '0x50686f6e65',
         2021,
         500.00,
        '0x546861696c616e64',
        'This is a smart phone from Thailand',
        [1, 2, 3, 4, 5, 6, 7, 0, 0 ,0]    
    )
    get_list_of_product_pk(pid, accounts, '0x6b6579')


def test_get_product_detail(pid, accounts):
    register_company_account(
        pid, 
        accounts, 
        '0x47616c617879', 
        '86bd8dc76256e242240332d8133c2c8778a4600ca90b21f220c443ba8fd4d653', 
        '0x0190732A8203a0FE4a91052A8AB6A35624E054F1',
        0
    )
    register_product(
        pid,
        accounts,
        '0x6b6579',
        '0x53616d73756e67',
        '0x50686f6e65',
         2021,
         500.00,
        '0x546861696c616e64',
        'This is a smart phone from Thailand',
        [1, 2, 3, 4, 5, 6, 7, 0, 0 ,0]    
    )
    get_product_detail(pid, accounts, '0x6b6579')

def test_update_product(pid, accounts):
    register_company_account(
        pid, 
        accounts, 
        '0x47616c617879', 
        '86bd8dc76256e242240332d8133c2c8778a4600ca90b21f220c443ba8fd4d653', 
        '0x0190732A8203a0FE4a91052A8AB6A35624E054F1',
        0
    )
    register_product(
        pid,
        accounts,
        '0x6b6579',
        '0x53616d73756e67',
        '0x50686f6e65',
         2021,
         500.00,
        '0x546861696c616e64',
        'This is a smart phone from Thailand',
        [1, 2, 3, 4, 5, 6, 7, 0, 0 ,0]    
    )
    update_product(
        pid,
        accounts,
        '0x6b6579',
        '0x4970686f6e65',
        '0x50686f6e65',
         550.00,
        'This is an Iphone from USA'
    )

def test_get_first_product(pid, accounts):
    register_company_account(
        pid, 
        accounts, 
        '0x47616c617879', 
        '86bd8dc76256e242240332d8133c2c8778a4600ca90b21f220c443ba8fd4d653', 
        '0x0190732A8203a0FE4a91052A8AB6A35624E054F1',
        0
    )
    register_product(
        pid,
        accounts,
        '0x6b6579',
        '0x53616d73756e67',
        '0x50686f6e65',
         2021,
         500.00,
        '0x546861696c616e64',
        'This is a smart phone from Thailand',
        [1, 2, 3, 4, 5, 6, 7, 0, 0 ,0]    
    )
    register_product(
        pid,
        accounts,
        '0x636f6d70757465726b6579',
        '0x4850',
        '0x436f6d7075746572',
         2021,
         900.00,
        '0x48502d73657269616c2d636f6465',
        'This is a HP Computer from Thailand',
        [1, 2, 3, 4, 5, 6, 7, 9, 9 ,0]    
    )
    get_first_product(pid, accounts, '0x6b6579')

def test_get_last_product(pid, accounts):
    register_company_account(
        pid, 
        accounts, 
        '0x47616c617879', 
        '86bd8dc76256e242240332d8133c2c8778a4600ca90b21f220c443ba8fd4d653', 
        '0x0190732A8203a0FE4a91052A8AB6A35624E054F1',
        0
    )
    register_product(
        pid,
        accounts,
        '0x6b6579',
        '0x53616d73756e67',
        '0x50686f6e65',
         2021,
         500.00,
        '0x546861696c616e64',
        'This is a smart phone from Thailand',
        [1, 2, 3, 4, 5, 6, 7, 0, 0 ,0]    
    )
    register_product(
        pid,
        accounts,
        '0x636f6d70757465726b6579',
        '0x4850',
        '0x436f6d7075746572',
         2021,
         900.00,
        '0x48502d73657269616c2d636f6465',
        'This is a HP Computer from Thailand',
        [1, 2, 3, 4, 5, 6, 7, 9, 9 ,0]    
    )
    get_last_product(pid, accounts, '0x636f6d70757465726b6579')