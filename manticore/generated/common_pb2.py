# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0c\x63ommon.proto\x12\x08protobuf\x1a\x19google/protobuf/any.proto\"|\n\x07package\x12\x10\n\x08obj_type\x18\x01 \x01(\t\x12\x13\n\x0bobj_version\x18\x02 \x01(\x04\x12\x0e\n\x06source\x18\x03 \x01(\t\x12\x13\n\x0b\x64\x65stination\x18\x04 \x01(\t\x12%\n\x07payload\x18\x05 \x01(\x0b\x32\x14.google.protobuf.Any\"\'\n\x06object\x12\n\n\x02id\x18\x01 \x01(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x04\"\x9f\x01\n\x07request\x12\x1d\n\x03obj\x18\x01 \x01(\x0b\x32\x10.protobuf.object\x12/\n\x07\x66ilters\x18\x02 \x03(\x0b\x32\x1e.protobuf.request.FiltersEntry\x1a\x44\n\x0c\x46iltersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12#\n\x05value\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any:\x02\x38\x01\"I\n\x08response\x12\x1d\n\x03obj\x18\x01 \x01(\x0b\x32\x10.protobuf.object\x12\x0e\n\x06status\x18\x02 \x01(\x04\x12\x0e\n\x06\x64\x65tail\x18\x03 \x01(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'common_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _REQUEST_FILTERSENTRY._options = None
  _REQUEST_FILTERSENTRY._serialized_options = b'8\001'
  _PACKAGE._serialized_start=53
  _PACKAGE._serialized_end=177
  _OBJECT._serialized_start=179
  _OBJECT._serialized_end=218
  _REQUEST._serialized_start=221
  _REQUEST._serialized_end=380
  _REQUEST_FILTERSENTRY._serialized_start=312
  _REQUEST_FILTERSENTRY._serialized_end=380
  _RESPONSE._serialized_start=382
  _RESPONSE._serialized_end=455
# @@protoc_insertion_point(module_scope)