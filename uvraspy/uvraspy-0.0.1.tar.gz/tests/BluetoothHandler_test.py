# test file for BluetoothHandler.py using pytest
from time import sleep

import pytest
from gather.gather import Gather
from database.dbmanager import dbm
bt = pytest.importorskip("bluetooth.BluetoothHandler")


def test_start_stop():
    # start the bluetooth service
    bt.start(None)
    sleep(1)
    bt.stop()


def test_sensordata():
    Gather(dbm)
    bt.start(None)
    # start the bluetooth service
    x = bt.sv.characteristics[1].ReadValue(None)
    assert len(x) > 38  # should have at least 39 bytes

    cryptor = pytest.importorskip("encryption.Cryptor").cryptor
    y = x[:16]
    z = x[16:32]
    x = x[32:]
    x = cryptor.decrypt(x, y, z)

    print(x)
    bt.stop()


buf = b""
def test_analyze():
    import bluetooth.ble as ble
    global buf
    def receive(data):
        global buf
        buf += ble.dbus_array_to_bytes(data)

    # start the bluetooth service
    bt.start(None)
    
    x = ble.dbus_array_to_bytes(bt.sv.characteristics[2].ReadValue({"callback": receive}))
    assert len(x) == 32  # should have exactly 32 bytes
    print(x[:16])
    print(x[16:])
    cryptor = pytest.importorskip("encryption.Cryptor").cryptor
    data = cryptor.decrypt(buf, x[:16], x[16:32])

    print(x)
    print(data[:64])
    buf = b""
    bt.stop()


def test_filter():
    import bluetooth.ble as ble
    global buf
    def receive(data):
        global buf
        buf += ble.dbus_array_to_bytes(data)

    # start the bluetooth service
    bt.start(None)
    filters = b"\0" * 16 + (2).to_bytes(4, 'little') + b"\0" * 8

    cryptor = pytest.importorskip("encryption.Cryptor").cryptor
    # encrypt the filter
    text, y, z = cryptor.encrypt(filters)
    bt.sv.characteristics[2].WriteValue(y + z + text,{})
    
    x = ble.dbus_array_to_bytes(bt.sv.characteristics[2].ReadValue({"callback": receive}))
    sleep(1)
    assert len(x) == 32  # should have exactly 32 bytes
    print("tag: " + str(x[:16]))
    print("nonce" + str(x[16:]))
    print(len(buf))
    data = cryptor.decrypt(buf, x[:16], x[16:32])

    print(x)
    assert len(data) <= 32 * 2
    bt.stop()



def test_preferences():
    # start the bluetooth service
    bt.start(None)
    sleep(1)

    # set the preferences
    preferences = b"22222\0" + b"\1\1\0" + b"\0\0"
    bt.sv.characteristics[4].WriteValue(preferences, None) 

    preferences = b"22222\0" + b"\1\1\0" + b"namen\0" + b"33333\0"
    bt.sv.characteristics[4].WriteValue(preferences, None)

    preferences = b"33333\0" + b"\1\1\0" + b"\0\0"
    bt.sv.characteristics[4].WriteValue(preferences, None)

    preferences = b"33333\0" + b"\2\2\0\0" + b"22222\0"
    bt.sv.characteristics[4].WriteValue(preferences, None)
    
    bt.stop()

    import threading
    for thread in threading.enumerate(): 
        print(thread.name)
    pass
