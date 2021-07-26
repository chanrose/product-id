from brownie import *

def main():
    accounts.add(config['wallets']['from_key'])
    accounts[-1].deploy(ProductIdentification)
