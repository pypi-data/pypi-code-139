# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transport/internet/quic/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from api.common.serial import typed_message_pb2 as common_dot_serial_dot_typed__message__pb2
from api.common.protocol import headers_pb2 as common_dot_protocol_dot_headers__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='transport/internet/quic/config.proto',
  package='v2ray.core.transport.internet.quic',
  syntax='proto3',
  serialized_options=b'\n&com.v2ray.core.transport.internet.quicP\001Z&v2ray.com/core/transport/internet/quic\252\002\"V2Ray.Core.Transport.Internet.Quic',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n$transport/internet/quic/config.proto\x12\"v2ray.core.transport.internet.quic\x1a!common/serial/typed_message.proto\x1a\x1d\x63ommon/protocol/headers.proto\"\x8b\x01\n\x06\x43onfig\x12\x0b\n\x03key\x18\x01 \x01(\t\x12<\n\x08security\x18\x02 \x01(\x0b\x32*.v2ray.core.common.protocol.SecurityConfig\x12\x36\n\x06header\x18\x03 \x01(\x0b\x32&.v2ray.core.common.serial.TypedMessageBw\n&com.v2ray.core.transport.internet.quicP\x01Z&v2ray.com/core/transport/internet/quic\xaa\x02\"V2Ray.Core.Transport.Internet.Quicb\x06proto3'
  ,
  dependencies=[common_dot_serial_dot_typed__message__pb2.DESCRIPTOR,common_dot_protocol_dot_headers__pb2.DESCRIPTOR,])




_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='v2ray.core.transport.internet.quic.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='v2ray.core.transport.internet.quic.Config.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='security', full_name='v2ray.core.transport.internet.quic.Config.security', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='header', full_name='v2ray.core.transport.internet.quic.Config.header', index=2,
      number=3, type=11, cpp_type=10, label=1,
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
  serialized_start=143,
  serialized_end=282,
)

_CONFIG.fields_by_name['security'].message_type = common_dot_protocol_dot_headers__pb2._SECURITYCONFIG
_CONFIG.fields_by_name['header'].message_type = common_dot_serial_dot_typed__message__pb2._TYPEDMESSAGE
DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'transport.internet.quic.config_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.transport.internet.quic.Config)
  })
_sym_db.RegisterMessage(Config)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
