import logging

from PyInstaller.utils.hooks import collect_submodules

hiddenimports = []

packages = [
]

for pkg in packages:
    try:
        hiddenimports.extend(collect_submodules(pkg))
    except Exception as e:
        logging.exception(f"Warning: Could not scan {pkg}: {e}")

datatypes = [
    'datatypes.custom.array',
    'datatypes.custom.bool',
    'datatypes.custom.compare',
    'datatypes.custom.datavariant',
    'datatypes.custom.dt',
    'datatypes.custom.helper',
    'datatypes.custom.math',
    'datatypes.custom.module',
    'datatypes.custom.numbers',
    'datatypes.custom.string',
    'datatypes.custom.time',

    'datatypes.safety.safety',

    'datatypes.alarm',
    'datatypes.axis',
    'datatypes.cam',
    'datatypes.capture',
    'datatypes.cb',
    'datatypes.dci',
    'datatypes.discrete',
    'datatypes.dominant',
    'datatypes.energy',
    'datatypes.fdb',
    'datatypes.filter',
    'datatypes.flip_flop',
    'datatypes.lead_lag',
    'datatypes.misc',
    'datatypes.motion',
    'datatypes.odometer',
    'datatypes.output',
    'datatypes.alaprm',
    'datatypes.phase',
    'datatypes.pid',
    'datatypes.rac',
    'datatypes.select',
    'datatypes.sfc',
    'datatypes.pid',
    'datatypes.valve',
]
hiddenimports.extend(datatypes)

instructions = [
    'instructions.ascii.ascii',
    'instructions.ascii.asciiconversion',

    'instructions.file.filemisc',
    'instructions.file.fileshift',

    'instructions.math.advancedmath',
    'instructions.math.math',
    'instructions.math.mathconversation',
    'instructions.math.trig',

    'instructions.motion.motion',
    'instructions.motion.motionconfig',
    'instructions.motion.motioncordinate',
    'instructions.motion.motiongroup',
    'instructions.motion.motionmove',
    'instructions.motion.motionstate',

    'instructions.safety.drive_safety',
    'instructions.safety.metal_form',
    'instructions.safety.safety',

    'instructions.alarms',
    'instructions.bit',
    'instructions.boolean',
    'instructions.compare',
    'instructions.drives',
    'instructions.filters',
    'instructions.helper',
    'instructions.hmi',
    'instructions.input',
    'instructions.limit',
    'instructions.lisence',
    'instructions.move',
    'instructions.phase',
    'instructions.process',
    'instructions.programcontroll',
    'instructions.sequencer',
    'instructions.special',
    'instructions.statistical',
    'instructions.timer',
]
hiddenimports.extend(instructions)

modules = [
    'modules.ab._1734._4iol',
    'modules.ab._1734.di',
    'modules.ab._1734.ob',
    'modules.ab._1734.slot',
    'modules.ab._1734.ssi',

    'modules.ab._5000.hart',

    'modules.ab.cip.drive',

    'modules.ab.ethernet.module',
    'modules.ab.ethernet.safety',

    'modules.ab.motion.motion',

    'modules.ab.powerflex._425',

    'modules.channel.ai',
    'modules.channel.ao',
    'modules.channel.di',
    'modules.channel.do',
    'modules.channel.hsc',

    'modules.pas',
]
hiddenimports.extend(modules)

hiddenimports = list(set(hiddenimports))

print(f"Hook loaded {len(hiddenimports)} submodules: {hiddenimports}")