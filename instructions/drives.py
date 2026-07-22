import math

from dataclasses import dataclass, field

from engine.context import ExecutionContext
from engine.instruction import Instruction
from core.registry.instructionregistry import InstructionRegistry
from core.objectregistry import ObjectRegistry
from core.memory.identity import Identity

from datatypes.misc import PULSE_MULTIPLIER, S_CURVE, PROP_INT
from datatypes.custom.numbers import DINT, REAL

@InstructionRegistry.register
class PMUL(Instruction):
        
    async def ladder_preScan(self, ctx):
        await super().preScan(ctx)
        pm:PULSE_MULTIPLIER = self.getMemory(self.args[0])

        pm.EnableOut._reset()
        pm.EnableIn._reset()

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        pm:PULSE_MULTIPLIER = self.getMemory(self.args[0])

        if pm.EnableIn:
            pm.OutOverflow.setValue(False)
            pm.LostPrecision.setValue(False)
            pm.MultiplierInv.setValue(False)
            pm.WordSizeInv.setValue(False)

            if pm.WordSize < 2 or pm.WordSize > 32:
                pm.WordSizeInv.setValue(True)
            if pm.Multiplier <= 0:
                pm.MultiplierInv.setValue(True)

            if not pm.WordSizeInv and not pm.MultiplierInv:
                if pm.Initialize:
                    pm.Out.setValue(pm.InitialValue)
                    pm.Initialize.setValue(False)

                max_value = DINT((2 ** pm.WordSize) - 1)
                min_value = DINT(0 if pm.Mode else -(2 ** (pm.WordSize - 1)))

                clamped_input = REAL(max(min_value, min(max_value, pm.In)))

                raw_result = clamped_input * pm.Multiplier

                if raw_result > 2147483647 or raw_result < -2147483648:
                    pm.OutOverflow.setValue(True)
                    pm.Out.setValue(REAL(2147483647 if raw_result > 2147483647 else -2147483648))
                else:
                    if pm.Mode:
                        if abs(raw_result - round(raw_result)) > 1e-9:
                            pm.LostPrecision.setValue(True)
                    pm.Out.setValue(raw_result)

            status = 0
            if pm.WordSizeInv:
                status |= (1 << 2)
            if pm.OutOverflow:
                status |= (1 << 3)
            if pm.LostPrecision:
                status |= (1 << 4)
            if pm.MultiplierInv:
                status |= (1 << 5)

            if status > 0:
                status |= (1 << 1)

            pm.InstructFault.setValue(status > 0)
            pm.Status.setValue(status)

        pm.EnableIn.setValue(pm.EnableOut)

@dataclass
class SCRVMemory(Identity):
    ELAPSED_TIME:REAL = field(init=False, default_factory=REAL)

    def __post_init__(self):
        self.ELAPSED_TIME.setValue(0.0)

@InstructionRegistry.register
class SCRV(Instruction):

    async def ladder_preScan(self, ctx):
        await super().preScan(ctx)
        pm:S_CURVE = self.getMemory(self.args[0])

        pm.EnableOut._reset()
        pm.EnableIn._reset()

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        sc:S_CURVE = self.getMemory(self.args[0])

        memory = ObjectRegistry.get(sc, SCRVMemory)

        sc.AccelRateInv.setValue(False)
        sc.DecelRateInv.setValue(False)
        sc.JerkRateInv.setValue(False)
        sc.TimingModeInv.setValue(False)
        sc.RTSTimeInv.setValue(False)
        sc.RTSTimeStampInv.setValue(False)
        sc.DeltaTInv.setValue(False)
        sc.RTSMissed.setValue(False)

        if sc.AccelRate <= 0:
            sc.AccelRateInv.setValue(True)
        if sc.DecelRate <= 0:
            sc.DecelRateInv.setValue(True)
        if sc.JerkRate <= 0:
            sc.JerkRateInv.setValue(True)
        if sc.DeltaT < 0:
            sc.DeltaTInv.setValue(True)

        if not sc.AccelRateInv and not sc.DecelRateInv and not sc.JerkRateInv and not sc.DeltaTInv:
            if sc.Initialize:
                memory.ELAPSED_TIME.setValue(0.0)
                sc.Out.setValue(sc.InitialValue)
                sc.Initialize.setValue(False)

            if not sc.HoldMode or not sc.HoldEnable:
                start_pos = sc.Out.getPLCValue()
                target_pos = sc.In.getPLCValue()
                delta_pos = target_pos - start_pos

                if abs(delta_pos) < 1e-9:
                    sc.Out.setValue(target_pos)
                else:
                    acc_rate = sc.AccelRate
                    jerk_rate = sc.JerkRate
                    t_ramp = acc_rate / jerk_rate
                    dist_one_ramp = (1.0/6.0) * jerk_rate * (t_ramp ** 3)
                    dist_both_ramps = 2.0 * dist_one_ramp

                    if abs(delta_pos) < dist_both_ramps:
                        scale_factor = (abs(delta_pos) / dist_both_ramps) ** (1.0/3.0)
                        actual_acc = acc_rate * scale_factor
                        actual_t_ramp = actual_acc / jerk_rate
                        t_total = 2.0 * actual_t_ramp

                        if memory.ELAPSED_TIME.getPLCValue() >= t_total:
                            sc.Out.setValue(target_pos)
                        else:
                            elapsed = memory.ELAPSED_TIME.getPLCValue()
                            current_pos = 0.0

                            if elapsed <= actual_t_ramp:
                                current_pos = start_pos + (1.0/6.0) * jerk_rate * (elapsed ** 3)
                            else:
                                t_rem = t_total - elapsed
                                current_pos = target_pos - (1.0/6.0) * jerk_rate * (t_rem ** 3)

                            if delta_pos < 0:
                                if elapsed <= actual_t_ramp:
                                    current_pos = start_pos - (1.0/6.0) * jerk_rate * (elapsed ** 3)
                                else:
                                    t_rem = t_total - elapsed
                                    current_pos = target_pos + (1.0/6.0) * jerk_rate * (t_rem ** 3)

                            sc.Out.setValue(current_pos)
                    else:
                        dist_const_acc = abs(delta_pos) - dist_both_ramps
                        v_ramp_end = 0.5 * jerk_rate * (t_ramp ** 2)
                        a_quad = 0.5 * acc_rate
                        b_quad = v_ramp_end
                        c_quad = -dist_const_acc
                        discriminant = b_quad**2 - 4*a_quad*c_quad

                        if discriminant < 0:
                            sc.TimingModeInv.setValue(True)
                        else:
                            t2 = (-b_quad + math.sqrt(discriminant)) / (2 * a_quad)
                            t_total = 2.0 * t_ramp + t2
                            elapsed = memory.ELAPSED_TIME.getPLCValue()

                            if elapsed >= t_total:
                                sc.Out.setValue(target_pos)
                            else:
                                current_pos = 0.0
                                if elapsed <= t_ramp:
                                    current_pos = start_pos + (1.0/6.0) * jerk_rate * (elapsed ** 3)
                                elif elapsed <= t_ramp + t2:
                                    t_in_region = elapsed - t_ramp
                                    pos_at_r1_end = start_pos + (1.0/6.0) * jerk_rate * (t_ramp ** 3)
                                    vel_at_r1_end = 0.5 * jerk_rate * (t_ramp ** 2)
                                    current_pos = pos_at_r1_end + vel_at_r1_end * t_in_region + 0.5 * acc_rate * (t_in_region ** 2)
                                else:
                                    t_in_region = elapsed - (t_ramp + t2)
                                    current_pos = target_pos - (1.0/6.0) * jerk_rate * ((t_ramp - t_in_region) ** 3)

                                if delta_pos < 0:
                                    if elapsed <= t_ramp:
                                        current_pos = start_pos - (1.0/6.0) * jerk_rate * (elapsed ** 3)
                                    elif elapsed <= t_ramp + t2:
                                        t_in_region = elapsed - t_ramp
                                        pos_at_r1_end = start_pos - (1.0/6.0) * jerk_rate * (t_ramp ** 3)
                                        vel_at_r1_end = 0.5 * jerk_rate * (t_ramp ** 2)
                                        current_pos = pos_at_r1_end - (vel_at_r1_end * t_in_region + 0.5 * acc_rate * (t_in_region ** 2))
                                    else:
                                        t_in_region = elapsed - (t_ramp + t2)
                                        current_pos = target_pos + (1.0/6.0) * jerk_rate * ((t_ramp - t_in_region) ** 3)

                                sc.Out.setValue(current_pos)

        memory.ELAPSED_TIME.setValue(elapsed + sc.DeltaT)

        status = 0
        if sc.AccelRateInv:
            status |= (1 << 2)
        if sc.DecelRateInv:
            status |= (1 << 3)
        if sc.JerkRateInv:
            status |= (1 << 4)
        if sc.TimingModeInv:
            status |= (1 << 27)
        if sc.RTSMissed:
            status |= (1 << 28)
        if sc.RTSTimeInv:
            status |= (1 << 29)
        if sc.RTSTimeStampInv:
            status |= (1 << 30)
        if sc.DeltaTInv:
            status |= (1 << 31)

        if status > 0:
            status |= (1 << 1)

        sc.InstructFault.setValue(status > 0)
        
        sc.Status.setValue(status)

        sc.EnableOut.setValue(sc.EnableIn)

@InstructionRegistry.register
class PI(Instruction):

    async def ladder_preScan(self, ctx):
        await super().preScan(ctx)
        pm:PROP_INT = self.getMemory(self.args[0])

        pm.EnableOut._reset()
        pm.EnableIn._reset()    

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        pi:PROP_INT = self.getMemory(self.args[0])

        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class INTG(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class SOC(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")

@InstructionRegistry.register
class UPDN(Instruction):

    async def ladder_execute(self, ctx:"ExecutionContext") -> None:
        if ctx.RungStatus:
            raise NotImplementedError(f"{__class__} not implemented yet")