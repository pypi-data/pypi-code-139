mapping = {
    "StatefulPartitionedCall/ME_RVTDNN/expert0_layer0/MatMul": {
        "core_allocation": 1,
        "spatial_mapping": {'D1': ('K', 16), 'D2': ('C', 32)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
    "StatefulPartitionedCall/ME_RVTDNN/expert0_output/MatMul": {
        "core_allocation": 2,
        "spatial_mapping": {'D1': ('K', 16), 'D2': ('C', 32)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
    "StatefulPartitionedCall/ME_RVTDNN/expert1_layer0/MatMul": {
        "core_allocation": 3,
        "spatial_mapping": {'D1': ('K', 16), 'D2': ('C', 32)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
    "StatefulPartitionedCall/ME_RVTDNN/expert1_output/MatMul": {
        "core_allocation": 4,
        "spatial_mapping": {'D1': ('K', 16), 'D2': ('C', 32)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
}