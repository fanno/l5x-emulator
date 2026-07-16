from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry
from datatypes.custom.datavariant import DataVariant

from datatypes.custom.numbers import DINT, SINT
from datatypes.custom.array import Array

@DataTypeRegistry.register
@dataclass
class TIME(DataVariant):
    _maxlength:Optional[int] = field(repr=False, default=82)

    LEN:DINT = field(init=False, repr=False, default_factory=DINT)
    DATA:Array[SINT] = field(init=False, repr=False, default_factory=lambda: Array.create(SINT, 82))

    _ua_variant:ua.Variant = field(init=False, repr=False, default=ua.VariantType.String)
    _py_variant:Any = field(init=False, repr=False, default=str)

@DataTypeRegistry.register
@dataclass
class TIME32(DataVariant):
    pass

@DataTypeRegistry.register
@dataclass
class LTIME(DataVariant):
    pass