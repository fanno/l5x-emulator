from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, INT, SINT
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class AB_1734_4IOL_STRUCT_STATUS_I_0:
    Ch0Fault: BOOL = field(init=False, default_factory=BOOL)
    Ch0ConnectionFaulted: BOOL = field(init=False, default_factory=BOOL)
    Ch0ConfigurationInProgress: BOOL = field(init=False, default_factory=BOOL)
    Ch0ConfigurationFault: BOOL = field(init=False, default_factory=BOOL)
    Ch0KeyingFault: BOOL = field(init=False, default_factory=BOOL)
    Ch0ShortCircuit: BOOL = field(init=False, default_factory=BOOL)
    Ch0DataInvalid: BOOL = field(init=False, default_factory=BOOL)
    Ch0PowerFault: BOOL = field(init=False, default_factory=BOOL)
    Ch0ClampAlarm: BOOL = field(init=False, default_factory=BOOL)
    Ch1Fault: BOOL = field(init=False, default_factory=BOOL)
    Ch1ConnectionFaulted: BOOL = field(init=False, default_factory=BOOL)
    Ch1ConfigurationInProgress: BOOL = field(init=False, default_factory=BOOL)
    Ch1ConfigurationFault: BOOL = field(init=False, default_factory=BOOL)
    Ch1KeyingFault: BOOL = field(init=False, default_factory=BOOL)
    Ch1ShortCircuit: BOOL = field(init=False, default_factory=BOOL)
    Ch1DataInvalid: BOOL = field(init=False, default_factory=BOOL)
    Ch1PowerFault: BOOL = field(init=False, default_factory=BOOL)
    Ch1ClampAlarm: BOOL = field(init=False, default_factory=BOOL)
    Ch2Fault: BOOL = field(init=False, default_factory=BOOL)
    Ch2ConnectionFaulted: BOOL = field(init=False, default_factory=BOOL)
    Ch2ConfigurationInProgress: BOOL = field(init=False, default_factory=BOOL)
    Ch2ConfigurationFault: BOOL = field(init=False, default_factory=BOOL)
    Ch2KeyingFault: BOOL = field(init=False, default_factory=BOOL)
    Ch2ShortCircuit: BOOL = field(init=False, default_factory=BOOL)
    Ch2DataInvalid: BOOL = field(init=False, default_factory=BOOL)
    Ch2PowerFault: BOOL = field(init=False, default_factory=BOOL)
    Ch2ClampAlarm: BOOL = field(init=False, default_factory=BOOL)
    Ch3Fault: BOOL = field(init=False, default_factory=BOOL)
    Ch3ConnectionFaulted: BOOL = field(init=False, default_factory=BOOL)
    Ch3ConfigurationInProgress: BOOL = field(init=False, default_factory=BOOL)
    Ch3ConfigurationFault: BOOL = field(init=False, default_factory=BOOL)
    Ch3KeyingFault: BOOL = field(init=False, default_factory=BOOL)
    Ch3ShortCircuit: BOOL = field(init=False, default_factory=BOOL)
    Ch3DataInvalid: BOOL = field(init=False, default_factory=BOOL)
    Ch3PowerFault: BOOL = field(init=False, default_factory=BOOL)
    Ch3ClampAlarm: BOOL = field(init=False, default_factory=BOOL)


@DataTypeRegistry.register
@dataclass
class AB_1734_4IOL_STRUCT_EVENT_I_0:
    SequenceCount: SINT = field(init=False, default_factory=SINT)
    Qualifier: SINT = field(init=False, default_factory=SINT)
    Source_0: BOOL = field(init=False, default_factory=BOOL)
    Source_1: BOOL = field(init=False, default_factory=BOOL)
    Source_2: BOOL = field(init=False, default_factory=BOOL)
    Location: BOOL = field(init=False, default_factory=BOOL)
    Type_0: BOOL = field(init=False, default_factory=BOOL)
    Type_1: BOOL = field(init=False, default_factory=BOOL)
    Mode_0: BOOL = field(init=False, default_factory=BOOL)
    Mode_1: BOOL = field(init=False, default_factory=BOOL)
    Code: INT = field(init=False, default_factory=INT)

@DataTypeRegistry.register
@dataclass
class AB_1734_4IOL1_C_0:
    Ch0FaultMode: SINT = field(init=False, default_factory=SINT)
    Ch0ProgMode: SINT = field(init=False, default_factory=SINT)
    Ch1FaultMode: SINT = field(init=False, default_factory=SINT)
    Ch1ProgMode: SINT = field(init=False, default_factory=SINT)
    Ch2FaultMode: SINT = field(init=False, default_factory=SINT)
    Ch2ProgMode: SINT = field(init=False, default_factory=SINT)
    Ch3FaultMode: SINT = field(init=False, default_factory=SINT)
    Ch3ProgMode: SINT = field(init=False, default_factory=SINT)
    Ch0FilterOffOn: SINT = field(init=False, default_factory=SINT)
    Ch0FilterOnOff: SINT = field(init=False, default_factory=SINT)
    Ch1FilterOffOn: SINT = field(init=False, default_factory=SINT)
    Ch1FilterOnOff: SINT = field(init=False, default_factory=SINT)
    Ch2FilterOffOn: SINT = field(init=False, default_factory=SINT)
    Ch2FilterOnOff: SINT = field(init=False, default_factory=SINT)
    Ch3FilterOffOn: SINT = field(init=False, default_factory=SINT)
    Ch3FilterOnOff: SINT = field(init=False, default_factory=SINT)

@DataTypeRegistry.register
@dataclass
class AB_1734_4IOL_I_0:
    Fault: DINT = field(init=False, default_factory=DINT)
    Status: AB_1734_4IOL_STRUCT_STATUS_I_0 = field(init=False, default_factory=AB_1734_4IOL_STRUCT_STATUS_I_0)
    Ch0DiagEvent: AB_1734_4IOL_STRUCT_EVENT_I_0 = field(init=False, default_factory=AB_1734_4IOL_STRUCT_EVENT_I_0)
    Ch1DiagEvent: AB_1734_4IOL_STRUCT_EVENT_I_0 = field(init=False, default_factory=AB_1734_4IOL_STRUCT_EVENT_I_0)
    Ch2DiagEvent: AB_1734_4IOL_STRUCT_EVENT_I_0 = field(init=False, default_factory=AB_1734_4IOL_STRUCT_EVENT_I_0)
    Ch3DiagEvent: AB_1734_4IOL_STRUCT_EVENT_I_0 = field(init=False, default_factory=AB_1734_4IOL_STRUCT_EVENT_I_0)
