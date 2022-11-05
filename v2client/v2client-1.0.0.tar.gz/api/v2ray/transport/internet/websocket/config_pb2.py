# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transport/internet/websocket/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='transport/internet/websocket/config.proto',
  package='v2ray.core.transport.internet.websocket',
  syntax='proto3',
  serialized_options=b'\n+com.v2ray.core.transport.internet.websocketP\001Z+v2ray.com/core/transport/internet/websocket\252\002\'V2Ray.Core.Transport.Internet.Websocket',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n)transport/internet/websocket/config.proto\x12\'v2ray.core.transport.internet.websocket\"$\n\x06Header\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"|\n\x06\x43onfig\x12\x0c\n\x04path\x18\x02 \x01(\t\x12?\n\x06header\x18\x03 \x03(\x0b\x32/.v2ray.core.transport.internet.websocket.Header\x12\x1d\n\x15\x61\x63\x63\x65pt_proxy_protocol\x18\x04 \x01(\x08J\x04\x08\x01\x10\x02\x42\x86\x01\n+com.v2ray.core.transport.internet.websocketP\x01Z+v2ray.com/core/transport/internet/websocket\xaa\x02\'V2Ray.Core.Transport.Internet.Websocketb\x06proto3'
)




_HEADER = _descriptor.Descriptor(
  name='Header',
  full_name='v2ray.core.transport.internet.websocket.Header',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='v2ray.core.transport.internet.websocket.Header.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='value', full_name='v2ray.core.transport.internet.websocket.Header.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
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
  serialized_start=86,
  serialized_end=122,
)


_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='v2ray.core.transport.internet.websocket.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='path', full_name='v2ray.core.transport.internet.websocket.Config.path', index=0,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='header', full_name='v2ray.core.transport.internet.websocket.Config.header', index=1,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='accept_proxy_protocol', full_name='v2ray.core.transport.internet.websocket.Config.accept_proxy_protocol', index=2,
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
  serialized_start=124,
  serialized_end=248,
)

_CONFIG.fields_by_name['header'].message_type = _HEADER
DESCRIPTOR.message_types_by_name['Header'] = _HEADER
DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Header = _reflection.GeneratedProtocolMessageType('Header', (_message.Message,), {
  'DESCRIPTOR' : _HEADER,
  '__module__' : 'transport.internet.websocket.config_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.transport.internet.websocket.Header)
  })
_sym_db.RegisterMessage(Header)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'transport.internet.websocket.config_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.transport.internet.websocket.Config)
  })
_sym_db.RegisterMessage(Config)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
