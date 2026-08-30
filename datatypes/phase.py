from dataclasses import dataclass, field

from core.registry.datatyperegistry import DataTypeRegistry

from datatypes.custom.numbers import DINT, INT
from datatypes.custom.bool import BOOL, MEMORY_BIT
from datatypes.custom.udt import UDT

from core.l5k.l5kreader import L5KSKIP, L5KBOOLBYTEEND, L5KBIT

@DataTypeRegistry.register
@dataclass
class PHASE(UDT):

    def __post_init__(self):
        self.Running = MEMORY_BIT(self.State, 0)
        self.Holding = MEMORY_BIT(self.State, 1)
        self.Restarting = MEMORY_BIT(self.State, 2)
        self.Stopping = MEMORY_BIT(self.State, 3)
        self.Aborting = MEMORY_BIT(self.State, 4)
        self.Resetting = MEMORY_BIT(self.State, 5)
        self.Idle = MEMORY_BIT(self.State, 6)
        self.Held = MEMORY_BIT(self.State, 7)
        self.Complete = MEMORY_BIT(self.State, 8)
        self.Stopped = MEMORY_BIT(self.State, 9)
        self.Aborted = MEMORY_BIT(self.State, 10)
        
        self.PauseEnabled = MEMORY_BIT(self.PauseControl, 0)
        self.Paused = MEMORY_BIT(self.PauseControl, 1)

        self.DownloadInputParameters = MEMORY_BIT(self.PendingRequest, 0)
        self.DownloadInputParametersSubset = MEMORY_BIT(self.PendingRequest, 1)
        self.UploadOutputParameters = MEMORY_BIT(self.PendingRequest, 2)
        self.UploadOutputParametersSubset = MEMORY_BIT(self.PendingRequest, 3)
        self.DownloadOutputParameterLimits = MEMORY_BIT(self.PendingRequest, 4)
        self.ReleaseResources = MEMORY_BIT(self.PendingRequest, 5)
        self.SendMessageToLinkedPhase = MEMORY_BIT(self.PendingRequest, 6)
        self.SendMessageToLinkedPhaseAndWait = MEMORY_BIT(self.PendingRequest, 7)
        self.ReceiveMessageFromLinkedPhase = MEMORY_BIT(self.PendingRequest, 8)
        self.CancelMessageToLinkedPhase = MEMORY_BIT(self.PendingRequest, 9)
        self.SendMessageToOperator = MEMORY_BIT(self.PendingRequest, 10)
        self.ClearMessageToOperator = MEMORY_BIT(self.PendingRequest, 11)
        self.GenerateESignature = MEMORY_BIT(self.PendingRequest, 12)
        self.DownloadBatchData = MEMORY_BIT(self.PendingRequest, 13)
        self.DownloadMaterialTrackDataContainerInUse = MEMORY_BIT(self.PendingRequest, 14)
        self.DownloadContainerBindingPriority = MEMORY_BIT(self.PendingRequest, 15)
        self.DownloadSufficientMaterial = MEMORY_BIT(self.PendingRequest, 16)
        self.DownloadMaterialTrackDatabaseData = MEMORY_BIT(self.PendingRequest, 17)
        self.UploadMaterialTrackDataContainerInUse = MEMORY_BIT(self.PendingRequest, 18)
        self.UploadContainerBindingPriority = MEMORY_BIT(self.PendingRequest, 19)
        self.UploadMaterialTrackDatabaseData = MEMORY_BIT(self.PendingRequest, 20)
        self.AbortingRequest = MEMORY_BIT(self.PendingRequest, 21)


    State: DINT = field(init=False, default_factory=DINT)
    Running: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Holding: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Restarting: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Stopping: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Aborting: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Resetting: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Idle: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Held: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Complete: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Stopped: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Aborted: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    PauseControl: DINT = field(init=False, default_factory=DINT)
    PauseEnabled: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    Paused: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    AutoPauseEnabled: BOOL = field(init=False, default_factory=BOOL)
    StepIndex: DINT = field(init=False, default_factory=DINT)
    Failure: DINT = field(init=False, default_factory=DINT)
    UnitID: DINT = field(init=False, default_factory=DINT)
    Owner: DINT = field(init=False, default_factory=DINT)
    PendingRequest: DINT = field(init=False, default_factory=DINT)
    DownloadInputParameters: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    DownloadInputParametersSubset: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    UploadOutputParameters: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    UploadOutputParametersSubset: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    DownloadOutputParameterLimits: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ReleaseResources: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    SendMessageToLinkedPhase: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    SendMessageToLinkedPhaseAndWait: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ReceiveMessageFromLinkedPhase: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    CancelMessageToLinkedPhase: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    SendMessageToOperator: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ClearMessageToOperator: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    GenerateESignature: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    DownloadBatchData: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    DownloadMaterialTrackDataContainerInUse: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    DownloadContainerBindingPriority: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    DownloadSufficientMaterial: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    DownloadMaterialTrackDatabaseData: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    UploadMaterialTrackDataContainerInUse: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    UploadContainerBindingPriority: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    UploadMaterialTrackDatabaseData: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    AbortingRequest: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    NewInputParameters: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBIT(1))
    Producing: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBIT(8))
    Standby: BOOL = field(init=False, default_factory=BOOL, metadata=L5KBIT(9))

@DataTypeRegistry.register
@dataclass
class PHASE_INSTRUCTION(UDT):
    
    def __post_init__(self):
        self.EN = MEMORY_BIT(self.Status, 31)
        self.ER = MEMORY_BIT(self.Status, 28)
        self.PC = MEMORY_BIT(self.Status, 27)
        self.IP = MEMORY_BIT(self.Status, 26)
        self.IP = MEMORY_BIT(self.Status, 25)
        self.WA = MEMORY_BIT(self.Status, 24)
        self.ABORT = MEMORY_BIT(self.Status, 23)

    Status: DINT = field(init=False, default_factory=DINT)
    EN: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ER: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    PC: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    IP: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    WA: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ABORT: BOOL = field(init=False, default_factory=BOOL, metadata=L5KSKIP)
    ERR: INT = field(init=False, default_factory=INT)
    EXERR: INT = field(init=False, default_factory=INT)