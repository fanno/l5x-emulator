from dataclasses import dataclass, field, InitVar
from typing import Any, Protocol, List, Iterable, Generic, Union, TypeVar, Optional, get_args, get_origin, TypeGuard, Protocol
from lxml.etree import _Element as Element
from asyncua import ua

from datatypes.custom.datavariant import DataVariant

from protocols.memory import SupportsSetValue, SupportsToL5X

from utils.isplcinstance import isPLCInstance

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
            self._extend(init)

        self._ua_variant = getattr(self._cls, "_ua_variant", ua.VariantType.ExtensionObject)
        self._py_variant = getattr(self._cls, "_py_variant", self._cls)

    @staticmethod
    def create(dtype: Generic[T], count: int) -> 'Array[T]':
        # Ensure we create distinct instances
        initial_data = [dtype() for _ in range(count)]
        return Array(dtype, initial_data)

    def setValue(self, value:"Array"):
        if not isinstance(value, Array):
            raise TypeError(f"Expected Array, got {type(value).__name__}")

        if self.getDim() != value.getDim():
            raise ValueError(f"Array dimensions do not match: {self.getDim()} != {value.getDim()}")

        for idx, item in enumerate(value):
            if isPLCInstance(item, SupportsSetValue):
                self[idx].setValue(item)
            else:
                raise TypeError(f"Expected UDT or DataVariant, got {type(item).__name__}")

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

    def _index_to_string(self, coords: list[int]) -> str:
        return "[" + ",".join(map(str, coords)) + "]"

    def toL5X(self, element:Element) -> None:
        if isinstance(element, Element):
            dimensions_str = element.get("Dimensions", "0")
            dimensions = [int(d) for d in dimensions_str.split(",") if d.strip()]
            
            if dimensions:
                total_elements = 1
                for d in dimensions:
                    total_elements *= d
                
                def traverse(data, coords: list[int] = [], depth: int = 0):
                    if depth == len(dimensions):
                        index_str = self._index_to_string(coords)
                        e = element.find(f'./Element[@Index="{index_str}"]')
                        if isinstance(e, Element):
                            if isPLCInstance(data, SupportsToL5X):
                                container = e.find("./Structure") or e.find("./Array") or e
                                data.toL5X(container)
                        return
                    
                    for i in range(dimensions[depth]):
                        if i < len(data):
                            traverse(data[i], coords + [i], depth + 1)
                
                traverse(self._data)

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
                return Array(self._cls, value)
        return self._cls(value)

    def _extend(self, values: Iterable[Any]) -> None:
        for v in values:
            self._data.append(self._coerce(v))

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
        self._data[index].setValue(value)
        '''
        if isinstance(value, self._cls):
            self._data[index] = value
        else:
            self._data[index].setValue(value)
        '''

    def __getitem__(self, i) -> T:
        return self._data[i]

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Array[{self._cls.__name__}]({self._data!r})"

    def __str__(self) -> str:
        return f"Array[{self._cls.__name__}]({self._data!r})"

    def __contains__(self, key:int):
        return 0 <= key < len(self._data)

    def __iter__(self):
        return iter(self._data)    

def isarray(obj: Any, expected_elem_type: type, min_len=0) -> TypeGuard[SupportsSetValue]:
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

    #if not hasattr(obj, 'setValue'):
    #    return False
    
    return True        