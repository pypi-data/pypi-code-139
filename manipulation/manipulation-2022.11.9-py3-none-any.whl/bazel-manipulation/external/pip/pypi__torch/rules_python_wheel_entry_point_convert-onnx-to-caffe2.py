#!/usr/bin/env python3
import sys
from caffe2.python.onnx.bin.conversion import onnx_to_caffe2
if __name__ == "__main__":
    rc = onnx_to_caffe2()
    sys.exit(onnx_to_caffe2())
