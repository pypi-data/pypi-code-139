mapping = {
    "StatefulPartitionedCall/ME_DNN/expert0_layer0/MatMul": {
        "core_allocation": 1,
        "spatial_mapping": {'D1': ('K', 2), 'D2': ('C', 12)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
    "StatefulPartitionedCall/ME_DNN/expert0_output/MatMul": {
        "core_allocation": 1,
        "spatial_mapping": {'D1': ('K', 2), 'D2': ('C', 12)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },

    "StatefulPartitionedCall/ME_DNN/expert1_layer0/MatMul": {
        "core_allocation": 1,
        "spatial_mapping": {'D1': ('K', 2), 'D2': ('C', 12)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
    "StatefulPartitionedCall/ME_DNN/expert1_output/MatMul": {
        "core_allocation": 1,
        "spatial_mapping": {'D1': ('K', 2), 'D2': ('C', 12)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },

    "StatefulPartitionedCall/ME_DNN/expert2_layer0/MatMul": {
        "core_allocation": 1,
        "spatial_mapping": {'D1': ('K', 2), 'D2': ('C', 12)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
    "StatefulPartitionedCall/ME_DNN/expert2_output/MatMul": {
        "core_allocation": 1,
        "spatial_mapping": {'D1': ('K', 2), 'D2': ('C', 12)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },

    "StatefulPartitionedCall/ME_DNN/gating_layer_0/MatMul": {
        "core_allocation": 1,
        "spatial_mapping": {'D1': ('K', 40), 'D2': ('C', 40)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
    "StatefulPartitionedCall/ME_DNN/gating_layer_output/MatMul": {
        "core_allocation": 2,
        "spatial_mapping": {'D1': ('K', 12), 'D2': ('C', 40)},
        "memory_operand_links": {'O': 'O', 'B': 'I2', 'A': 'I1'}
    },
}