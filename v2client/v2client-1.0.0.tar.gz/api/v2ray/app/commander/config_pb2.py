# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: app/commander/config.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from api.common.serial import typed_message_pb2 as common_dot_serial_dot_typed__message__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='app/commander/config.proto',
  package='v2ray.core.app.commander',
  syntax='proto3',
  serialized_options=b'\n\034com.v2ray.core.app.commanderP\001Z\034v2ray.com/core/app/commander\252\002\030V2Ray.Core.App.Commander',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1a\x61pp/commander/config.proto\x12\x18v2ray.core.app.commander\x1a!common/serial/typed_message.proto\"N\n\x06\x43onfig\x12\x0b\n\x03tag\x18\x01 \x01(\t\x12\x37\n\x07service\x18\x02 \x03(\x0b\x32&.v2ray.core.common.serial.TypedMessageBY\n\x1c\x63om.v2ray.core.app.commanderP\x01Z\x1cv2ray.com/core/app/commander\xaa\x02\x18V2Ray.Core.App.Commanderb\x06proto3'
  ,
  dependencies=[common_dot_serial_dot_typed__message__pb2.DESCRIPTOR,])




_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='v2ray.core.app.commander.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tag', full_name='v2ray.core.app.commander.Config.tag', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='service', full_name='v2ray.core.app.commander.Config.service', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=91,
  serialized_end=169,
)

_CONFIG.fields_by_name['service'].message_type = common_dot_serial_dot_typed__message__pb2._TYPEDMESSAGE
DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'app.commander.config_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.app.commander.Config)
  })
_sym_db.RegisterMessage(Config)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
