# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: anki/media.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from anki import generic_pb2 as anki_dot_generic__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x61nki/media.proto\x12\nanki.media\x1a\x12\x61nki/generic.proto\"Y\n\x12\x43heckMediaResponse\x12\x0e\n\x06unused\x18\x01 \x03(\t\x12\x0f\n\x07missing\x18\x02 \x03(\t\x12\x0e\n\x06report\x18\x03 \x01(\t\x12\x12\n\nhave_trash\x18\x04 \x01(\x08\"(\n\x16TrashMediaFilesRequest\x12\x0e\n\x06\x66names\x18\x01 \x03(\t\"9\n\x13\x41\x64\x64MediaFileRequest\x12\x14\n\x0c\x64\x65sired_name\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x32\xd6\x02\n\x0cMediaService\x12\x41\n\nCheckMedia\x12\x13.anki.generic.Empty\x1a\x1e.anki.media.CheckMediaResponse\x12J\n\x0fTrashMediaFiles\x12\".anki.media.TrashMediaFilesRequest\x1a\x13.anki.generic.Empty\x12\x45\n\x0c\x41\x64\x64MediaFile\x12\x1f.anki.media.AddMediaFileRequest\x1a\x14.anki.generic.String\x12\x36\n\nEmptyTrash\x12\x13.anki.generic.Empty\x1a\x13.anki.generic.Empty\x12\x38\n\x0cRestoreTrash\x12\x13.anki.generic.Empty\x1a\x13.anki.generic.EmptyB\x02P\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'anki.media_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'P\001'
  _CHECKMEDIARESPONSE._serialized_start=52
  _CHECKMEDIARESPONSE._serialized_end=141
  _TRASHMEDIAFILESREQUEST._serialized_start=143
  _TRASHMEDIAFILESREQUEST._serialized_end=183
  _ADDMEDIAFILEREQUEST._serialized_start=185
  _ADDMEDIAFILEREQUEST._serialized_end=242
  _MEDIASERVICE._serialized_start=245
  _MEDIASERVICE._serialized_end=587
# @@protoc_insertion_point(module_scope)
