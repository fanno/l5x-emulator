from typing import Any
from asyncua import ua
from dataclasses import is_dataclass, fields
from datatypes.custom.datavariant import DataVariant

def getVariantValue(value:Any) -> Any:
    if isinstance(value, DataVariant):
        return value.getUAValue()
    elif is_dataclass(value):
        result = getattr(ua, value.__class__.__name__)()

        for f in fields(value):
            if f.repr:
                if hasattr(result, f.name):
                    setattr(result, f.name, getVariantValue(getattr(value, f.name)))
                else:
                    raise ValueError(f"Field class attribute is missing {value.__class__.__name__}, {f.name}")
        return result
    raise ValueError(f"getVariantValue cant create value {value} , {type(value)}")