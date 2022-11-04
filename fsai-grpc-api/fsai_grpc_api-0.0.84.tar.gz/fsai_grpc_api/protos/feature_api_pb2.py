# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fsai_grpc_api/protos/feature_api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from fsai_grpc_api.protos import utils_pb2 as fsai__grpc__api_dot_protos_dot_utils__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='fsai_grpc_api/protos/feature_api.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n&fsai_grpc_api/protos/feature_api.proto\x1a fsai_grpc_api/protos/utils.proto\"I\n\x0e\x46\x65\x61tureRequest\x12\x13\n\x0bvendor_name\x18\x01 \x01(\t\x12\x11\n\tvendor_id\x18\x02 \x01(\t\x12\x0f\n\x07\x66\x65\x61ture\x18\x03 \x01(\t\"?\n\x0f\x46\x65\x61tureResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12\n\n\x02id\x18\x02 \x01(\x03\x32\x46\n\nFeatureApi\x12\x38\n\x13\x46indOrCreateFeature\x12\x0f.FeatureRequest\x1a\x10.FeatureResponseb\x06proto3'
  ,
  dependencies=[fsai__grpc__api_dot_protos_dot_utils__pb2.DESCRIPTOR,])




_FEATUREREQUEST = _descriptor.Descriptor(
  name='FeatureRequest',
  full_name='FeatureRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='vendor_name', full_name='FeatureRequest.vendor_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='vendor_id', full_name='FeatureRequest.vendor_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='feature', full_name='FeatureRequest.feature', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  serialized_start=76,
  serialized_end=149,
)


_FEATURERESPONSE = _descriptor.Descriptor(
  name='FeatureResponse',
  full_name='FeatureResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='change_type', full_name='FeatureResponse.change_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='id', full_name='FeatureResponse.id', index=1,
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
  serialized_start=151,
  serialized_end=214,
)

_FEATURERESPONSE.fields_by_name['change_type'].enum_type = fsai__grpc__api_dot_protos_dot_utils__pb2._CHANGETYPE
DESCRIPTOR.message_types_by_name['FeatureRequest'] = _FEATUREREQUEST
DESCRIPTOR.message_types_by_name['FeatureResponse'] = _FEATURERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

FeatureRequest = _reflection.GeneratedProtocolMessageType('FeatureRequest', (_message.Message,), {
  'DESCRIPTOR' : _FEATUREREQUEST,
  '__module__' : 'fsai_grpc_api.protos.feature_api_pb2'
  # @@protoc_insertion_point(class_scope:FeatureRequest)
  })
_sym_db.RegisterMessage(FeatureRequest)

FeatureResponse = _reflection.GeneratedProtocolMessageType('FeatureResponse', (_message.Message,), {
  'DESCRIPTOR' : _FEATURERESPONSE,
  '__module__' : 'fsai_grpc_api.protos.feature_api_pb2'
  # @@protoc_insertion_point(class_scope:FeatureResponse)
  })
_sym_db.RegisterMessage(FeatureResponse)



_FEATUREAPI = _descriptor.ServiceDescriptor(
  name='FeatureApi',
  full_name='FeatureApi',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=216,
  serialized_end=286,
  methods=[
  _descriptor.MethodDescriptor(
    name='FindOrCreateFeature',
    full_name='FeatureApi.FindOrCreateFeature',
    index=0,
    containing_service=None,
    input_type=_FEATUREREQUEST,
    output_type=_FEATURERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_FEATUREAPI)

DESCRIPTOR.services_by_name['FeatureApi'] = _FEATUREAPI

# @@protoc_insertion_point(module_scope)
