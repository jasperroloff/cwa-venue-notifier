"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class TraceLocationType(_TraceLocationType, metaclass=_TraceLocationTypeEnumTypeWrapper):
    pass
class _TraceLocationType:
    V = typing.NewType('V', builtins.int)
class _TraceLocationTypeEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_TraceLocationType.V], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
    LOCATION_TYPE_UNSPECIFIED = TraceLocationType.V(0)
    LOCATION_TYPE_PERMANENT_OTHER = TraceLocationType.V(1)
    LOCATION_TYPE_TEMPORARY_OTHER = TraceLocationType.V(2)
    LOCATION_TYPE_PERMANENT_RETAIL = TraceLocationType.V(3)
    LOCATION_TYPE_PERMANENT_FOOD_SERVICE = TraceLocationType.V(4)
    LOCATION_TYPE_PERMANENT_CRAFT = TraceLocationType.V(5)
    LOCATION_TYPE_PERMANENT_WORKPLACE = TraceLocationType.V(6)
    LOCATION_TYPE_PERMANENT_EDUCATIONAL_INSTITUTION = TraceLocationType.V(7)
    LOCATION_TYPE_PERMANENT_PUBLIC_BUILDING = TraceLocationType.V(8)
    LOCATION_TYPE_TEMPORARY_CULTURAL_EVENT = TraceLocationType.V(9)
    LOCATION_TYPE_TEMPORARY_CLUB_ACTIVITY = TraceLocationType.V(10)
    LOCATION_TYPE_TEMPORARY_PRIVATE_EVENT = TraceLocationType.V(11)
    LOCATION_TYPE_TEMPORARY_WORSHIP_SERVICE = TraceLocationType.V(12)

LOCATION_TYPE_UNSPECIFIED = TraceLocationType.V(0)
LOCATION_TYPE_PERMANENT_OTHER = TraceLocationType.V(1)
LOCATION_TYPE_TEMPORARY_OTHER = TraceLocationType.V(2)
LOCATION_TYPE_PERMANENT_RETAIL = TraceLocationType.V(3)
LOCATION_TYPE_PERMANENT_FOOD_SERVICE = TraceLocationType.V(4)
LOCATION_TYPE_PERMANENT_CRAFT = TraceLocationType.V(5)
LOCATION_TYPE_PERMANENT_WORKPLACE = TraceLocationType.V(6)
LOCATION_TYPE_PERMANENT_EDUCATIONAL_INSTITUTION = TraceLocationType.V(7)
LOCATION_TYPE_PERMANENT_PUBLIC_BUILDING = TraceLocationType.V(8)
LOCATION_TYPE_TEMPORARY_CULTURAL_EVENT = TraceLocationType.V(9)
LOCATION_TYPE_TEMPORARY_CLUB_ACTIVITY = TraceLocationType.V(10)
LOCATION_TYPE_TEMPORARY_PRIVATE_EVENT = TraceLocationType.V(11)
LOCATION_TYPE_TEMPORARY_WORSHIP_SERVICE = TraceLocationType.V(12)
global___TraceLocationType = TraceLocationType


class QRCodePayload(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    VERSION_FIELD_NUMBER: builtins.int
    LOCATIONDATA_FIELD_NUMBER: builtins.int
    CROWDNOTIFIERDATA_FIELD_NUMBER: builtins.int
    VENDORDATA_FIELD_NUMBER: builtins.int
    version: builtins.int = ...
    @property
    def locationData(self) -> global___TraceLocation: ...
    @property
    def crowdNotifierData(self) -> global___CrowdNotifierData: ...
    vendorData: builtins.bytes = ...
    """byte sequence of CWALocationData"""

    def __init__(self,
        *,
        version : builtins.int = ...,
        locationData : typing.Optional[global___TraceLocation] = ...,
        crowdNotifierData : typing.Optional[global___CrowdNotifierData] = ...,
        vendorData : builtins.bytes = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["crowdNotifierData",b"crowdNotifierData","locationData",b"locationData"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["crowdNotifierData",b"crowdNotifierData","locationData",b"locationData","vendorData",b"vendorData","version",b"version"]) -> None: ...
global___QRCodePayload = QRCodePayload

class TraceLocation(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    VERSION_FIELD_NUMBER: builtins.int
    DESCRIPTION_FIELD_NUMBER: builtins.int
    ADDRESS_FIELD_NUMBER: builtins.int
    STARTTIMESTAMP_FIELD_NUMBER: builtins.int
    ENDTIMESTAMP_FIELD_NUMBER: builtins.int
    version: builtins.int = ...
    description: typing.Text = ...
    """max. 100 characters"""

    address: typing.Text = ...
    """max. 100 characters"""

    startTimestamp: builtins.int = ...
    """UNIX timestamp (in seconds)"""

    endTimestamp: builtins.int = ...
    """UNIX timestamp (in seconds)"""

    def __init__(self,
        *,
        version : builtins.int = ...,
        description : typing.Text = ...,
        address : typing.Text = ...,
        startTimestamp : builtins.int = ...,
        endTimestamp : builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["address",b"address","description",b"description","endTimestamp",b"endTimestamp","startTimestamp",b"startTimestamp","version",b"version"]) -> None: ...
global___TraceLocation = TraceLocation

class CrowdNotifierData(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    VERSION_FIELD_NUMBER: builtins.int
    PUBLICKEY_FIELD_NUMBER: builtins.int
    CRYPTOGRAPHICSEED_FIELD_NUMBER: builtins.int
    version: builtins.int = ...
    publicKey: builtins.bytes = ...
    cryptographicSeed: builtins.bytes = ...
    def __init__(self,
        *,
        version : builtins.int = ...,
        publicKey : builtins.bytes = ...,
        cryptographicSeed : builtins.bytes = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["cryptographicSeed",b"cryptographicSeed","publicKey",b"publicKey","version",b"version"]) -> None: ...
global___CrowdNotifierData = CrowdNotifierData

class CWALocationData(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    VERSION_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    DEFAULTCHECKINLENGTHINMINUTES_FIELD_NUMBER: builtins.int
    version: builtins.int = ...
    type: global___TraceLocationType.V = ...
    defaultCheckInLengthInMinutes: builtins.int = ...
    def __init__(self,
        *,
        version : builtins.int = ...,
        type : global___TraceLocationType.V = ...,
        defaultCheckInLengthInMinutes : builtins.int = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["defaultCheckInLengthInMinutes",b"defaultCheckInLengthInMinutes","type",b"type","version",b"version"]) -> None: ...
global___CWALocationData = CWALocationData