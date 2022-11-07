"""Tests the WalletBoy class"""

from walletboy import WalletBoy

wallet = WalletBoy("coinbase")


def test_get_price():
    global wallet

    print(wallet.get_price("BTC-USD"))
    print(wallet.get_price("ETH-USD"))


def test_get_balances():
    global wallet

    print(wallet.get_balances())


def test_get_total():
    global wallet

    print(wallet.get_total())


if __name__ == "__main__":
    test_get_price()
    test_get_total()
    test_get_balances()
