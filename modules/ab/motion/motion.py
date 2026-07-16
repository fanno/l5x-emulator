from asyncua import ua

from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, INT, SINT

@DataTypeRegistry.register
@dataclass
class AB_MOTION_DIAGNOSTICS_S_1:
    LostControllerToDriveTransmissions: INT = field(init=False, default_factory=INT)
    LateControllerToDriveTransmissions: INT = field(init=False, default_factory=INT)
    LostDriveToControllerTransmissions: INT = field(init=False, default_factory=INT)
    LateDriveToControllerTransmissions: INT = field(init=False, default_factory=INT)
    LastControllerToDriveTime: INT = field(init=False, default_factory=INT)
    AverageControllerToDriveTime: INT = field(init=False, default_factory=INT)
    MaximumControllerToDriveTime: INT = field(init=False, default_factory=INT)
    LastDriveToControllerTime: INT = field(init=False, default_factory=INT)
    AverageDriveToControllerTime: INT = field(init=False, default_factory=INT)
    MaximumDriveToControllerTime: INT = field(init=False, default_factory=INT)
    LastSystemClockJitter: DINT = field(init=False, default_factory=DINT)
    AverageSystemClockJitter: DINT = field(init=False, default_factory=DINT)
    MaximumSystemClockJitter: DINT = field(init=False, default_factory=DINT)
    TimingStatisticsEnabled: SINT = field(init=False, default_factory=SINT)
    ControllerToDriveConnectionSize: INT = field(init=False, default_factory=INT)
    DriveToControllerConnectionSize: INT = field(init=False, default_factory=INT)
    NominalControllerToDriveTime: INT = field(init=False, default_factory=INT)
    NominalDriveToControllerTime: INT = field(init=False, default_factory=INT)
    CoarseUpdatePeriod: INT = field(init=False, default_factory=INT)
