# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: werewolves.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10werewolves.proto\x12\x04grpc\"\x07\n\x05\x45mpty\"(\n\x07Message\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"\x14\n\x04Name\x12\x0c\n\x04name\x18\x01 \x01(\t\"1\n\x0b\x43redentials\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t2\x91\x01\n\nChatServer\x12)\n\nChatStream\x12\n.grpc.Name\x1a\r.grpc.Message0\x01\x12+\n\rHandleMessage\x12\r.grpc.Message\x1a\x0b.grpc.Empty\x12+\n\x07\x43onnect\x12\x11.grpc.Credentials\x1a\r.grpc.Messageb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'werewolves_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_EMPTY']._serialized_start=26
  _globals['_EMPTY']._serialized_end=33
  _globals['_MESSAGE']._serialized_start=35
  _globals['_MESSAGE']._serialized_end=75
  _globals['_NAME']._serialized_start=77
  _globals['_NAME']._serialized_end=97
  _globals['_CREDENTIALS']._serialized_start=99
  _globals['_CREDENTIALS']._serialized_end=148
  _globals['_CHATSERVER']._serialized_start=151
  _globals['_CHATSERVER']._serialized_end=296
# @@protoc_insertion_point(module_scope)
