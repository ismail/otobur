# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: schedule.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='schedule.proto',
  package='otobur',
  serialized_pb='\n\x0eschedule.proto\x12\x06otobur\"}\n\x04Line\x12\x1b\n\x05stops\x18\x01 \x03(\x0b\x32\x0c.otobur.Stop\x12\x0c\n\x04name\x18\x02 \x02(\t\x12\n\n\x02id\x18\x03 \x02(\t\x12\x1f\n\x05start\x18\x04 \x02(\x0b\x32\x10.otobur.Location\x12\x1d\n\x03\x65nd\x18\x05 \x02(\x0b\x32\x10.otobur.Location\"\x8d\x01\n\x04Stop\x12\x11\n\tdirection\x18\x01 \x02(\x05\x12\x0c\n\x04\x63ode\x18\x02 \x02(\t\x12\x0c\n\x04name\x18\x03 \x02(\t\x12\"\n\x08location\x18\x04 \x02(\x0b\x32\x10.otobur.Location\x12\x10\n\x08latitude\x18\x05 \x02(\t\x12\x11\n\tlongitude\x18\x06 \x02(\t\x12\r\n\x05order\x18\x07 \x02(\x05\"<\n\x08Location\x12\x10\n\x08stopName\x18\x01 \x02(\t\x12\x0f\n\x07mahalle\x18\x02 \x02(\t\x12\r\n\x05\x63\x61\x64\x64\x65\x18\x03 \x02(\t\"\'\n\x08Schedule\x12\x1b\n\x05lines\x18\x01 \x03(\x0b\x32\x0c.otobur.Line')




_LINE = _descriptor.Descriptor(
  name='Line',
  full_name='otobur.Line',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='stops', full_name='otobur.Line.stops', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='otobur.Line.name', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='id', full_name='otobur.Line.id', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='start', full_name='otobur.Line.start', index=3,
      number=4, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='end', full_name='otobur.Line.end', index=4,
      number=5, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=26,
  serialized_end=151,
)


_STOP = _descriptor.Descriptor(
  name='Stop',
  full_name='otobur.Stop',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='direction', full_name='otobur.Stop.direction', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='code', full_name='otobur.Stop.code', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='name', full_name='otobur.Stop.name', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='location', full_name='otobur.Stop.location', index=3,
      number=4, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='latitude', full_name='otobur.Stop.latitude', index=4,
      number=5, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='longitude', full_name='otobur.Stop.longitude', index=5,
      number=6, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='order', full_name='otobur.Stop.order', index=6,
      number=7, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=154,
  serialized_end=295,
)


_LOCATION = _descriptor.Descriptor(
  name='Location',
  full_name='otobur.Location',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='stopName', full_name='otobur.Location.stopName', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='mahalle', full_name='otobur.Location.mahalle', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cadde', full_name='otobur.Location.cadde', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=297,
  serialized_end=357,
)


_SCHEDULE = _descriptor.Descriptor(
  name='Schedule',
  full_name='otobur.Schedule',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='lines', full_name='otobur.Schedule.lines', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=359,
  serialized_end=398,
)

_LINE.fields_by_name['stops'].message_type = _STOP
_LINE.fields_by_name['start'].message_type = _LOCATION
_LINE.fields_by_name['end'].message_type = _LOCATION
_STOP.fields_by_name['location'].message_type = _LOCATION
_SCHEDULE.fields_by_name['lines'].message_type = _LINE
DESCRIPTOR.message_types_by_name['Line'] = _LINE
DESCRIPTOR.message_types_by_name['Stop'] = _STOP
DESCRIPTOR.message_types_by_name['Location'] = _LOCATION
DESCRIPTOR.message_types_by_name['Schedule'] = _SCHEDULE

class Line(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LINE

  # @@protoc_insertion_point(class_scope:otobur.Line)

class Stop(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _STOP

  # @@protoc_insertion_point(class_scope:otobur.Stop)

class Location(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LOCATION

  # @@protoc_insertion_point(class_scope:otobur.Location)

class Schedule(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _SCHEDULE

  # @@protoc_insertion_point(class_scope:otobur.Schedule)


# @@protoc_insertion_point(module_scope)
