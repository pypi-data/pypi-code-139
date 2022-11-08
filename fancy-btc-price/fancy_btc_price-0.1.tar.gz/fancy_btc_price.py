#!/usr/bin/env python3
from requests import get
from datetime import datetime, timedelta
from os.path import basename
from sys import stderr
from click import command, option, IntRange


version='0.1'


class BtcPrice():


    url = 'https://api.moneyonchain.com/api/measurement/mocMainnet2'
    no_available_symbol = "ⁿ/ₐ"
    warrinig_symbol = '⚠'
    bitcoin_symbol = "₿"


    def __init__(self, max_age=timedelta(minutes=3), verbose=lambda x: None):
        self._value = None
        self._time = None
        self.max_age = max_age
        self.verbose = verbose
        self.verbose(f'Start, parameters url={self.url} max_age={self.max_age}')


    @staticmethod
    def to_str(o):
        return o if o is not None else 'N/A'


    @property
    def value(self):
        out = self._value
        self.verbose(f"Data value: {self.to_str(out)}")
        return out 


    @property
    def time(self):
        out = self._time
        self.verbose(f"Data time: {self.to_str(out)}")
        return out 


    @property
    def age(self):
        out = None if self._time is None else datetime.utcnow() - self._time
        self.verbose(f"Data age: {self.to_str(out)}")
        return out 


    @property
    def age_warning(self):
        age = self.age
        out = age is None or age > self.max_age
        self.verbose(f"Data age warning: {'Yes' if out else 'No'}")
        return out


    def gather(self):

        try:
            data = get(self.url).json()
            value = float(data['btc_price'])
            time = datetime.fromisoformat(data['time'])
        except:
            value = None
            time = None

        if not value:
            value = None

        self.verbose(f"Gather data, value={self.to_str(value)} time={self.to_str(time)}")

        self._value = value
        self._time = time


    def __bool__(self):
        out = bool(self._value and self._time)
        self.verbose(f"Data is valid: {'Yes' if out else 'No'}")
        return out


    def __del__(self):
        self.verbose(f"Bye!")


    def __str__(self):

        self.gather()

        self.verbose(f"Format data into string...")

        out = f"1{self.bitcoin_symbol}={self.no_available_symbol}"
        if self:
            value = self.value
            value = value if value < 1000 else int(value)
            if self.age_warning:
                out = f"1{self.bitcoin_symbol}={value}$ {self.warrinig_symbol}"
            else:
                out = f"1{self.bitcoin_symbol}={value}$"

        self.verbose(f"Output string: {repr(out)}")

        return out


@command()
@option('-v', '--verbose', is_flag=True,
    help='Enables verbose mode')
@option('--version', 'show_version', is_flag=True,
    help='Show version and exit')
@option('-m', '--max-age', type=IntRange(1, 120), default=3, show_default=True,
    help="Max price age without showing a warning (in minutes)")
def cli(max_age=3, verbose=False, show_version=False):
    """Simple program that shows the BTC price

    Taken from the Money on Chain API Rest (moneyonchain.com)"""

    if show_version:
        print(version)
        return

    if verbose:
        verbose_fnc=lambda x: print(
            f"{basename(__file__)}\t{datetime.now()}\t{x}", file=stderr)
    else:
        verbose_fnc=lambda x: None

    btc_price = BtcPrice(max_age=timedelta(minutes=max_age), verbose=verbose_fnc)

    print(btc_price)

    if not btc_price:
        exit(1)


if __name__ == '__main__':
    cli()
