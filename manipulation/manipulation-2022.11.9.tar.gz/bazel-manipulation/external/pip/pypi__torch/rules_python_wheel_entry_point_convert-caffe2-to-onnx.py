#!/usr/bin/env python3
import sys
from caffe2.python.onnx.bin.conversion import caffe2_to_onnx
if __name__ == "__main__":
    rc = caffe2_to_onnx()
    sys.exit(caffe2_to_onnx())
