# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: PythonMakeLSTMModelService.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n PythonMakeLSTMModelService.proto\x12\x13PythonMakeLSTMModel\"\xcd\x01\n\x0cStartRequest\x12\r\n\x05modes\x18\x01 \x03(\t\x12\x14\n\x0csamples_path\x18\x02 \x01(\t\x12\x17\n\x0fsave_model_path\x18\x03 \x01(\t\x12\x0f\n\x07\x64ropout\x18\x04 \x01(\x01\x12\x0f\n\x07neurons\x18\x05 \x01(\x05\x12\x0e\n\x06\x65pochs\x18\x06 \x01(\x05\x12\x12\n\nbatch_size\x18\x07 \x01(\x05\x12\x13\n\x0bvector_size\x18\x08 \x01(\x05\x12\x11\n\titeration\x18\t \x01(\x05\x12\x11\n\tmin_count\x18\n \x01(\x05\"F\n\rStartResponse\x12\x0e\n\x06result\x18\x01 \x01(\x08\x12\x15\n\rerror_message\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\t2n\n\x1aPythonMakeLSTMModelService\x12P\n\x05Start\x12!.PythonMakeLSTMModel.StartRequest\x1a\".PythonMakeLSTMModel.StartResponse0\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'PythonMakeLSTMModelService_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_STARTREQUEST']._serialized_start=58
  _globals['_STARTREQUEST']._serialized_end=263
  _globals['_STARTRESPONSE']._serialized_start=265
  _globals['_STARTRESPONSE']._serialized_end=335
  _globals['_PYTHONMAKELSTMMODELSERVICE']._serialized_start=337
  _globals['_PYTHONMAKELSTMMODELSERVICE']._serialized_end=447
# @@protoc_insertion_point(module_scope)
