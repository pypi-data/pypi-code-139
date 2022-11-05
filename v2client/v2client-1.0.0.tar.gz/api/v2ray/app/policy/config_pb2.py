# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: app/policy/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='app/policy/config.proto',
  package='v2ray.core.app.policy',
  syntax='proto3',
  serialized_options=b'\n\031com.v2ray.core.app.policyP\001Z\031v2ray.com/core/app/policy\252\002\025V2Ray.Core.App.Policy',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x17\x61pp/policy/config.proto\x12\x15v2ray.core.app.policy\"\x17\n\x06Second\x12\r\n\x05value\x18\x01 \x01(\r\"\xdd\x03\n\x06Policy\x12\x36\n\x07timeout\x18\x01 \x01(\x0b\x32%.v2ray.core.app.policy.Policy.Timeout\x12\x32\n\x05stats\x18\x02 \x01(\x0b\x32#.v2ray.core.app.policy.Policy.Stats\x12\x34\n\x06\x62uffer\x18\x03 \x01(\x0b\x32$.v2ray.core.app.policy.Policy.Buffer\x1a\xdd\x01\n\x07Timeout\x12\x30\n\thandshake\x18\x01 \x01(\x0b\x32\x1d.v2ray.core.app.policy.Second\x12\x36\n\x0f\x63onnection_idle\x18\x02 \x01(\x0b\x32\x1d.v2ray.core.app.policy.Second\x12\x32\n\x0buplink_only\x18\x03 \x01(\x0b\x32\x1d.v2ray.core.app.policy.Second\x12\x34\n\rdownlink_only\x18\x04 \x01(\x0b\x32\x1d.v2ray.core.app.policy.Second\x1a\x33\n\x05Stats\x12\x13\n\x0buser_uplink\x18\x01 \x01(\x08\x12\x15\n\ruser_downlink\x18\x02 \x01(\x08\x1a\x1c\n\x06\x42uffer\x12\x12\n\nconnection\x18\x01 \x01(\x05\"\xb7\x01\n\x0cSystemPolicy\x12\x38\n\x05stats\x18\x01 \x01(\x0b\x32).v2ray.core.app.policy.SystemPolicy.Stats\x1am\n\x05Stats\x12\x16\n\x0einbound_uplink\x18\x01 \x01(\x08\x12\x18\n\x10inbound_downlink\x18\x02 \x01(\x08\x12\x17\n\x0foutbound_uplink\x18\x03 \x01(\x08\x12\x19\n\x11outbound_downlink\x18\x04 \x01(\x08\"\xc3\x01\n\x06\x43onfig\x12\x37\n\x05level\x18\x01 \x03(\x0b\x32(.v2ray.core.app.policy.Config.LevelEntry\x12\x33\n\x06system\x18\x02 \x01(\x0b\x32#.v2ray.core.app.policy.SystemPolicy\x1aK\n\nLevelEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12,\n\x05value\x18\x02 \x01(\x0b\x32\x1d.v2ray.core.app.policy.Policy:\x02\x38\x01\x42P\n\x19\x63om.v2ray.core.app.policyP\x01Z\x19v2ray.com/core/app/policy\xaa\x02\x15V2Ray.Core.App.Policyb\x06proto3'
)




_SECOND = _descriptor.Descriptor(
  name='Second',
  full_name='v2ray.core.app.policy.Second',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='value', full_name='v2ray.core.app.policy.Second.value', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=50,
  serialized_end=73,
)


_POLICY_TIMEOUT = _descriptor.Descriptor(
  name='Timeout',
  full_name='v2ray.core.app.policy.Policy.Timeout',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='handshake', full_name='v2ray.core.app.policy.Policy.Timeout.handshake', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='connection_idle', full_name='v2ray.core.app.policy.Policy.Timeout.connection_idle', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='uplink_only', full_name='v2ray.core.app.policy.Policy.Timeout.uplink_only', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='downlink_only', full_name='v2ray.core.app.policy.Policy.Timeout.downlink_only', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=249,
  serialized_end=470,
)

_POLICY_STATS = _descriptor.Descriptor(
  name='Stats',
  full_name='v2ray.core.app.policy.Policy.Stats',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='user_uplink', full_name='v2ray.core.app.policy.Policy.Stats.user_uplink', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='user_downlink', full_name='v2ray.core.app.policy.Policy.Stats.user_downlink', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=472,
  serialized_end=523,
)

_POLICY_BUFFER = _descriptor.Descriptor(
  name='Buffer',
  full_name='v2ray.core.app.policy.Policy.Buffer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='connection', full_name='v2ray.core.app.policy.Policy.Buffer.connection', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=525,
  serialized_end=553,
)

_POLICY = _descriptor.Descriptor(
  name='Policy',
  full_name='v2ray.core.app.policy.Policy',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='timeout', full_name='v2ray.core.app.policy.Policy.timeout', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stats', full_name='v2ray.core.app.policy.Policy.stats', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='buffer', full_name='v2ray.core.app.policy.Policy.buffer', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_POLICY_TIMEOUT, _POLICY_STATS, _POLICY_BUFFER, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=76,
  serialized_end=553,
)


_SYSTEMPOLICY_STATS = _descriptor.Descriptor(
  name='Stats',
  full_name='v2ray.core.app.policy.SystemPolicy.Stats',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='inbound_uplink', full_name='v2ray.core.app.policy.SystemPolicy.Stats.inbound_uplink', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='inbound_downlink', full_name='v2ray.core.app.policy.SystemPolicy.Stats.inbound_downlink', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='outbound_uplink', full_name='v2ray.core.app.policy.SystemPolicy.Stats.outbound_uplink', index=2,
      number=3, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='outbound_downlink', full_name='v2ray.core.app.policy.SystemPolicy.Stats.outbound_downlink', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=630,
  serialized_end=739,
)

_SYSTEMPOLICY = _descriptor.Descriptor(
  name='SystemPolicy',
  full_name='v2ray.core.app.policy.SystemPolicy',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='stats', full_name='v2ray.core.app.policy.SystemPolicy.stats', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_SYSTEMPOLICY_STATS, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=556,
  serialized_end=739,
)


_CONFIG_LEVELENTRY = _descriptor.Descriptor(
  name='LevelEntry',
  full_name='v2ray.core.app.policy.Config.LevelEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='v2ray.core.app.policy.Config.LevelEntry.key', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='v2ray.core.app.policy.Config.LevelEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=b'8\001',
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=862,
  serialized_end=937,
)

_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='v2ray.core.app.policy.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='level', full_name='v2ray.core.app.policy.Config.level', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='system', full_name='v2ray.core.app.policy.Config.system', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[_CONFIG_LEVELENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=742,
  serialized_end=937,
)

_POLICY_TIMEOUT.fields_by_name['handshake'].message_type = _SECOND
_POLICY_TIMEOUT.fields_by_name['connection_idle'].message_type = _SECOND
_POLICY_TIMEOUT.fields_by_name['uplink_only'].message_type = _SECOND
_POLICY_TIMEOUT.fields_by_name['downlink_only'].message_type = _SECOND
_POLICY_TIMEOUT.containing_type = _POLICY
_POLICY_STATS.containing_type = _POLICY
_POLICY_BUFFER.containing_type = _POLICY
_POLICY.fields_by_name['timeout'].message_type = _POLICY_TIMEOUT
_POLICY.fields_by_name['stats'].message_type = _POLICY_STATS
_POLICY.fields_by_name['buffer'].message_type = _POLICY_BUFFER
_SYSTEMPOLICY_STATS.containing_type = _SYSTEMPOLICY
_SYSTEMPOLICY.fields_by_name['stats'].message_type = _SYSTEMPOLICY_STATS
_CONFIG_LEVELENTRY.fields_by_name['value'].message_type = _POLICY
_CONFIG_LEVELENTRY.containing_type = _CONFIG
_CONFIG.fields_by_name['level'].message_type = _CONFIG_LEVELENTRY
_CONFIG.fields_by_name['system'].message_type = _SYSTEMPOLICY
DESCRIPTOR.message_types_by_name['Second'] = _SECOND
DESCRIPTOR.message_types_by_name['Policy'] = _POLICY
DESCRIPTOR.message_types_by_name['SystemPolicy'] = _SYSTEMPOLICY
DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Second = _reflection.GeneratedProtocolMessageType('Second', (_message.Message,), {
  'DESCRIPTOR' : _SECOND,
  '__module__' : 'app.policy.config_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.app.policy.Second)
  })
_sym_db.RegisterMessage(Second)

Policy = _reflection.GeneratedProtocolMessageType('Policy', (_message.Message,), {

  'Timeout' : _reflection.GeneratedProtocolMessageType('Timeout', (_message.Message,), {
    'DESCRIPTOR' : _POLICY_TIMEOUT,
    '__module__' : 'app.policy.config_pb2'
    # @@protoc_insertion_point(class_scope:v2ray.core.app.policy.Policy.Timeout)
    })
  ,

  'Stats' : _reflection.GeneratedProtocolMessageType('Stats', (_message.Message,), {
    'DESCRIPTOR' : _POLICY_STATS,
    '__module__' : 'app.policy.config_pb2'
    # @@protoc_insertion_point(class_scope:v2ray.core.app.policy.Policy.Stats)
    })
  ,

  'Buffer' : _reflection.GeneratedProtocolMessageType('Buffer', (_message.Message,), {
    'DESCRIPTOR' : _POLICY_BUFFER,
    '__module__' : 'app.policy.config_pb2'
    # @@protoc_insertion_point(class_scope:v2ray.core.app.policy.Policy.Buffer)
    })
  ,
  'DESCRIPTOR' : _POLICY,
  '__module__' : 'app.policy.config_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.app.policy.Policy)
  })
_sym_db.RegisterMessage(Policy)
_sym_db.RegisterMessage(Policy.Timeout)
_sym_db.RegisterMessage(Policy.Stats)
_sym_db.RegisterMessage(Policy.Buffer)

SystemPolicy = _reflection.GeneratedProtocolMessageType('SystemPolicy', (_message.Message,), {

  'Stats' : _reflection.GeneratedProtocolMessageType('Stats', (_message.Message,), {
    'DESCRIPTOR' : _SYSTEMPOLICY_STATS,
    '__module__' : 'app.policy.config_pb2'
    # @@protoc_insertion_point(class_scope:v2ray.core.app.policy.SystemPolicy.Stats)
    })
  ,
  'DESCRIPTOR' : _SYSTEMPOLICY,
  '__module__' : 'app.policy.config_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.app.policy.SystemPolicy)
  })
_sym_db.RegisterMessage(SystemPolicy)
_sym_db.RegisterMessage(SystemPolicy.Stats)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {

  'LevelEntry' : _reflection.GeneratedProtocolMessageType('LevelEntry', (_message.Message,), {
    'DESCRIPTOR' : _CONFIG_LEVELENTRY,
    '__module__' : 'app.policy.config_pb2'
    # @@protoc_insertion_point(class_scope:v2ray.core.app.policy.Config.LevelEntry)
    })
  ,
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'app.policy.config_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.app.policy.Config)
  })
_sym_db.RegisterMessage(Config)
_sym_db.RegisterMessage(Config.LevelEntry)


DESCRIPTOR._options = None
_CONFIG_LEVELENTRY._options = None
# @@protoc_insertion_point(module_scope)
