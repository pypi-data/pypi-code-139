# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fsai_grpc_api/protos/category_api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from fsai_grpc_api.protos import utils_pb2 as fsai__grpc__api_dot_protos_dot_utils__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='fsai_grpc_api/protos/category_api.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\'fsai_grpc_api/protos/category_api.proto\x1a fsai_grpc_api/protos/utils.proto\"\x1f\n\x0f\x43\x61tegoryRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"@\n\x10\x43\x61tegoryResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12\n\n\x02id\x18\x02 \x01(\x03\x32J\n\x0b\x43\x61tegoryApi\x12;\n\x14\x46indOrCreateCategory\x12\x10.CategoryRequest\x1a\x11.CategoryResponseb\x06proto3'
  ,
  dependencies=[fsai__grpc__api_dot_protos_dot_utils__pb2.DESCRIPTOR,])




_CATEGORYREQUEST = _descriptor.Descriptor(
  name='CategoryRequest',
  full_name='CategoryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='CategoryRequest.name', index=0,
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
  serialized_start=77,
  serialized_end=108,
)


_CATEGORYRESPONSE = _descriptor.Descriptor(
  name='CategoryResponse',
  full_name='CategoryResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='change_type', full_name='CategoryResponse.change_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='CategoryResponse.id', index=1,
      number=2, type=3, cpp_type=2, label=1,
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
  serialized_start=110,
  serialized_end=174,
)

_CATEGORYRESPONSE.fields_by_name['change_type'].enum_type = fsai__grpc__api_dot_protos_dot_utils__pb2._CHANGETYPE
DESCRIPTOR.message_types_by_name['CategoryRequest'] = _CATEGORYREQUEST
DESCRIPTOR.message_types_by_name['CategoryResponse'] = _CATEGORYRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CategoryRequest = _reflection.GeneratedProtocolMessageType('CategoryRequest', (_message.Message,), {
  'DESCRIPTOR' : _CATEGORYREQUEST,
  '__module__' : 'fsai_grpc_api.protos.category_api_pb2'
  # @@protoc_insertion_point(class_scope:CategoryRequest)
  })
_sym_db.RegisterMessage(CategoryRequest)

CategoryResponse = _reflection.GeneratedProtocolMessageType('CategoryResponse', (_message.Message,), {
  'DESCRIPTOR' : _CATEGORYRESPONSE,
  '__module__' : 'fsai_grpc_api.protos.category_api_pb2'
  # @@protoc_insertion_point(class_scope:CategoryResponse)
  })
_sym_db.RegisterMessage(CategoryResponse)



_CATEGORYAPI = _descriptor.ServiceDescriptor(
  name='CategoryApi',
  full_name='CategoryApi',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=176,
  serialized_end=250,
  methods=[
  _descriptor.MethodDescriptor(
    name='FindOrCreateCategory',
    full_name='CategoryApi.FindOrCreateCategory',
    index=0,
    containing_service=None,
    input_type=_CATEGORYREQUEST,
    output_type=_CATEGORYRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_CATEGORYAPI)

DESCRIPTOR.services_by_name['CategoryApi'] = _CATEGORYAPI

# @@protoc_insertion_point(module_scope)
