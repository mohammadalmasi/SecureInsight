# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: PythonMakeCNNModelService.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fPythonMakeCNNModelService.proto\x12\x12PythonMakeCNNModel\"r\n\x0cStartRequest\x12\r\n\x05modes\x18\x01 \x03(\t\x12\x17\n\x0fsave_model_path\x18\x02 \x01(\t\x12\x0e\n\x06\x65pochs\x18\x03 \x01(\x05\x12\x12\n\nbatch_size\x18\x04 \x01(\x05\x12\x16\n\x0e\x65nable_logging\x18\x05 \x01(\x08\"X\n\rStartResponse\x12\x0e\n\x06result\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\t\x12\x10\n\x08progress\x18\x04 \x01(\t2k\n\x19PythonMakeCNNModelService\x12N\n\x05Start\x12 .PythonMakeCNNModel.StartRequest\x1a!.PythonMakeCNNModel.StartResponse0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'PythonMakeCNNModelService_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_STARTREQUEST']._serialized_start=55
  _globals['_STARTREQUEST']._serialized_end=169
  _globals['_STARTRESPONSE']._serialized_start=171
  _globals['_STARTRESPONSE']._serialized_end=259
  _globals['_PYTHONMAKECNNMODELSERVICE']._serialized_start=261
  _globals['_PYTHONMAKECNNMODELSERVICE']._serialized_end=368
# @@protoc_insertion_point(module_scope)
