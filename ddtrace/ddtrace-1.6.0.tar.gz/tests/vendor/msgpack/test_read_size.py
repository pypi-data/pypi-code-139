"""Test Unpacker's read_array_header and read_map_header methods"""
from msgpack import OutOfData
from msgpack import Unpacker

from ddtrace.internal._encoding import packb


UnexpectedTypeException = ValueError


def test_read_array_header():
    unpacker = Unpacker()
    unpacker.feed(packb(["a", "b", "c"]))
    assert unpacker.read_array_header() == 3
    assert unpacker.unpack() == "a"
    assert unpacker.unpack() == "b"
    assert unpacker.unpack() == "c"
    try:
        unpacker.unpack()
        assert 0, "should raise exception"
    except OutOfData:
        assert 1, "okay"


def test_read_map_header():
    unpacker = Unpacker()
    unpacker.feed(packb({"a": "A"}))
    assert unpacker.read_map_header() == 1
    assert unpacker.unpack() == "a"
    assert unpacker.unpack() == "A"
    try:
        unpacker.unpack()
        assert 0, "should raise exception"
    except OutOfData:
        assert 1, "okay"


def test_incorrect_type_array():
    unpacker = Unpacker()
    unpacker.feed(packb(1))
    try:
        unpacker.read_array_header()
        assert 0, "should raise exception"
    except UnexpectedTypeException:
        assert 1, "okay"


def test_incorrect_type_map():
    unpacker = Unpacker()
    unpacker.feed(packb(1))
    try:
        unpacker.read_map_header()
        assert 0, "should raise exception"
    except UnexpectedTypeException:
        assert 1, "okay"


def test_correct_type_nested_array():
    unpacker = Unpacker()
    unpacker.feed(packb({"a": ["b", "c", "d"]}))
    try:
        unpacker.read_array_header()
        assert 0, "should raise exception"
    except UnexpectedTypeException:
        assert 1, "okay"


def test_incorrect_type_nested_map():
    unpacker = Unpacker()
    unpacker.feed(packb([{"a": "b"}]))
    try:
        unpacker.read_map_header()
        assert 0, "should raise exception"
    except UnexpectedTypeException:
        assert 1, "okay"
