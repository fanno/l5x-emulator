from xml.etree.ElementTree import Element

from dataclasses import dataclass, field

from datatypes.custom.datavariant import DataVariant
from datatypes.custom.array import Array
from datatypes.custom.udt import UDT

from core.memory.helper import getMemory

from engine.st.st import ST
import engine.context

@dataclass
class Action:
    _Element: Element = field(init=True, default=None)

    ID: int = field(init=False, default=None)
    Operand: str = field(init=False, default=None)
    Value:DataVariant|Array|UDT = field(init=False, default=None)
    PresetUsesExpr: bool = field(init=False, default=False)
    IsBoolean: bool = field(init=False, default=False)
    Qualifier: str = field(init=False, default=None)

    def __post_init__(self):
        if self._Element:
            self.ID = int(self._Element.get('ID'))
            self.Operand = self._Element.get('Operand')
            self.Qualifier = self._Element.get('Qualifier')
            self.PresetUsesExpr = bool(self._Element.get('PresetUsesExpr'))
            self.IsBoolean = bool(self._Element.get('IsBoolean'))

            content = self._Element.find('./Body/STContent')
            st = ST(content)
            self.ST = st.getPython()

    async def execute(self, ctx:"engine.context.ExecutionContext") -> None:
        if not self.Value:
            self.Value = getMemory(self.Operand)

        #TODO: do action
        from engine.st.hooks import run_exec_env

        await run_exec_env(self.ST, ctx, self.Name, False)


