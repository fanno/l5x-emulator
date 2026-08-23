from dataclasses import dataclass, field, InitVar
from typing import Any, Protocol, List, Iterable, Generic, Union, TypeVar, Optional, get_args, get_origin, TypeGuard, Protocol, ClassVar, Callable
from lxml.etree import _Element as Element
from asyncua import ua

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.udt import UDT
from datatypes.custom.bool import BOOL

from protocols.memory import SupportsToL5X, SupportsToUi

from utils.isplcinstance import isPLCInstance

from core.memory.uimemory import UIMemoryObject, DT
from core.l5k.l5kreader import L5KReader

class DataClassMarker(Protocol):
    __dataclass_fields__: dict

T = TypeVar('T', bound=Union[DataVariant, DataClassMarker])

@dataclass(repr=False)
class Array(Generic[T], DataVariant):
    _type: ClassVar[DT] = DT.ARRAY
    #_cls: type[T] = field(repr=False)
    cls: InitVar[type[T]]
    init: InitVar[Iterable[Any]]

    _ua_variant: ua.VariantType = field(init=False, repr=False)
    _py_variant: Any = field(init=False, repr=False)    

    _data: List[T] = field(init=False, default_factory=list)

    def __post_init__(self, cls: type[T], init: Iterable[Any]) -> None:
        self._cls = cls
        if not (issubclass(self._cls, DataVariant) or issubclass(self._cls, UDT)):
            raise TypeError(f"{self._cls!r} must be a DataVariant or UDT")

        if init:
            self._extend(init)

        self._ua_variant = getattr(self._cls, "_ua_variant", ua.VariantType.ExtensionObject)
        self._py_variant = self._cls

    @staticmethod
    def create(dtype: Generic[T], count: int|list) -> 'Array[T]':
        def create_dimension(dimensions: list[int]) -> list:
            if len(dimensions) == 1:
                return [dtype() for _ in range(dimensions[0])]

            return [
                create_dimension(dimensions[1:])
                for _ in range(dimensions[0])
            ]

        if isinstance(count, int):
            initial_data = [dtype() for _ in range(count)]
        else:
            initial_data = create_dimension(count)
        return Array(dtype, initial_data)

    def setValue(self, value:"Array"):
        if not isinstance(value, Array|list):
            raise TypeError(f"Expected Array, got {type(value).__name__}")

        if len(self) != len(value):
            raise ValueError(f"Array dimensions do not match: {len(self)} != {len(value)}")

        for idx, item in enumerate(value):
            self[idx].setValue(item)

    def setOnChange(self, on_change:Callable[[Any], None] | None):
        if self._on_change is None:
            self._on_change = on_change

        for items in self._data:
            items.setOnChange(self._child_changed)            

    def _register_change(self):
        for items in self._data:
            items.setOnChange(self._child_changed)

    def getPLCValue(self) -> List[Any]:
        return self._data
        
    def getUAValue(self) -> ua.Variant:
        result = []
        for value in self._data:
            result.append(value.getUAValue())
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

    def toUI(self, name:str, path_filter: dict[str, dict] | None = None) -> UIMemoryObject:
        elements = {}

        for idx, elem in enumerate(self._data):
            key = str(idx)
            if path_filter is None or key in path_filter:
                if isPLCInstance(elem, SupportsToUi):
                    next = None
                    if path_filter:
                        next = path_filter[key]

                    elements[key] = elem.toUI(key, next)

        return UIMemoryObject(name, Datatype=self._type, Value=elements)

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
                                container = e.find("./Structure")
                                if not isPLCInstance(container, Element):
                                    container = e.find("./Array")
                                    if not isPLCInstance(container, Element):
                                        container = e
                                data.toL5X(container)
                        return
                    
                    for i in range(dimensions[depth]):
                        if i < len(data):
                            traverse(data[i], coords + [i], depth + 1)
                
                traverse(self._data)

    def toVariant(self) -> ua.Variant:
        return ua.Variant(Value=self.getUAValue(),
                          VariantType=self._ua_variant,
                          Dimensions=self.getDim(),
                          is_array=True)
    
    def fromVariant(self, variant:ua.Variant) -> None:
        if variant.VariantType == self._ua_variant:
            self.setValue(variant.Value)

    def fromL5K(self, data:L5KReader|str|list|None) -> Any:
        reader = self.getReader(data)

        from datatypes.custom.string import STRING

        for idx, value in enumerate(self._data):

            if isinstance(value, BOOL):
                value.setValue(reader.nextBool())
            elif isinstance(value, Array):
                value.fromL5K(reader)
            elif isinstance(value, STRING|UDT):
                value.fromL5K(reader.nextRaw())
            else:
                value.setValue(reader.nextRaw())

    def _coerce(self, value: Any) -> T:
        if isinstance(value, self._cls):
            return value
        
        if hasattr(self._cls, '__dataclass_fields__'):
            if isinstance(value, dict):
                return self._cls(value)
            if isinstance(value, (list, tuple)):
                return Array[self._cls](self._cls, value)
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

def isarray(obj: Any, expected_elem_type: type, min_len=0) -> TypeGuard[Array]:
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