# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: anki/tags.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from anki import generic_pb2 as anki_dot_generic__pb2
from anki import collection_pb2 as anki_dot_collection__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0f\x61nki/tags.proto\x12\tanki.tags\x1a\x12\x61nki/generic.proto\x1a\x15\x61nki/collection.proto\"9\n\x16SetTagCollapsedRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tcollapsed\x18\x02 \x01(\x08\"g\n\x0bTagTreeNode\x12\x0c\n\x04name\x18\x01 \x01(\t\x12(\n\x08\x63hildren\x18\x02 \x03(\x0b\x32\x16.anki.tags.TagTreeNode\x12\r\n\x05level\x18\x03 \x01(\r\x12\x11\n\tcollapsed\x18\x04 \x01(\x08\"7\n\x13ReparentTagsRequest\x12\x0c\n\x04tags\x18\x01 \x03(\t\x12\x12\n\nnew_parent\x18\x02 \x01(\t\"?\n\x11RenameTagsRequest\x12\x16\n\x0e\x63urrent_prefix\x18\x01 \x01(\t\x12\x12\n\nnew_prefix\x18\x02 \x01(\t\"7\n\x15NoteIdsAndTagsRequest\x12\x10\n\x08note_ids\x18\x01 \x03(\x03\x12\x0c\n\x04tags\x18\x02 \x01(\t\"t\n\x18\x46indAndReplaceTagRequest\x12\x10\n\x08note_ids\x18\x01 \x03(\x03\x12\x0e\n\x06search\x18\x02 \x01(\t\x12\x13\n\x0breplacement\x18\x03 \x01(\t\x12\r\n\x05regex\x18\x04 \x01(\x08\x12\x12\n\nmatch_case\x18\x05 \x01(\x08\"8\n\x12\x43ompleteTagRequest\x12\r\n\x05input\x18\x01 \x01(\t\x12\x13\n\x0bmatch_limit\x18\x02 \x01(\r\"#\n\x13\x43ompleteTagResponse\x12\x0c\n\x04tags\x18\x01 \x03(\t2\xe9\x06\n\x0bTagsService\x12K\n\x0f\x43learUnusedTags\x12\x13.anki.generic.Empty\x1a#.anki.collection.OpChangesWithCount\x12\x38\n\x07\x41llTags\x12\x13.anki.generic.Empty\x1a\x18.anki.generic.StringList\x12G\n\nRemoveTags\x12\x14.anki.generic.String\x1a#.anki.collection.OpChangesWithCount\x12P\n\x0fSetTagCollapsed\x12!.anki.tags.SetTagCollapsedRequest\x1a\x1a.anki.collection.OpChanges\x12\x36\n\x07TagTree\x12\x13.anki.generic.Empty\x1a\x16.anki.tags.TagTreeNode\x12S\n\x0cReparentTags\x12\x1e.anki.tags.ReparentTagsRequest\x1a#.anki.collection.OpChangesWithCount\x12O\n\nRenameTags\x12\x1c.anki.tags.RenameTagsRequest\x1a#.anki.collection.OpChangesWithCount\x12T\n\x0b\x41\x64\x64NoteTags\x12 .anki.tags.NoteIdsAndTagsRequest\x1a#.anki.collection.OpChangesWithCount\x12W\n\x0eRemoveNoteTags\x12 .anki.tags.NoteIdsAndTagsRequest\x1a#.anki.collection.OpChangesWithCount\x12]\n\x11\x46indAndReplaceTag\x12#.anki.tags.FindAndReplaceTagRequest\x1a#.anki.collection.OpChangesWithCount\x12L\n\x0b\x43ompleteTag\x12\x1d.anki.tags.CompleteTagRequest\x1a\x1e.anki.tags.CompleteTagResponseB\x02P\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'anki.tags_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'P\001'
  _SETTAGCOLLAPSEDREQUEST._serialized_start=73
  _SETTAGCOLLAPSEDREQUEST._serialized_end=130
  _TAGTREENODE._serialized_start=132
  _TAGTREENODE._serialized_end=235
  _REPARENTTAGSREQUEST._serialized_start=237
  _REPARENTTAGSREQUEST._serialized_end=292
  _RENAMETAGSREQUEST._serialized_start=294
  _RENAMETAGSREQUEST._serialized_end=357
  _NOTEIDSANDTAGSREQUEST._serialized_start=359
  _NOTEIDSANDTAGSREQUEST._serialized_end=414
  _FINDANDREPLACETAGREQUEST._serialized_start=416
  _FINDANDREPLACETAGREQUEST._serialized_end=532
  _COMPLETETAGREQUEST._serialized_start=534
  _COMPLETETAGREQUEST._serialized_end=590
  _COMPLETETAGRESPONSE._serialized_start=592
  _COMPLETETAGRESPONSE._serialized_end=627
  _TAGSSERVICE._serialized_start=630
  _TAGSSERVICE._serialized_end=1503
# @@protoc_insertion_point(module_scope)
