mapping = {
    "StatefulPartitionedCall/ME_RVTDNN/expert0_layer0/MatMul": {
        "core_allocation": 1,
        "spatial_mapping": {'D1': ('K', 32), 'D2': ('C', 64)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
    "StatefulPartitionedCall/ME_RVTDNN/expert0_output/MatMul": {
        "core_allocation": 1,
        "spatial_mapping": {'D1': ('K', 32), 'D2': ('C', 64)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
    "StatefulPartitionedCall/ME_RVTDNN/expert1_layer0/MatMul": {
        "core_allocation": 2,
        "spatial_mapping": {'D1': ('K', 32), 'D2': ('C', 64)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
    "StatefulPartitionedCall/ME_RVTDNN/expert1_output/MatMul": {
        "core_allocation": 2,
        "spatial_mapping": {'D1': ('K', 32), 'D2': ('C', 64)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
}