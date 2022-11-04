# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: fsai_grpc_api/protos/mission_api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from fsai_grpc_api.protos import utils_pb2 as fsai__grpc__api_dot_protos_dot_utils__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='fsai_grpc_api/protos/mission_api.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n&fsai_grpc_api/protos/mission_api.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a fsai_grpc_api/protos/utils.proto\"S\n\x07Mission\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\x12.\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"7\n\x1a\x46indOrCreateMissionRequest\x12\x19\n\x07Mission\x18\x01 \x01(\x0b\x32\x08.Mission\"Z\n\x1b\x46indOrCreateMissionResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12\x19\n\x07Mission\x18\x02 \x01(\x0b\x32\x08.Mission\"0\n\x13ListMissionsRequest\x12\x19\n\x07Mission\x18\x01 \x01(\x0b\x32\x08.Mission\"T\n\x14ListMissionsResponse\x12 \n\x0b\x63hange_type\x18\x01 \x01(\x0e\x32\x0b.ChangeType\x12\x1a\n\x08Missions\x18\x02 \x03(\x0b\x32\x08.Mission2\x9b\x01\n\nMissionApi\x12P\n\x13\x46indOrCreateMission\x12\x1b.FindOrCreateMissionRequest\x1a\x1c.FindOrCreateMissionResponse\x12;\n\x0cListMissions\x12\x14.ListMissionsRequest\x1a\x15.ListMissionsResponseb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,fsai__grpc__api_dot_protos_dot_utils__pb2.DESCRIPTOR,])




_MISSION = _descriptor.Descriptor(
  name='Mission',
  full_name='Mission',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='id', full_name='Mission.id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='Mission.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='Mission.created_at', index=2,
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
  serialized_start=109,
  serialized_end=192,
)


_FINDORCREATEMISSIONREQUEST = _descriptor.Descriptor(
  name='FindOrCreateMissionRequest',
  full_name='FindOrCreateMissionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Mission', full_name='FindOrCreateMissionRequest.Mission', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=194,
  serialized_end=249,
)


_FINDORCREATEMISSIONRESPONSE = _descriptor.Descriptor(
  name='FindOrCreateMissionResponse',
  full_name='FindOrCreateMissionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='change_type', full_name='FindOrCreateMissionResponse.change_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Mission', full_name='FindOrCreateMissionResponse.Mission', index=1,
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
  serialized_start=251,
  serialized_end=341,
)


_LISTMISSIONSREQUEST = _descriptor.Descriptor(
  name='ListMissionsRequest',
  full_name='ListMissionsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='Mission', full_name='ListMissionsRequest.Mission', index=0,
      number=1, type=11, cpp_type=10, label=1,
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
  serialized_start=343,
  serialized_end=391,
)


_LISTMISSIONSRESPONSE = _descriptor.Descriptor(
  name='ListMissionsResponse',
  full_name='ListMissionsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='change_type', full_name='ListMissionsResponse.change_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='Missions', full_name='ListMissionsResponse.Missions', index=1,
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
  serialized_start=393,
  serialized_end=477,
)

_MISSION.fields_by_name['created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_FINDORCREATEMISSIONREQUEST.fields_by_name['Mission'].message_type = _MISSION
_FINDORCREATEMISSIONRESPONSE.fields_by_name['change_type'].enum_type = fsai__grpc__api_dot_protos_dot_utils__pb2._CHANGETYPE
_FINDORCREATEMISSIONRESPONSE.fields_by_name['Mission'].message_type = _MISSION
_LISTMISSIONSREQUEST.fields_by_name['Mission'].message_type = _MISSION
_LISTMISSIONSRESPONSE.fields_by_name['change_type'].enum_type = fsai__grpc__api_dot_protos_dot_utils__pb2._CHANGETYPE
_LISTMISSIONSRESPONSE.fields_by_name['Missions'].message_type = _MISSION
DESCRIPTOR.message_types_by_name['Mission'] = _MISSION
DESCRIPTOR.message_types_by_name['FindOrCreateMissionRequest'] = _FINDORCREATEMISSIONREQUEST
DESCRIPTOR.message_types_by_name['FindOrCreateMissionResponse'] = _FINDORCREATEMISSIONRESPONSE
DESCRIPTOR.message_types_by_name['ListMissionsRequest'] = _LISTMISSIONSREQUEST
DESCRIPTOR.message_types_by_name['ListMissionsResponse'] = _LISTMISSIONSRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Mission = _reflection.GeneratedProtocolMessageType('Mission', (_message.Message,), {
  'DESCRIPTOR' : _MISSION,
  '__module__' : 'fsai_grpc_api.protos.mission_api_pb2'
  # @@protoc_insertion_point(class_scope:Mission)
  })
_sym_db.RegisterMessage(Mission)

FindOrCreateMissionRequest = _reflection.GeneratedProtocolMessageType('FindOrCreateMissionRequest', (_message.Message,), {
  'DESCRIPTOR' : _FINDORCREATEMISSIONREQUEST,
  '__module__' : 'fsai_grpc_api.protos.mission_api_pb2'
  # @@protoc_insertion_point(class_scope:FindOrCreateMissionRequest)
  })
_sym_db.RegisterMessage(FindOrCreateMissionRequest)

FindOrCreateMissionResponse = _reflection.GeneratedProtocolMessageType('FindOrCreateMissionResponse', (_message.Message,), {
  'DESCRIPTOR' : _FINDORCREATEMISSIONRESPONSE,
  '__module__' : 'fsai_grpc_api.protos.mission_api_pb2'
  # @@protoc_insertion_point(class_scope:FindOrCreateMissionResponse)
  })
_sym_db.RegisterMessage(FindOrCreateMissionResponse)

ListMissionsRequest = _reflection.GeneratedProtocolMessageType('ListMissionsRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTMISSIONSREQUEST,
  '__module__' : 'fsai_grpc_api.protos.mission_api_pb2'
  # @@protoc_insertion_point(class_scope:ListMissionsRequest)
  })
_sym_db.RegisterMessage(ListMissionsRequest)

ListMissionsResponse = _reflection.GeneratedProtocolMessageType('ListMissionsResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTMISSIONSRESPONSE,
  '__module__' : 'fsai_grpc_api.protos.mission_api_pb2'
  # @@protoc_insertion_point(class_scope:ListMissionsResponse)
  })
_sym_db.RegisterMessage(ListMissionsResponse)



_MISSIONAPI = _descriptor.ServiceDescriptor(
  name='MissionApi',
  full_name='MissionApi',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=480,
  serialized_end=635,
  methods=[
  _descriptor.MethodDescriptor(
    name='FindOrCreateMission',
    full_name='MissionApi.FindOrCreateMission',
    index=0,
    containing_service=None,
    input_type=_FINDORCREATEMISSIONREQUEST,
    output_type=_FINDORCREATEMISSIONRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ListMissions',
    full_name='MissionApi.ListMissions',
    index=1,
    containing_service=None,
    input_type=_LISTMISSIONSREQUEST,
    output_type=_LISTMISSIONSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_MISSIONAPI)

DESCRIPTOR.services_by_name['MissionApi'] = _MISSIONAPI

# @@protoc_insertion_point(module_scope)
