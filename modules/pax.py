from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import SINT, REAL
from datatypes.custom.bool import BOOL

from modules.channel.ai import CHANNEL_AI_HART_I_0, CHANNEL_AI_I_0
from modules.ab._5000.hart import AB_5000_HART_STATIC_STRUCT_I_0

@DataTypeRegistry.register
@dataclass
class PAX_HART_DEVICE_I_0:
    RunMode: BOOL = field(init=False, default_factory=BOOL)
    ConnectionFaulted: BOOL = field(init=False, default_factory=BOOL)
    DiagnosticActive: BOOL = field(init=False, default_factory=BOOL)
    DiagnosticSequenceCount: SINT = field(init=False, default_factory=SINT)
    CurrentSaturated: BOOL = field(init=False, default_factory=BOOL)
    CurrentFixed: BOOL = field(init=False, default_factory=BOOL)
    MoreStatusAvailable: BOOL = field(init=False, default_factory=BOOL)
    CurrentMismatch: BOOL = field(init=False, default_factory=BOOL)
    ConfigurationChanged: BOOL = field(init=False, default_factory=BOOL)
    Malfunction: BOOL = field(init=False, default_factory=BOOL)
    LoopCurrent: CHANNEL_AI_I_0 = field(init=False, default_factory=CHANNEL_AI_I_0)
    PV: CHANNEL_AI_HART_I_0 = field(init=False, default_factory=CHANNEL_AI_HART_I_0)
    SV: CHANNEL_AI_HART_I_0 = field(init=False, default_factory=CHANNEL_AI_HART_I_0)
    TV: CHANNEL_AI_HART_I_0 = field(init=False, default_factory=CHANNEL_AI_HART_I_0)
    QV: CHANNEL_AI_HART_I_0 = field(init=False, default_factory=CHANNEL_AI_HART_I_0)
    Static: AB_5000_HART_STATIC_STRUCT_I_0 = field(init=False, default_factory=AB_5000_HART_STATIC_STRUCT_I_0)
    ChDataAtSignal4: REAL = field(init=False, default_factory=REAL)
    ChDataAtSignal20: REAL = field(init=False, default_factory=REAL)
