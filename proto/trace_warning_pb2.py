# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: trace_warning.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='trace_warning.proto',
  package='app.coronawarn.server.common.protocols.internal.pt',
  syntax='proto3',
  serialized_options=b'P\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x13trace_warning.proto\x12\x32\x61pp.coronawarn.server.common.protocols.internal.pt\"[\n\rCheckInRecord\x12\x1b\n\x13startIntervalNumber\x18\x01 \x01(\r\x12\x0e\n\x06period\x18\x02 \x01(\r\x12\x1d\n\x15transmissionRiskLevel\x18\x03 \x01(\r\"i\n\x16\x43heckInProtectedReport\x12\x16\n\x0elocationIdHash\x18\x01 \x01(\x0c\x12\n\n\x02iv\x18\x02 \x01(\x0c\x12\x1e\n\x16\x65ncryptedCheckInRecord\x18\x03 \x01(\x0c\x12\x0b\n\x03mac\x18\x04 \x01(\x0c\"\x9a\x02\n\x13TraceWarningPackage\x12\x16\n\x0eintervalNumber\x18\x01 \x01(\r\x12\x0e\n\x06region\x18\x02 \x01(\t\x12n\n\x14timeIntervalWarnings\x18\x03 \x03(\x0b\x32L.app.coronawarn.server.common.protocols.internal.pt.TraceTimeIntervalWarningB\x02\x18\x01\x12k\n\x17\x63heckInProtectedReports\x18\x04 \x03(\x0b\x32J.app.coronawarn.server.common.protocols.internal.pt.CheckInProtectedReport\"~\n\x18TraceTimeIntervalWarning\x12\x16\n\x0elocationIdHash\x18\x01 \x01(\x0c\x12\x1b\n\x13startIntervalNumber\x18\x02 \x01(\r\x12\x0e\n\x06period\x18\x03 \x01(\r\x12\x1d\n\x15transmissionRiskLevel\x18\x04 \x01(\rB\x02P\x01\x62\x06proto3'
)




_CHECKINRECORD = _descriptor.Descriptor(
  name='CheckInRecord',
  full_name='app.coronawarn.server.common.protocols.internal.pt.CheckInRecord',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='startIntervalNumber', full_name='app.coronawarn.server.common.protocols.internal.pt.CheckInRecord.startIntervalNumber', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='period', full_name='app.coronawarn.server.common.protocols.internal.pt.CheckInRecord.period', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transmissionRiskLevel', full_name='app.coronawarn.server.common.protocols.internal.pt.CheckInRecord.transmissionRiskLevel', index=2,
      number=3, type=13, cpp_type=3, label=1,
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
  serialized_start=75,
  serialized_end=166,
)


_CHECKINPROTECTEDREPORT = _descriptor.Descriptor(
  name='CheckInProtectedReport',
  full_name='app.coronawarn.server.common.protocols.internal.pt.CheckInProtectedReport',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='locationIdHash', full_name='app.coronawarn.server.common.protocols.internal.pt.CheckInProtectedReport.locationIdHash', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='iv', full_name='app.coronawarn.server.common.protocols.internal.pt.CheckInProtectedReport.iv', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='encryptedCheckInRecord', full_name='app.coronawarn.server.common.protocols.internal.pt.CheckInProtectedReport.encryptedCheckInRecord', index=2,
      number=3, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='mac', full_name='app.coronawarn.server.common.protocols.internal.pt.CheckInProtectedReport.mac', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
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
  serialized_start=168,
  serialized_end=273,
)


_TRACEWARNINGPACKAGE = _descriptor.Descriptor(
  name='TraceWarningPackage',
  full_name='app.coronawarn.server.common.protocols.internal.pt.TraceWarningPackage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='intervalNumber', full_name='app.coronawarn.server.common.protocols.internal.pt.TraceWarningPackage.intervalNumber', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='region', full_name='app.coronawarn.server.common.protocols.internal.pt.TraceWarningPackage.region', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timeIntervalWarnings', full_name='app.coronawarn.server.common.protocols.internal.pt.TraceWarningPackage.timeIntervalWarnings', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='checkInProtectedReports', full_name='app.coronawarn.server.common.protocols.internal.pt.TraceWarningPackage.checkInProtectedReports', index=3,
      number=4, type=11, cpp_type=10, label=3,
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
  serialized_start=276,
  serialized_end=558,
)


_TRACETIMEINTERVALWARNING = _descriptor.Descriptor(
  name='TraceTimeIntervalWarning',
  full_name='app.coronawarn.server.common.protocols.internal.pt.TraceTimeIntervalWarning',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='locationIdHash', full_name='app.coronawarn.server.common.protocols.internal.pt.TraceTimeIntervalWarning.locationIdHash', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='startIntervalNumber', full_name='app.coronawarn.server.common.protocols.internal.pt.TraceTimeIntervalWarning.startIntervalNumber', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='period', full_name='app.coronawarn.server.common.protocols.internal.pt.TraceTimeIntervalWarning.period', index=2,
      number=3, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transmissionRiskLevel', full_name='app.coronawarn.server.common.protocols.internal.pt.TraceTimeIntervalWarning.transmissionRiskLevel', index=3,
      number=4, type=13, cpp_type=3, label=1,
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
  serialized_start=560,
  serialized_end=686,
)

_TRACEWARNINGPACKAGE.fields_by_name['timeIntervalWarnings'].message_type = _TRACETIMEINTERVALWARNING
_TRACEWARNINGPACKAGE.fields_by_name['checkInProtectedReports'].message_type = _CHECKINPROTECTEDREPORT
DESCRIPTOR.message_types_by_name['CheckInRecord'] = _CHECKINRECORD
DESCRIPTOR.message_types_by_name['CheckInProtectedReport'] = _CHECKINPROTECTEDREPORT
DESCRIPTOR.message_types_by_name['TraceWarningPackage'] = _TRACEWARNINGPACKAGE
DESCRIPTOR.message_types_by_name['TraceTimeIntervalWarning'] = _TRACETIMEINTERVALWARNING
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CheckInRecord = _reflection.GeneratedProtocolMessageType('CheckInRecord', (_message.Message,), {
  'DESCRIPTOR' : _CHECKINRECORD,
  '__module__' : 'trace_warning_pb2'
  # @@protoc_insertion_point(class_scope:app.coronawarn.server.common.protocols.internal.pt.CheckInRecord)
  })
_sym_db.RegisterMessage(CheckInRecord)

CheckInProtectedReport = _reflection.GeneratedProtocolMessageType('CheckInProtectedReport', (_message.Message,), {
  'DESCRIPTOR' : _CHECKINPROTECTEDREPORT,
  '__module__' : 'trace_warning_pb2'
  # @@protoc_insertion_point(class_scope:app.coronawarn.server.common.protocols.internal.pt.CheckInProtectedReport)
  })
_sym_db.RegisterMessage(CheckInProtectedReport)

TraceWarningPackage = _reflection.GeneratedProtocolMessageType('TraceWarningPackage', (_message.Message,), {
  'DESCRIPTOR' : _TRACEWARNINGPACKAGE,
  '__module__' : 'trace_warning_pb2'
  # @@protoc_insertion_point(class_scope:app.coronawarn.server.common.protocols.internal.pt.TraceWarningPackage)
  })
_sym_db.RegisterMessage(TraceWarningPackage)

TraceTimeIntervalWarning = _reflection.GeneratedProtocolMessageType('TraceTimeIntervalWarning', (_message.Message,), {
  'DESCRIPTOR' : _TRACETIMEINTERVALWARNING,
  '__module__' : 'trace_warning_pb2'
  # @@protoc_insertion_point(class_scope:app.coronawarn.server.common.protocols.internal.pt.TraceTimeIntervalWarning)
  })
_sym_db.RegisterMessage(TraceTimeIntervalWarning)


DESCRIPTOR._options = None
_TRACEWARNINGPACKAGE.fields_by_name['timeIntervalWarnings']._options = None
# @@protoc_insertion_point(module_scope)
