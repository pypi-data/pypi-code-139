from rust_circuit import (
    Add as rAdd,
    ScalarConstant as rScalarConstant,
    Rearrange as rRearrange,
    RearrangeSpec as rRearrangeSpec,
    ArrayConstant as rArrayConstant,
    compiler_simp,
    compiler_simp_until_same,
    strip_names,
    deep_canonicalize,
    deep_maybe_distribute,
    deep_optimize_einsums,
    optimize_circuit,
    count_nodes as r_count_nodes,
    scheduled_evaluate,
    optimize_and_evaluate,
    OptimizationSettings,
    deep_heuristic_nest_adds,
)
from interp.circuit.circuit import MemoizedFn
from interp.circuit.circuit_compiler.compiler import evaluate_circuit
import torch
from interp.circuit.circuit_compiler.canonical_ast import (
    ast_count_nodes,
    circuit_to_canonical_ast,
    optimize_with_backreferences,
    print_ast_deep,
)
from interp.circuit.circuit_compiler.util import FrozenDict, oom_fmt
from interp.circuit.circuit_utils import cast_circuit, count_nodes, evaluate_fn
from interp.circuit.computational_node import (
    Add,
    Concat,
    Einsum,
    GeneralFunction,
    Index,
    UnaryRearrange,
    log_softmax_fn,
    relu,
    sigmoid,
    sigmoid_fn,
    softmax,
    softmax_fn,
    rsqrt_fn,
    softmax_jacobian,
    reciprocal_jacobian,
    log_exp_p_1_fn,
    sigmoid_jacobian,
    log_exp_p_1_jacobian,
    rsqrt_jacobian,
    reciprocal_fn,
)  # imports used in eval
from interp.circuit.var import AutoTag
from interp.circuit.constant import ArrayConstant, Constant, FloatConstant, One, Zero
from interp.circuit.interop_rust.interop_rust import py_to_rust, rust_to_py
from uuid import UUID
from interp.tools.perf_timer import catchtime

x1 = rRearrange(
    rAdd(
        rArrayConstant(torch.randn((2,))),
        rRearrange(
            rRearrange(rScalarConstant(1.0, ()), rRearrangeSpec([], [[0]], [2])),
            rRearrangeSpec([[0]], [[0], [1]], [None, 2]),
        ),
    ),
    rRearrangeSpec([[0], [1]], [[0], [1], [2]], [None, None, 2]),
)
x1_s = compiler_simp(deep_canonicalize(x1))
x1_s.compiler_print()
nb_example = eval(
    """
(lambda c17: (lambda c16: (lambda c14: (lambda c15: (lambda c11: (lambda c10: (lambda c13: (lambda c12: (lambda c9: (lambda c2: (lambda c8: (lambda c1: (lambda c7: (lambda c3: (lambda c4: (lambda c0: (lambda c6: (lambda c5: Add(items=FrozenDict({Einsum(args=((Einsum(args=((Einsum(args=((c3, (0,)), (Add(items=FrozenDict({UnaryRearrange(node=Einsum(args=((c6, (0,)), (Add(items=FrozenDict({UnaryRearrange(node=One(shape=(8192,), name='one_sample'), op_string='b0 -> b0', axes_lengths=(), name='one_sample_rearrange_for_add_0', shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=c4, op_string='b0 -> b0', axes_lengths=(), name='is_p_var_sample_rearrange_for_add_1', shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): -1.0}), name='is_q_var_sample', shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0,))), out_axes=(0,), name='logit_diff_times_correct_sample', shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 -> b0', axes_lengths=(), name='logit_diff_times_correct_sample_rearrange_for_add_0', shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=GeneralFunction(node=c6, function=log_exp_p_1_fn, get_jacobian=log_exp_p_1_jacobian, name='logit_diff_log_exp_p_1_sample', allows_batching=True, non_batch_dims=(), shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 -> b0', axes_lengths=(), name='logit_diff_log_exp_p_1_sample_rearrange_for_add_1', shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): -1.0}), name='log_loss_sample', shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0,))), out_axes=(), name='log_loss_sample_sample_expectation', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), ()), (c1, ())), out_axes=(), name='ScalarMul', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), ()),), out_axes=(), name='Ein', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, Einsum(args=((UnaryRearrange(node=Einsum(args=((Einsum(args=((c3, (0,)), (GeneralFunction(node=c6, function=sigmoid_fn, get_jacobian=sigmoid_jacobian, name='logit_diff_sigmoid_sample', allows_batching=True, non_batch_dims=(), shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0,))), out_axes=(), name='logit_diff_sigmoid_sample_sample_expectation', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), ()), (c1, ())), out_axes=(), name='ScalarMul', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string=' -> ', axes_lengths=(), name='I k1 logit_diff_sigmoid I perm', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), ()),), out_axes=(), name='Ein', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, Einsum(args=((Einsum(args=((Einsum(args=((Add(items=FrozenDict({Einsum(args=((c3, (0,)), (Einsum(args=((c5, (0,)), (c5, (0,))), out_axes=(0,), name='outer_sample', shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0,))), out_axes=(), name='outer_sample_sample_expectation', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='is_it_p_variance_decompose', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), ()), (c1, ())), out_axes=(), name='ScalarMul', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), ()), (c1, ())), out_axes=(), name='ScalarMul', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), ()),), out_axes=(), name='Ein', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, Einsum(args=((Einsum(args=((c0, ()), (c1, ())), out_axes=(), name='ScalarMul', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), ()),), out_axes=(), name='Ein', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='Add', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True))(Add(items=FrozenDict({UnaryRearrange(node=c4, op_string='b0 -> b0', axes_lengths=(), name='is_p_var_sample_rearrange_for_add_0', shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=UnaryRearrange(node=c0, op_string=' -> 8192', axes_lengths=(), name='is_p_var_sample_sample_expectation_sample', shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 -> b0', axes_lengths=(), name='is_p_var_sample_sample_expectation_sample_rearrange_for_add_1', shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): -1.0}), name='is_p_var_centered_sample', shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(Index(node=Add(items=FrozenDict({UnaryRearrange(node=Einsum(args=((c7, (0, 1, 2)), (UnaryRearrange(node=Index(node=c8, index=(30, slice(None, None, None)), name='w.unembed_q_mark', hash_tensor_idx_by_value=False, shape=(256,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='a -> 8192 a', axes_lengths=(), name='w.unembed_q_mark_sample', shape=(8192, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 2))), out_axes=(0, 1), name='logits_q_mark_sample', shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 -> b0 a0', axes_lengths=(), name='logits_q_mark_sample_rearrange_for_add_0', shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=Einsum(args=((c7, (0, 1, 2)), (UnaryRearrange(node=Index(node=c8, index=(13, slice(None, None, None)), name='w.unembed_period', hash_tensor_idx_by_value=False, shape=(256,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='a -> 8192 a', axes_lengths=(), name='w.unembed_period_sample', shape=(8192, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 2))), out_axes=(0, 1), name='logits_period_sample', shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 -> b0 a0', axes_lengths=(), name='logits_period_sample_rearrange_for_add_1', shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): -1.0}), name='logit_diff_all_seq_sample', shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), index=(slice(None, None, None), -1), name='logit_diff_sample', hash_tensor_idx_by_value=False, shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(Einsum(args=((c3, (0,)), (c4, (0,))), out_axes=(), name='is_p_var_sample_sample_expectation', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(Index(node=ArrayConstant(value=torch.randn(torch.Size([48110])), shape=(48110,), uuid=UUID('dfe273fe-ae36-45fd-b32d-97eaa2556223'), name='is_p'), index=(torch.randint(1,48094,torch.Size([8192])),), name='is_p_var_sample', hash_tensor_idx_by_value=False, shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(Einsum(args=((c2, (0,)), (GeneralFunction(node=c1, function=reciprocal_fn, get_jacobian=reciprocal_jacobian, name='Ein_recip', allows_batching=True, non_batch_dims=(), shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), ())), out_axes=(0,), name='ScalarMul', shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(Add(items=FrozenDict({UnaryRearrange(node=ArrayConstant(value=torch.randn(torch.Size([256])), shape=(8192, 256), uuid=UUID('a3d94a03-5e58-4253-bef7-bb424a117c21'), name='final.n.w.bias_sample'), op_string='b0 a0 -> b0 o0 a0', axes_lengths=(('o0', 1),), name='final.n.w.bias_sample_rearrange_for_add_0', shape=(8192, 1, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=Einsum(args=((Einsum(args=((c9, (0, 1, 2)), (ArrayConstant(value=torch.randn(torch.Size([256])), shape=(8192, 256), uuid=UUID('ef0b3f2f-cdb5-414a-9f9e-e80eec300d86'), name='final.n.w.scale_sample'), (0, 2))), out_axes=(0, 1, 2), name='final.n.y_scale_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 2)), (GeneralFunction(node=Add(items=FrozenDict({UnaryRearrange(node=Einsum(args=((c9, (0, 1, 2)), (c9, (0, 1, 2)), (FloatConstant(value=0.00390625, shape=(8192,), name='final.n.c.recip_h_size_sample'), (0,))), out_axes=(0, 1), name='final.n.var_sample', shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 -> b0 a0', axes_lengths=(), name='final.n.var_sample_rearrange_for_add_0', shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=FloatConstant(value=1e-05, shape=(8192,), name='final.n.eps_sample'), op_string='b0 -> b0 o0', axes_lengths=(('o0', 1),), name='final.n.eps_sample_rearrange_for_add_1', shape=(8192, 1), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='final.n.c.var_p_eps_sample', shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), function=rsqrt_fn, get_jacobian=rsqrt_jacobian, name='final.n.full_mul_sample', allows_batching=True, non_batch_dims=(), shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1))), out_axes=(0, 1, 2), name='final.n.y_out_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 -> b0 a0 a1', axes_lengths=(), name='final.n.y_out_sample_rearrange_for_add_1', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='final.n_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(Einsum(args=((c2, (0,)),), out_axes=(), name='Ein', shape=(), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(ArrayConstant(value=torch.randn(torch.Size([50259, 256])), shape=(50259, 256), uuid=UUID('af1caa2f-85d3-462f-8efe-f02dd1491924'), name='w.unembed')))(Einsum(args=((Index(node=AutoTag(node=FloatConstant(value=2.0785699438786117e-05, shape=(48110,), name='uniform_probs'), uuid=UUID('43012443-725a-4f51-aa91-2310a20c8db4'), name='uniform_probs_and_group'), index=(torch.randint(1,48094,torch.Size([8192])),), name='uniform_probs_and_group_importance_sample_idxed_probs', hash_tensor_idx_by_value=False, shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0,)), (ArrayConstant(value=torch.randn(torch.Size([8192])), shape=(8192,), uuid=UUID('453a0a27-3c62-482a-b0b5-c5dde5099c67'), name='importance_sample_recip_sample_weights'), (0,))), out_axes=(0,), name='uniform_probs_and_group_importance_sample_weights', shape=(8192,), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(Einsum(args=((Add(items=FrozenDict({c10: 1.0, c11: 1.0, UnaryRearrange(node=Einsum(args=((Einsum(args=((GeneralFunction(node=Add(items=FrozenDict({UnaryRearrange(node=Einsum(args=((Einsum(args=((Add(items=FrozenDict({UnaryRearrange(node=Einsum(args=((ArrayConstant(value=torch.randn(torch.Size([8, 32, 256])), shape=(8192, 8, 32, 256), uuid=UUID('04680ebd-ca99-4597-80b4-9fcdfb4f541d'), name='a1.w.q_sample'), (0, 1, 2, 3)), (c12, (0, 4, 3))), out_axes=(0, 1, 4, 2), name='a1.q_sample', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 a2 -> b0 a0 a1 a2', axes_lengths=(), name='a1.q_sample_rearrange_for_add_0', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=UnaryRearrange(node=Einsum(args=((ArrayConstant(value=torch.randn(torch.Size([8, 32, 256])), shape=(8, 32, 256), uuid=UUID('04680ebd-ca99-4597-80b4-9fcdfb4f541d'), name='a1.w.q'), (0, 1, 2)), (c14, (3, 2))), out_axes=(0, 3, 1), name='a1.w.pos_q', shape=(8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='a b c -> 8192 a b c', axes_lengths=(), name='a1.w.pos_q_sample', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 a2 -> b0 a0 a1 a2', axes_lengths=(), name='a1.w.pos_q_sample_rearrange_for_add_1', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='a1.f_q_sample', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 2, 3)), (Add(items=FrozenDict({UnaryRearrange(node=Einsum(args=((ArrayConstant(value=torch.randn(torch.Size([8, 32, 256])), shape=(8192, 8, 32, 256), uuid=UUID('4c311ff7-6006-4f1b-8df0-0df38a352e5d'), name='a1.w.k_sample'), (0, 1, 2, 3)), (c12, (0, 4, 3))), out_axes=(0, 1, 4, 2), name='a1.k_sample', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 a2 -> b0 a0 a1 a2', axes_lengths=(), name='a1.k_sample_rearrange_for_add_0', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=UnaryRearrange(node=Einsum(args=((ArrayConstant(value=torch.randn(torch.Size([8, 32, 256])), shape=(8, 32, 256), uuid=UUID('4c311ff7-6006-4f1b-8df0-0df38a352e5d'), name='a1.w.k'), (0, 1, 2)), (c14, (3, 2))), out_axes=(0, 3, 1), name='a1.w.pos_k', shape=(8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='a b c -> 8192 a b c', axes_lengths=(), name='a1.w.pos_k_sample', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 a2 -> b0 a0 a1 a2', axes_lengths=(), name='a1.w.pos_k_sample_rearrange_for_add_1', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='a1.f_k_sample', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 4, 3)), (FloatConstant(value=0.17677669529663687, shape=(8192,), name='a1.c.div_head_size_sample'), (0,))), out_axes=(0, 1, 2, 4), name='a1.scores_not_masked_sample', shape=(8192, 8, 35, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 2, 3)), (ArrayConstant(value=torch.randn(torch.Size([35, 35])), shape=(8192, 35, 35), uuid=UUID('8923e0b9-aec5-4117-909d-92e59f0da512'), name='a1.c.score_mask_sample'), (0, 2, 3))), out_axes=(0, 1, 2, 3), name='a1.scores_mul_mask_sample', shape=(8192, 8, 35, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 a2 -> b0 a0 a1 a2', axes_lengths=(), name='a1.scores_mul_mask_sample_rearrange_for_add_0', shape=(8192, 8, 35, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=ArrayConstant(value=torch.randn(torch.Size([35, 35])), shape=(8192, 35, 35), uuid=UUID('2a2d96ec-b792-4c3d-8942-f02804ae5da0'), name='a1.c.score_neg_inf_bias_sample'), op_string='b0 a0 a1 -> b0 o0 a0 a1', axes_lengths=(('o0', 1),), name='a1.c.score_neg_inf_bias_sample_rearrange_for_add_1', shape=(8192, 1, 35, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='a1.scores_sample', shape=(8192, 8, 35, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), function=softmax_fn, get_jacobian=softmax_jacobian, name='a1.probs_sample', allows_batching=True, non_batch_dims=(-1,), shape=(8192, 8, 35, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 2, 3)), (Einsum(args=((ArrayConstant(value=torch.randn(torch.Size([8, 32, 256])), shape=(8192, 8, 32, 256), uuid=UUID('30181721-36a6-4d46-b87b-4e87aea6aeef'), name='a1.w.v_sample'), (0, 1, 2, 3)), (c12, (0, 4, 3))), out_axes=(0, 1, 4, 2), name='a1.v_sample', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 3, 4))), out_axes=(0, 2, 1, 4), name='a1.comb_v_sample', shape=(8192, 35, 8, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 2, 3)), (ArrayConstant(value=torch.randn(torch.Size([8, 32, 256])), shape=(8192, 8, 32, 256), uuid=UUID('67abd9d5-cb28-488e-916d-6e6aea3b4ca8'), name='a1.w.out_sample'), (0, 2, 3, 4))), out_axes=(0, 1, 4), name='a1_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 -> b0 a0 a1', axes_lengths=(), name='a1_sample_rearrange_for_add_2', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='final.inp_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 2)), (ArrayConstant(value=torch.randn(torch.Size([256, 256])), shape=(8192, 256, 256), uuid=UUID('9bd04993-d6d5-46c8-8265-6d6db412d94b'), name='final.n.c.sub_mean_sample'), (0, 2, 3))), out_axes=(0, 1, 3), name='final.n.z_mean_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(Add(items=FrozenDict({UnaryRearrange(node=ArrayConstant(value=torch.randn(torch.Size([256])), shape=(8192, 256), uuid=UUID('08cfad93-cdc4-446a-bd10-ffa8e2ec7177'), name='a1.n.w.bias_sample'), op_string='b0 a0 -> b0 o0 a0', axes_lengths=(('o0', 1),), name='a1.n.w.bias_sample_rearrange_for_add_0', shape=(8192, 1, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=Einsum(args=((Einsum(args=((c13, (0, 1, 2)), (ArrayConstant(value=torch.randn(torch.Size([256])), shape=(8192, 256), uuid=UUID('b39cc991-01a2-4355-b6f1-ffe85444ee6a'), name='a1.n.w.scale_sample'), (0, 2))), out_axes=(0, 1, 2), name='a1.n.y_scale_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 2)), (GeneralFunction(node=Add(items=FrozenDict({UnaryRearrange(node=Einsum(args=((c13, (0, 1, 2)), (c13, (0, 1, 2)), (FloatConstant(value=0.00390625, shape=(8192,), name='a1.n.c.recip_h_size_sample'), (0,))), out_axes=(0, 1), name='a1.n.var_sample', shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 -> b0 a0', axes_lengths=(), name='a1.n.var_sample_rearrange_for_add_0', shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=FloatConstant(value=1e-05, shape=(8192,), name='a1.n.eps_sample'), op_string='b0 -> b0 o0', axes_lengths=(('o0', 1),), name='a1.n.eps_sample_rearrange_for_add_1', shape=(8192, 1), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='a1.n.c.var_p_eps_sample', shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), function=rsqrt_fn, get_jacobian=rsqrt_jacobian, name='a1.n.full_mul_sample', allows_batching=True, non_batch_dims=(), shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1))), out_axes=(0, 1, 2), name='a1.n.y_out_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 -> b0 a0 a1', axes_lengths=(), name='a1.n.y_out_sample_rearrange_for_add_1', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='a1.n_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(Einsum(args=((Add(items=FrozenDict({c10: 1.0, c11: 1.0}), name='a1.inp_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 2)), (ArrayConstant(value=torch.randn(torch.Size([256, 256])), shape=(8192, 256, 256), uuid=UUID('15dad660-1d78-4801-96de-9bfed51d4948'), name='a1.n.c.sub_mean_sample'), (0, 2, 3))), out_axes=(0, 1, 3), name='a1.n.z_mean_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(UnaryRearrange(node=c17, op_string='b0 a0 a1 -> b0 a0 a1', axes_lengths=(), name='embed_var_sample_rearrange_for_add_0', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(UnaryRearrange(node=Einsum(args=((Einsum(args=((GeneralFunction(node=Add(items=FrozenDict({UnaryRearrange(node=Einsum(args=((Einsum(args=((Add(items=FrozenDict({UnaryRearrange(node=Einsum(args=((ArrayConstant(value=torch.randn(torch.Size([8, 32, 256])), shape=(8192, 8, 32, 256), uuid=UUID('a3982e07-149f-4c74-a4e5-20bc7f599ef9'), name='a0.w.q_sample'), (0, 1, 2, 3)), (c15, (0, 4, 3))), out_axes=(0, 1, 4, 2), name='a0.q_sample', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 a2 -> b0 a0 a1 a2', axes_lengths=(), name='a0.q_sample_rearrange_for_add_0', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=UnaryRearrange(node=Einsum(args=((ArrayConstant(value=torch.randn(torch.Size([8, 32, 256])), shape=(8, 32, 256), uuid=UUID('a3982e07-149f-4c74-a4e5-20bc7f599ef9'), name='a0.w.q'), (0, 1, 2)), (c14, (3, 2))), out_axes=(0, 3, 1), name='a0.w.pos_q', shape=(8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='a b c -> 8192 a b c', axes_lengths=(), name='a0.w.pos_q_sample', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 a2 -> b0 a0 a1 a2', axes_lengths=(), name='a0.w.pos_q_sample_rearrange_for_add_1', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='a0.f_q_sample', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 2, 3)), (Add(items=FrozenDict({UnaryRearrange(node=Einsum(args=((ArrayConstant(value=torch.randn(torch.Size([8, 32, 256])), shape=(8192, 8, 32, 256), uuid=UUID('f03fd2a7-a276-4c9c-afd5-d0d0914861b8'), name='a0.w.k_sample'), (0, 1, 2, 3)), (c15, (0, 4, 3))), out_axes=(0, 1, 4, 2), name='a0.k_sample', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 a2 -> b0 a0 a1 a2', axes_lengths=(), name='a0.k_sample_rearrange_for_add_0', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=UnaryRearrange(node=Einsum(args=((ArrayConstant(value=torch.randn(torch.Size([8, 32, 256])), shape=(8, 32, 256), uuid=UUID('f03fd2a7-a276-4c9c-afd5-d0d0914861b8'), name='a0.w.k'), (0, 1, 2)), (c14, (3, 2))), out_axes=(0, 3, 1), name='a0.w.pos_k', shape=(8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='a b c -> 8192 a b c', axes_lengths=(), name='a0.w.pos_k_sample', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 a2 -> b0 a0 a1 a2', axes_lengths=(), name='a0.w.pos_k_sample_rearrange_for_add_1', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='a0.f_k_sample', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 4, 3)), (FloatConstant(value=0.17677669529663687, shape=(8192,), name='a0.c.div_head_size_sample'), (0,))), out_axes=(0, 1, 2, 4), name='a0.scores_not_masked_sample', shape=(8192, 8, 35, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 2, 3)), (ArrayConstant(value=torch.randn(torch.Size([35, 35])), shape=(8192, 35, 35), uuid=UUID('251501a5-b371-42e4-8853-887bba31173c'), name='a0.c.score_mask_sample'), (0, 2, 3))), out_axes=(0, 1, 2, 3), name='a0.scores_mul_mask_sample', shape=(8192, 8, 35, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 a2 -> b0 a0 a1 a2', axes_lengths=(), name='a0.scores_mul_mask_sample_rearrange_for_add_0', shape=(8192, 8, 35, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=ArrayConstant(value=torch.randn(torch.Size([35, 35])), shape=(8192, 35, 35), uuid=UUID('09bec2c1-91bd-48c1-a940-3536620bfad8'), name='a0.c.score_neg_inf_bias_sample'), op_string='b0 a0 a1 -> b0 o0 a0 a1', axes_lengths=(('o0', 1),), name='a0.c.score_neg_inf_bias_sample_rearrange_for_add_1', shape=(8192, 1, 35, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='a0.scores_sample', shape=(8192, 8, 35, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), function=softmax_fn, get_jacobian=softmax_jacobian, name='a0.probs_sample', allows_batching=True, non_batch_dims=(-1,), shape=(8192, 8, 35, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 2, 3)), (Einsum(args=((ArrayConstant(value=torch.randn(torch.Size([8, 32, 256])), shape=(8192, 8, 32, 256), uuid=UUID('1b4daf99-41df-43e3-a390-25abda812c6e'), name='a0.w.v_sample'), (0, 1, 2, 3)), (c15, (0, 4, 3))), out_axes=(0, 1, 4, 2), name='a0.v_sample', shape=(8192, 8, 35, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 3, 4))), out_axes=(0, 2, 1, 4), name='a0.comb_v_sample', shape=(8192, 35, 8, 32), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 2, 3)), (ArrayConstant(value=torch.randn(torch.Size([8, 32, 256])), shape=(8192, 8, 32, 256), uuid=UUID('80972fcd-7330-47d2-a0a4-b6ce8b2b3f0f'), name='a0.w.out_sample'), (0, 2, 3, 4))), out_axes=(0, 1, 4), name='a0_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 -> b0 a0 a1', axes_lengths=(), name='a0_sample_rearrange_for_add_1', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(Add(items=FrozenDict({UnaryRearrange(node=ArrayConstant(value=torch.randn(torch.Size([256])), shape=(8192, 256), uuid=UUID('c9c9b86e-0121-4186-bc51-90bc4309bdd3'), name='a0.n.w.bias_sample'), op_string='b0 a0 -> b0 o0 a0', axes_lengths=(('o0', 1),), name='a0.n.w.bias_sample_rearrange_for_add_0', shape=(8192, 1, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=Einsum(args=((Einsum(args=((c16, (0, 1, 2)), (ArrayConstant(value=torch.randn(torch.Size([256])), shape=(8192, 256), uuid=UUID('340f89bc-c0de-4869-abc1-b30ab43dc551'), name='a0.n.w.scale_sample'), (0, 2))), out_axes=(0, 1, 2), name='a0.n.y_scale_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1, 2)), (GeneralFunction(node=Add(items=FrozenDict({UnaryRearrange(node=Einsum(args=((c16, (0, 1, 2)), (c16, (0, 1, 2)), (FloatConstant(value=0.00390625, shape=(8192,), name='a0.n.c.recip_h_size_sample'), (0,))), out_axes=(0, 1), name='a0.n.var_sample', shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 -> b0 a0', axes_lengths=(), name='a0.n.var_sample_rearrange_for_add_0', shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0, UnaryRearrange(node=FloatConstant(value=1e-05, shape=(8192,), name='a0.n.eps_sample'), op_string='b0 -> b0 o0', axes_lengths=(('o0', 1),), name='a0.n.eps_sample_rearrange_for_add_1', shape=(8192, 1), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='a0.n.c.var_p_eps_sample', shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), function=rsqrt_fn, get_jacobian=rsqrt_jacobian, name='a0.n.full_mul_sample', allows_batching=True, non_batch_dims=(), shape=(8192, 35), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), (0, 1))), out_axes=(0, 1, 2), name='a0.n.y_out_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True), op_string='b0 a0 a1 -> b0 a0 a1', axes_lengths=(), name='a0.n.y_out_sample_rearrange_for_add_1', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True): 1.0}), name='a0.n_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(ArrayConstant(value=torch.randn(torch.Size([35, 256])), shape=(35, 256), uuid=UUID('4382a439-ba87-43ff-8dd7-13f9f3d0c147'), name='w.pos_embeds')))(Einsum(args=((c17, (0, 1, 2)), (ArrayConstant(value=torch.randn(torch.Size([256, 256])), shape=(8192, 256, 256), uuid=UUID('87fea373-a043-4a30-a0b3-15d096b6d0db'), name='a0.n.c.sub_mean_sample'), (0, 2, 3))), out_axes=(0, 1, 3), name='a0.n.z_mean_sample', shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True)))(Index(node=ArrayConstant(value=torch.randn(torch.Size([48110, 35, 256])), shape=(48110, 35, 256), uuid=UUID('05a4b3da-31f1-4610-a3b9-58f483c9bac2'), name='unnamed'), index=(torch.randint(1,48094,torch.Size([8192])),), name='embed_var_sample', hash_tensor_idx_by_value=False, shape=(8192, 35, 256), is_constant=True, is_explicitly_computable=True, can_be_sampled=True))
"""
)
dtype = torch.float32
nb_example = cast_circuit(nb_example, device="cuda", dtype=dtype)
nb_example_rust = deep_canonicalize(strip_names(py_to_rust(nb_example)))
print(f"py circ has {count_nodes(nb_example)} nodes")
nb_example_rust.print_stats()
nb_example_rust.compiler_print()
with catchtime("py"):
    py_simp = optimize_with_backreferences(circuit_to_canonical_ast(nb_example))[0]
with catchtime("simp"):
    simped = optimize_circuit(nb_example_rust, OptimizationSettings())
simped.print_stats()
simped.compiler_print()
print(f"py circ has {ast_count_nodes(py_simp)} nodes, rust circ has {r_count_nodes(simped)} nodes")
with catchtime("scheduled eval"):
    sched_eval = optimize_and_evaluate(simped, OptimizationSettings(0, 1_800_000_000, scheduling_simplify=False))
with catchtime("rust circuit eval"):
    rust_eval = simped.evaluate()
with catchtime("rust raw eval"):
    rust_eval_raw = nb_example_rust.evaluate()
python_eval = evaluate_circuit(nb_example, verbose=0, device="cuda", dtype=dtype)
with catchtime("memf"):
    MemoizedFn(evaluate_fn(device="cuda", dtype=dtype))(nb_example)
torch.testing.assert_close(python_eval, rust_eval_raw)
deep_canonicalize(compiler_simp(nb_example_rust)).compiler_print()
print_ast_deep(py_simp)

# current rust flops: 25T python flops: 700B
