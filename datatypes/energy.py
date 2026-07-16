from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import REAL, INT
from datatypes.custom.bool import BOOL

from datatypes.odometer import ODOMETER, SIGNED_ODOMETER

@DataTypeRegistry.register
@dataclass
class ENERGY_BASE:
    EnergyResourceType: INT = field(init=False, default_factory=BOOL)
    BaseEnergyObjectCapabilities: INT = field(init=False, default_factory=BOOL)
    EnergyAccuracy: INT = field(init=False, default_factory=BOOL)
    DataStatus: INT = field(init=False, default_factory=BOOL)
    ConsumedEnergyOdometer: ODOMETER = field(init=False, default_factory=ODOMETER)
    GeneratedEnergyOdometer: ODOMETER = field(init=False, default_factory=ODOMETER)
    NetEnergyOdometer: SIGNED_ODOMETER = field(init=False, default_factory=SIGNED_ODOMETER)
    EnergyTransferRate: REAL = field(init=False, default_factory=REAL)
    ExtendedDataStatus: INT = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class ENERGY_ELLECTRICAL:
    RealEnergyConsumedOdometer: ODOMETER = field(init=False, default_factory=ODOMETER)
    RealEnergyGeneratedOdometer: ODOMETER = field(init=False, default_factory=ODOMETER)
    RealEnergyNetOdometer: SIGNED_ODOMETER = field(init=False, default_factory=SIGNED_ODOMETER)
    TotalRealPower: REAL = field(init=False, default_factory=REAL)
    ThreePhaseTruePowerFactor: REAL = field(init=False, default_factory=REAL)
    PhaseRotation: INT = field(init=False, default_factory=BOOL)