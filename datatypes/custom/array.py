from dataclasses import dataclass, field, InitVar
from typing import Any, Protocol, List, Iterable, Generic, Union, TypeVar, Optional, get_args, get_origin, TypeGuard, Protocol

from asyncua import ua

from datatypes.custom.datavariant import DataVariant

from datatypes.custom.helper import getVariantValue

class DataClassMarker(Protocol):
    __dataclass_fields__: dict

T = TypeVar('T', bound=Union[DataVariant, DataClassMarker])

@dataclass(repr=False)
class Array(Generic[T], DataVariant):
    _cls: type[T] = field(repr=False)

    init: InitVar[Optional[Iterable[Any]]] = None
    _data: List[T] = field(init=False, default_factory=list)

    def __post_init__(self, init: Optional[Iterable[Any]]) -> None:
        if not (issubclass(self._cls, DataVariant) or hasattr(self._cls, '__dataclass_fields__')):
            raise TypeError(f"{self._cls!r} must be a PLCElement or a dataclass")

        if init:
            self.extend(init)

        if issubclass(self._cls, DataVariant):
            self._ua_variant = self._cls._ua_variant
            self._py_variant = self._cls._py_variant
        else: 
            self._ua_variant = ua.VariantType.ExtensionObject
            self._py_variant = self._cls

    @staticmethod
    def create(dtype: Generic[T], count: int) -> 'Array[T]':
        # Ensure we create distinct instances
        initial_data = [dtype() for _ in range(count)]
        return Array(dtype, initial_data)

    def setValue(self, value:Any):
        self._data.clear()
        if isinstance(value, DataVariant):
            if value._ua_variant == self._ua_variant and value._py_variant == self._py_variant:
                self._data = value
            else:
                raise TypeError(f"{self._ua_variant}, {self._ua_variant}, {value._py_variant}, {self._py_variant}, variants do not match")
        else:
            if isinstance(value, (list, tuple)):
                for item in value:
                    self.append(item)
            else:
                self.append(value)

    def getPLCValue(self) -> List[Any]:
        return self._data
        
    def getUAValue(self) -> List[Any]:
        result = []
        for value in self._data:
            result.append(getVariantValue(value))
        return result

    def getDim(self) -> List[int]:
        data = self.getPLCValue()
        dim = []

        while(True):
            dim.append(len(data))

            if isinstance(data[0], Array):
                data = data[0].getPLCValue()
            else:
                break
        return dim

    def toVariant(self) -> ua.Variant:
        return ua.Variant(Value=self.getUAValue(),
                          VariantType=self._ua_variant,
                          Dimensions=self.getDim())
    
    def fromVariant(self, variant:ua.Variant) -> None:
        if variant.VariantType == self._ua_variant:
            self.setValue(variant.Value)

    def _coerce(self, value: Any) -> T:
        if isinstance(value, self._cls):
            return value
        if hasattr(self._cls, '__dataclass_fields__'):
            if isinstance(value, dict):
                return self._cls(value)
            if isinstance(value, (list, tuple)):
                return Array[self._cls](self._cls, value)
        return self._cls(value)

    def append(self, value: Any) -> None:
        self._data.append(self._coerce(value))

    def extend(self, values: Iterable[Any]) -> None:
        for v in values:
            self.append(v)

    def getType(self):
        lst = self._data
        dimensions = []
        while isinstance(lst, (list, Array )):
            dimensions.append(len(lst))
            
            if len(lst) > 0:
                lst = lst[0]
            else:
                break
                
        dim = ",".join(map(str, dimensions))

        return f"{self._cls.__name__}[{dim}]"

    def __setitem__(self, index: int, value: T) -> None:
        if isinstance(value, self._cls):
            self._data[index] = value
        else:
            self._data[index].setValue(value)

    def __getitem__(self, i) -> T:
        return self._data[i]

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Array[{self._cls.__name__}]({self._data!r})"

    def __str__(self) -> str:
        return f"Array[{self._cls.__name__}]({self._data!r})"    

class HasSetValue(Protocol):
    def setValue(self, value: Any) -> None: ...

def isarray(obj: Any, expected_elem_type: type, min_len=0) -> TypeGuard[HasSetValue]:
    if not isinstance(obj, Array):
        return False

    orig = getattr(obj, "__orig_class__", None)
    if orig is None:
        return False

    if get_origin(orig) is not Array:
        return False

    (actual_elem_type,) = get_args(orig)

    try:
        if not issubclass(actual_elem_type, expected_elem_type):
            return False
    except TypeError:
        if actual_elem_type != expected_elem_type:
            return False
        
    if min_len > 0:
        try:
            if len(obj) < min_len:
                return False
        except Exception:
            return False
        
    if not hasattr(obj, 'setValue'):
        return False
    
    return True        