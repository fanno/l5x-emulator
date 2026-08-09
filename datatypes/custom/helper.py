from typing import Any
from asyncua import ua
from dataclasses import is_dataclass, fields

from protocols.memory import SupportsGetPLCValue
from  utils.isplcinstance import isPLCInstance

def getVariantValue(value:Any) -> Any:
    if isPLCInstance(value, SupportsGetPLCValue):
        return value.getUAValue()
    elif is_dataclass(value):
        dt_name = value.__class__.__name__
        if hasattr(ua, dt_name):
            pass
        elif hasattr(ua, dt_name.upper()):
            dt_name = dt_name.upper()
        else:
            dt_name = None

        if dt_name is not None:
            result = getattr(ua, dt_name)()

            for f in fields(value):
                if f.repr:
                    if hasattr(result, f.name):
                        setattr(result, f.name, getVariantValue(getattr(value, f.name)))
                    else:
                        raise ValueError(f"Field class attribute is missing {dt_name}, {f.name}")
            return result
    raise ValueError(f"getVariantValue cant create value {value} , {type(value)}")