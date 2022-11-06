mapping = {
    "StatefulPartitionedCall/RVTDNN/expert0_layer0/MatMul": {
        "core_allocation": 1,
        "spatial_mapping": {'D1': ('K', 64), 'D2': ('C', 64)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
    "StatefulPartitionedCall/RVTDNN/expert0_layer1/MatMul": {
        "core_allocation": 1,
        "spatial_mapping": {'D1': ('K', 64), 'D2': ('C', 64)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
    "StatefulPartitionedCall/RVTDNN/model_output/MatMul": {
        "core_allocation": 1,
        "spatial_mapping": {'D1': ('K', 64), 'D2': ('C', 64)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
}