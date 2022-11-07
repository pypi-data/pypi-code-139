import mmh3
from bitarray import bitarray
import numpy as np


class BloomFilter:
    """
    capacity: bloom过滤器大小
    hash_size: hash函数个数
    """

    def __init__(self, capacity=1000, hash_size=10):
        self._capacity = capacity
        self._hash_size = hash_size
        self._bit_array = bitarray(self._capacity)
        self._bit_array.setall(0)

    def add(self, element):
        position_list = self._handle_position(str(element))
        for position in position_list:
            self._bit_array[position] = 1

    def query(self, element):
        position_list = self._handle_position(str(element))

        result = True
        for position in position_list:
            result = self._bit_array[position] and result
        return result

    def _handle_position(self, element):
        postion_list = []
        for i in range(self._hash_size):
            index = mmh3.hash(element, i) % self._capacity
            postion_list.append(index)
        return postion_list
