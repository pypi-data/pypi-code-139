# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: transport/internet/config.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from api.v2ray.common.serial import typed_message_pb2 as common_dot_serial_dot_typed__message__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='transport/internet/config.proto',
  package='v2ray.core.transport.internet',
  syntax='proto3',
  serialized_options=b'\n!com.v2ray.core.transport.internetP\001Z!v2ray.com/core/transport/internet\252\002\035V2Ray.Core.Transport.Internet',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1ftransport/internet/config.proto\x12\x1dv2ray.core.transport.internet\x1a!common/serial/typed_message.proto\"\xa6\x01\n\x0fTransportConfig\x12\x42\n\x08protocol\x18\x01 \x01(\x0e\x32\x30.v2ray.core.transport.internet.TransportProtocol\x12\x15\n\rprotocol_name\x18\x03 \x01(\t\x12\x38\n\x08settings\x18\x02 \x01(\x0b\x32&.v2ray.core.common.serial.TypedMessage\"\xd9\x02\n\x0cStreamConfig\x12\x46\n\x08protocol\x18\x01 \x01(\x0e\x32\x30.v2ray.core.transport.internet.TransportProtocolB\x02\x18\x01\x12\x15\n\rprotocol_name\x18\x05 \x01(\t\x12J\n\x12transport_settings\x18\x02 \x03(\x0b\x32..v2ray.core.transport.internet.TransportConfig\x12\x15\n\rsecurity_type\x18\x03 \x01(\t\x12\x41\n\x11security_settings\x18\x04 \x03(\x0b\x32&.v2ray.core.common.serial.TypedMessage\x12\x44\n\x0fsocket_settings\x18\x06 \x01(\x0b\x32+.v2ray.core.transport.internet.SocketConfig\"\x1a\n\x0bProxyConfig\x12\x0b\n\x03tag\x18\x01 \x01(\t\"\xe7\x02\n\x0cSocketConfig\x12\x0c\n\x04mark\x18\x01 \x01(\x05\x12I\n\x03tfo\x18\x02 \x01(\x0e\x32<.v2ray.core.transport.internet.SocketConfig.TCPFastOpenState\x12\x46\n\x06tproxy\x18\x03 \x01(\x0e\x32\x36.v2ray.core.transport.internet.SocketConfig.TProxyMode\x12%\n\x1dreceive_original_dest_address\x18\x04 \x01(\x08\x12\x14\n\x0c\x62ind_address\x18\x05 \x01(\x0c\x12\x11\n\tbind_port\x18\x06 \x01(\r\"5\n\x10TCPFastOpenState\x12\x08\n\x04\x41sIs\x10\x00\x12\n\n\x06\x45nable\x10\x01\x12\x0b\n\x07\x44isable\x10\x02\"/\n\nTProxyMode\x12\x07\n\x03Off\x10\x00\x12\n\n\x06TProxy\x10\x01\x12\x0c\n\x08Redirect\x10\x02*Z\n\x11TransportProtocol\x12\x07\n\x03TCP\x10\x00\x12\x07\n\x03UDP\x10\x01\x12\x08\n\x04MKCP\x10\x02\x12\r\n\tWebSocket\x10\x03\x12\x08\n\x04HTTP\x10\x04\x12\x10\n\x0c\x44omainSocket\x10\x05\x42h\n!com.v2ray.core.transport.internetP\x01Z!v2ray.com/core/transport/internet\xaa\x02\x1dV2Ray.Core.Transport.Internetb\x06proto3'
  ,
  dependencies=[common_dot_serial_dot_typed__message__pb2.DESCRIPTOR,])

_TRANSPORTPROTOCOL = _descriptor.EnumDescriptor(
  name='TransportProtocol',
  full_name='v2ray.core.transport.internet.TransportProtocol',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='TCP', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='UDP', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='MKCP', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='WebSocket', index=3, number=3,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='HTTP', index=4, number=4,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='DomainSocket', index=5, number=5,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=1008,
  serialized_end=1098,
)
_sym_db.RegisterEnumDescriptor(_TRANSPORTPROTOCOL)

TransportProtocol = enum_type_wrapper.EnumTypeWrapper(_TRANSPORTPROTOCOL)
TCP = 0
UDP = 1
MKCP = 2
WebSocket = 3
HTTP = 4
DomainSocket = 5


_SOCKETCONFIG_TCPFASTOPENSTATE = _descriptor.EnumDescriptor(
  name='TCPFastOpenState',
  full_name='v2ray.core.transport.internet.SocketConfig.TCPFastOpenState',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='AsIs', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Enable', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Disable', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=904,
  serialized_end=957,
)
_sym_db.RegisterEnumDescriptor(_SOCKETCONFIG_TCPFASTOPENSTATE)

_SOCKETCONFIG_TPROXYMODE = _descriptor.EnumDescriptor(
  name='TProxyMode',
  full_name='v2ray.core.transport.internet.SocketConfig.TProxyMode',
  filename=None,
  file=DESCRIPTOR,
  create_key=_descriptor._internal_create_key,
  values=[
    _descriptor.EnumValueDescriptor(
      name='Off', index=0, number=0,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='TProxy', index=1, number=1,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
    _descriptor.EnumValueDescriptor(
      name='Redirect', index=2, number=2,
      serialized_options=None,
      type=None,
      create_key=_descriptor._internal_create_key),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=959,
  serialized_end=1006,
)
_sym_db.RegisterEnumDescriptor(_SOCKETCONFIG_TPROXYMODE)


_TRANSPORTCONFIG = _descriptor.Descriptor(
  name='TransportConfig',
  full_name='v2ray.core.transport.internet.TransportConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='protocol', full_name='v2ray.core.transport.internet.TransportConfig.protocol', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='protocol_name', full_name='v2ray.core.transport.internet.TransportConfig.protocol_name', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='settings', full_name='v2ray.core.transport.internet.TransportConfig.settings', index=2,
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
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=102,
  serialized_end=268,
)


_STREAMCONFIG = _descriptor.Descriptor(
  name='StreamConfig',
  full_name='v2ray.core.transport.internet.StreamConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='protocol', full_name='v2ray.core.transport.internet.StreamConfig.protocol', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='protocol_name', full_name='v2ray.core.transport.internet.StreamConfig.protocol_name', index=1,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transport_settings', full_name='v2ray.core.transport.internet.StreamConfig.transport_settings', index=2,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='security_type', full_name='v2ray.core.transport.internet.StreamConfig.security_type', index=3,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='security_settings', full_name='v2ray.core.transport.internet.StreamConfig.security_settings', index=4,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='socket_settings', full_name='v2ray.core.transport.internet.StreamConfig.socket_settings', index=5,
      number=6, type=11, cpp_type=10, label=1,
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
  serialized_start=271,
  serialized_end=616,
)


_PROXYCONFIG = _descriptor.Descriptor(
  name='ProxyConfig',
  full_name='v2ray.core.transport.internet.ProxyConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='tag', full_name='v2ray.core.transport.internet.ProxyConfig.tag', index=0,
      number=1, type=9, cpp_type=9, label=1,
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
  serialized_start=618,
  serialized_end=644,
)


_SOCKETCONFIG = _descriptor.Descriptor(
  name='SocketConfig',
  full_name='v2ray.core.transport.internet.SocketConfig',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='mark', full_name='v2ray.core.transport.internet.SocketConfig.mark', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tfo', full_name='v2ray.core.transport.internet.SocketConfig.tfo', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tproxy', full_name='v2ray.core.transport.internet.SocketConfig.tproxy', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='receive_original_dest_address', full_name='v2ray.core.transport.internet.SocketConfig.receive_original_dest_address', index=3,
      number=4, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bind_address', full_name='v2ray.core.transport.internet.SocketConfig.bind_address', index=4,
      number=5, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bind_port', full_name='v2ray.core.transport.internet.SocketConfig.bind_port', index=5,
      number=6, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _SOCKETCONFIG_TCPFASTOPENSTATE,
    _SOCKETCONFIG_TPROXYMODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=647,
  serialized_end=1006,
)

_TRANSPORTCONFIG.fields_by_name['protocol'].enum_type = _TRANSPORTPROTOCOL
_TRANSPORTCONFIG.fields_by_name['settings'].message_type = common_dot_serial_dot_typed__message__pb2._TYPEDMESSAGE
_STREAMCONFIG.fields_by_name['protocol'].enum_type = _TRANSPORTPROTOCOL
_STREAMCONFIG.fields_by_name['transport_settings'].message_type = _TRANSPORTCONFIG
_STREAMCONFIG.fields_by_name['security_settings'].message_type = common_dot_serial_dot_typed__message__pb2._TYPEDMESSAGE
_STREAMCONFIG.fields_by_name['socket_settings'].message_type = _SOCKETCONFIG
_SOCKETCONFIG.fields_by_name['tfo'].enum_type = _SOCKETCONFIG_TCPFASTOPENSTATE
_SOCKETCONFIG.fields_by_name['tproxy'].enum_type = _SOCKETCONFIG_TPROXYMODE
_SOCKETCONFIG_TCPFASTOPENSTATE.containing_type = _SOCKETCONFIG
_SOCKETCONFIG_TPROXYMODE.containing_type = _SOCKETCONFIG
DESCRIPTOR.message_types_by_name['TransportConfig'] = _TRANSPORTCONFIG
DESCRIPTOR.message_types_by_name['StreamConfig'] = _STREAMCONFIG
DESCRIPTOR.message_types_by_name['ProxyConfig'] = _PROXYCONFIG
DESCRIPTOR.message_types_by_name['SocketConfig'] = _SOCKETCONFIG
DESCRIPTOR.enum_types_by_name['TransportProtocol'] = _TRANSPORTPROTOCOL
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TransportConfig = _reflection.GeneratedProtocolMessageType('TransportConfig', (_message.Message,), {
  'DESCRIPTOR' : _TRANSPORTCONFIG,
  '__module__' : 'transport.internet.config_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.transport.internet.TransportConfig)
  })
_sym_db.RegisterMessage(TransportConfig)

StreamConfig = _reflection.GeneratedProtocolMessageType('StreamConfig', (_message.Message,), {
  'DESCRIPTOR' : _STREAMCONFIG,
  '__module__' : 'transport.internet.config_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.transport.internet.StreamConfig)
  })
_sym_db.RegisterMessage(StreamConfig)

ProxyConfig = _reflection.GeneratedProtocolMessageType('ProxyConfig', (_message.Message,), {
  'DESCRIPTOR' : _PROXYCONFIG,
  '__module__' : 'transport.internet.config_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.transport.internet.ProxyConfig)
  })
_sym_db.RegisterMessage(ProxyConfig)

SocketConfig = _reflection.GeneratedProtocolMessageType('SocketConfig', (_message.Message,), {
  'DESCRIPTOR' : _SOCKETCONFIG,
  '__module__' : 'transport.internet.config_pb2'
  # @@protoc_insertion_point(class_scope:v2ray.core.transport.internet.SocketConfig)
  })
_sym_db.RegisterMessage(SocketConfig)


DESCRIPTOR._options = None
_STREAMCONFIG.fields_by_name['protocol']._options = None
# @@protoc_insertion_point(module_scope)
