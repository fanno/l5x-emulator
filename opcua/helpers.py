import uuid

from typing import Optional, Any

from datetime import datetime

from asyncua import ua

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.numbers import REAL, LREAL, INTIGER
from datatypes.custom.bool import BOOL
from datatypes.custom.dt import DT

TYPE_MAP = {
    "SINT": ua.VariantType.SByte,
    "USINT": ua.VariantType.SByte,
    "INT": ua.VariantType.Int16,
    "UINT": ua.VariantType.UInt16,
    "DINT": ua.VariantType.Int32,
    "UDINT": ua.VariantType.UInt32,
    "LINT": ua.VariantType.Int64,
    "ULINT": ua.VariantType.UInt64,
    "REAL": ua.VariantType.Float,
    "LREAL": ua.VariantType.Double,
    "BOOL": ua.VariantType.Boolean,
    "BIT": ua.VariantType.Boolean,
}

def getPLCValue(value: Any) -> Any:
    if isinstance(value, DataVariant):
        return value.getPLCValue()
    
    if isinstance(value, list):
        return [getPLCValue(item) for item in value]
    return value

def getUAVariantType(dt:str) -> ua.VariantType:
    result = TYPE_MAP.get(dt.upper(), ua.VariantType.ExtensionObject)
    if result == ua.VariantType.ExtensionObject:
        from core.registry.datauatypesregistry import DataUATypesRegistry
        result = DataUATypesRegistry.get(dt)
    return result

def getPythonVariantType(dt:str) -> Optional[type]:
    from core.registry.datatyperegistry import DataTypeRegistry
    return DataTypeRegistry.get(dt)

def createVariant(value, variantType=None, dimensions:list[int] = None) -> ua.Variant:
    dt = variantType
    if isinstance(variantType, str):
        variantType = getUAVariantType(variantType)

    value = getPLCValue(value)

    return ua.Variant(Value=getUAValue(value, dt),
                      VariantType=variantType,
                      Dimensions=dimensions)

def getUAValue(value, variantType) -> bool | int | bool | str | str | uuid.UUID | datetime | bytes | None:
    dt = variantType
    if isinstance(variantType, str):
        variantType = getUAVariantType(variantType)

    if isinstance(value, list):
        result = []
        for v in value:
            result.append(getUAValue(v, dt))
        return result

    match variantType:
        case ua.VariantType.Null:
            return None
        case ua.VariantType.String:
            if isinstance(value, bytes):
                return value.decode('utf-8').rstrip('\x00')
            return str(value)
        case ua.VariantType.ByteString:
            if isinstance(value, str):
                return value.encode('utf-8')
            return bytes(value)
        case ua.VariantType.SByte:
            return INTIGER.toValue(value, 'SINT')
        case ua.VariantType.Byte:
            return INTIGER.toValue(value, 'USINT')
        case ua.VariantType.Int16:
            return INTIGER.toValue(value, 'INT')
        case ua.VariantType.UInt16:
            return INTIGER.toValue(value, 'UINT')
        case ua.VariantType.Int32:
            return INTIGER.toValue(value, 'DINT')
        case ua.VariantType.UInt32:
            return INTIGER.toValue(value, 'UDINT')
        case ua.VariantType.Int64:
            return INTIGER.toValue(value, 'LINT')
        case ua.VariantType.UInt64:
            return INTIGER.toValue(value, 'ULINT')
        case ua.VariantType.Float:
            return REAL.toValue(value)
        case ua.VariantType.Double:
            return LREAL.toValue(value)        
        case ua.VariantType.Boolean:
            return BOOL.toValue(value)
        case ua.VariantType.DateTime:
            return DT.toValue(value)
        case ua.VariantType.Guid:
            if isinstance(value, str):
                return uuid.UUID(hex=value)
            elif isinstance(value, int):
                return uuid.UUID(int=value)
            raise ValueError(f"uuid.UUID '{value}' is not a valid uuid.UUID format")
        case ua.VariantType.ExtensionObject:
            return getattr(ua, dt)()    

    raise ValueError(f"unhandled type from '{value}' is not a valid {type(value)} format")