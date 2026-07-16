from dataclasses import dataclass, field

from asyncua import ua

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, INT
from datatypes.custom.bool import BOOL

@DataTypeRegistry.register
@dataclass
class PHASE:
    State: DINT = field(init=False, default_factory=DINT)
    Running: BOOL = field(init=False, default_factory=BOOL)
    Holding: BOOL = field(init=False, default_factory=BOOL)
    Restarting: BOOL = field(init=False, default_factory=BOOL)
    Stopping: BOOL = field(init=False, default_factory=BOOL)
    Aborting: BOOL = field(init=False, default_factory=BOOL)
    Resetting: BOOL = field(init=False, default_factory=BOOL)
    Idle: BOOL = field(init=False, default_factory=BOOL)
    Held: BOOL = field(init=False, default_factory=BOOL)
    Complete: BOOL = field(init=False, default_factory=BOOL)
    Stopped: BOOL = field(init=False, default_factory=BOOL)
    Aborted: BOOL = field(init=False, default_factory=BOOL)
    PauseControl: DINT = field(init=False, default_factory=DINT)
    PauseEnabled: BOOL = field(init=False, default_factory=BOOL)
    Paused: BOOL = field(init=False, default_factory=BOOL)
    AutoPauseEnabled: BOOL = field(init=False, default_factory=BOOL)
    StepIndex: DINT = field(init=False, default_factory=DINT)
    Failure: DINT = field(init=False, default_factory=DINT)
    UnitID: DINT = field(init=False, default_factory=DINT)
    Owner: DINT = field(init=False, default_factory=DINT)
    PendingRequest: DINT = field(init=False, default_factory=DINT)
    DownloadInputParameters: BOOL = field(init=False, default_factory=BOOL)
    DownloadInputParametersSubset: BOOL = field(init=False, default_factory=BOOL)
    UploadOutputParameters: BOOL = field(init=False, default_factory=BOOL)
    UploadOutputParametersSubset: BOOL = field(init=False, default_factory=BOOL)
    DownloadOutputParameterLimits: BOOL = field(init=False, default_factory=BOOL)
    ReleaseResources: BOOL = field(init=False, default_factory=BOOL)
    SendMessageToLinkedPhase: BOOL = field(init=False, default_factory=BOOL)
    SendMessageToLinkedPhaseAndWait: BOOL = field(init=False, default_factory=BOOL)
    ReceiveMessageFromLinkedPhase: BOOL = field(init=False, default_factory=BOOL)
    CancelMessageToLinkedPhase: BOOL = field(init=False, default_factory=BOOL)
    SendMessageToOperator: BOOL = field(init=False, default_factory=BOOL)
    ClearMessageToOperator: BOOL = field(init=False, default_factory=BOOL)
    GenerateESignature: BOOL = field(init=False, default_factory=BOOL)
    DownloadBatchData: BOOL = field(init=False, default_factory=BOOL)
    DownloadMaterialTrackDataContainerInUse: BOOL = field(init=False, default_factory=BOOL)
    DownloadContainerBindingPriority: BOOL = field(init=False, default_factory=BOOL)
    DownloadSufficientMaterial: BOOL = field(init=False, default_factory=BOOL)
    DownloadMaterialTrackDatabaseData: BOOL = field(init=False, default_factory=BOOL)
    UploadMaterialTrackDataContainerInUse: BOOL = field(init=False, default_factory=BOOL)
    UploadContainerBindingPriority: BOOL = field(init=False, default_factory=BOOL)
    UploadMaterialTrackDatabaseData: BOOL = field(init=False, default_factory=BOOL)
    AbortingRequest: BOOL = field(init=False, default_factory=BOOL)
    NewInputParameters: BOOL = field(init=False, default_factory=BOOL)
    Producing: BOOL = field(init=False, default_factory=BOOL)
    Standby: BOOL = field(init=False, default_factory=BOOL)

@DataTypeRegistry.register
@dataclass
class PHASE_INSTRUCTION:
    Status: DINT = field(init=False, default_factory=DINT)
    EN: BOOL = field(init=False, default_factory=BOOL)
    ER: BOOL = field(init=False, default_factory=BOOL)
    PC: BOOL = field(init=False, default_factory=BOOL)
    IP: BOOL = field(init=False, default_factory=BOOL)
    WA: BOOL = field(init=False, default_factory=BOOL)
    ABORT: BOOL = field(init=False, default_factory=BOOL)
    ERR: INT = field(init=False, default_factory=BOOL)
    EXERR: INT = field(init=False, default_factory=BOOL)
