# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: PythonTokenizerService.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cPythonTokenizerService.proto\x12\x0fPythonTokenizer\"I\n\x0cStartRequest\x12\x10\n\x08language\x18\x01 \x01(\t\x12\x13\n\x0binput_paths\x18\x02 \x03(\t\x12\x12\n\nchunk_size\x18\x03 \x01(\x05\"X\n\rStartResponse\x12\x0e\n\x06result\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\t\x12\x10\n\x08progress\x18\x04 \x01(\x02\x32\x62\n\x16PythonTokenizerService\x12H\n\x05Start\x12\x1d.PythonTokenizer.StartRequest\x1a\x1e.PythonTokenizer.StartResponse0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'PythonTokenizerService_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_STARTREQUEST']._serialized_start=49
  _globals['_STARTREQUEST']._serialized_end=122
  _globals['_STARTRESPONSE']._serialized_start=124
  _globals['_STARTRESPONSE']._serialized_end=212
  _globals['_PYTHONTOKENIZERSERVICE']._serialized_start=214
  _globals['_PYTHONTOKENIZERSERVICE']._serialized_end=312
# @@protoc_insertion_point(module_scope)
