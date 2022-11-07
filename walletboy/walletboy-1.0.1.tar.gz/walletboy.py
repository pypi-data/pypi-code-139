"""Crypto wallet application"""

__version__ = "1.0.1"

import coinbasepro as cbp
import os
from dotenv import load_dotenv
from decimal import Decimal, ROUND_UP


class WalletBoy:
    def __init__(self, exchange):
        load_dotenv()

        self.exchange = exchange
        self.balances = []
        self.client = None
        self.auth_client = None
        self.keys = {
            "key": os.getenv("API_KEY"),
            "secret": os.getenv("SECRET"),
            "passphrase": os.getenv("PASSPHRASE"),
        }

        self._connect()

    def _connect(self):
        if self.exchange == "coinbase":
            self.client = cbp.PublicClient()
            self.auth_client = cbp.AuthenticatedClient(**self.keys)

    def get_price(self, token):
        """Retrieves the price for specified crypto token"""

        if self.exchange == "coinbase":
            price = self.client.get_product_ticker(token)

        return price["price"]

    def get_balances(self):
        """Get the balance of wallet from exchange"""
        if self.balances:
            return self.balances

        accounts = self.auth_client.get_accounts()

        for account in accounts:
            balance = Decimal(account["balance"]).quantize(Decimal("1.000000"))
            currency = account["currency"]

            if balance > Decimal(0):
                if currency != "USD" and currency != "USDC":
                    usd_value = Decimal(self.get_price(f"{currency}-USD")) * Decimal(
                        balance
                    )
                    usd_value = Decimal(usd_value).quantize(Decimal("1.00"))

                    self.balances.append(
                        {
                            "currency": currency,
                            "balance": balance,
                            "USD": usd_value,
                        }
                    )
                else:
                    usd_value = Decimal(balance).quantize(Decimal("1.00"))
                    self.balances.append(
                        {
                            "currency": currency,
                            "balance": balance,
                            "USD": usd_value,
                        }
                    )

        return self.balances

    def get_total(self):
        """Gets the total amount of the wallet balance"""
        if not self.balances:
            self.get_balances()

        total = Decimal(0)

        for balance in self.balances:
            total = total + Decimal(balance["USD"])

        return total
