#!/usr/bin/env python3
"""
convert_input_one_line.py

* Reads `input.txt` (one definition per line)
* Writes ONE‑LINE dataclass field definitions to `output.txt`
* Handles array sizes written with ANY of these delimiters:
      [4]   $$4$$   {4}   (4)   <4>   etc.
* Mapping tables (TYPE_FACTORY_MAP / UA_VARIANT_MAP) stay the single
  place to add new base‑type support.
"""

import re
import sys
from pathlib import Path
from typing import Dict, Tuple

# --------------------------------------------------------------
# 1️⃣  Mapping tables – extend as needed
# --------------------------------------------------------------
TYPE_FACTORY_MAP: Dict[str, str] = {
    "BOOL": "BOOL",
    "BIT": "BIT",
    "SINT": "SINT",
    "USINT": "USINT",
    "INT": "INT",
    "UINT": "UINT",
    "DINT": "DINT",
    "UDINT": "UDINT",
    "LINT": "LINT",
    "ULINT": "ULINT",
    "REAL": "REAL",
    "LREAL": "LREAL",
    # add more scalar factories here …
}

UA_VARIANT_MAP: Dict[str, str] = {
    "BOOL": "ua.VariantType.Boolean",
    "BIT": "ua.VariantType.Boolean",
    "SINT": "ua.VariantType.SByte",
    "USINT": "ua.VariantType.Byte",
    "INT": "ua.VariantType.Int16",
    "UINT": "ua.VariantType.UInt16",
    "DINT": "ua.VariantType.Int32",
    "UDINT": "ua.VariantType.UInt32",
    "LINT": "ua.VariantType.Int64",
    "ULINT": "ua.VariantType.UInt64",
    "REAL": "ua.VariantType.Float",
    "LREAL": "ua.VariantType.Double",
    # add more UA variant mappings here …
}


# --------------------------------------------------------------
# 2️⃣  Helpers
# --------------------------------------------------------------
def normalize_datatype(token: str) -> Tuple[str, int]:
    """
    Turn any representation of a datatype into:
        (base_type, is_array)

    Examples
    --------
    "INT[4]"      → ("INT", True)
    "BOOL"        → ("BOOL", False)

    The function removes **all** characters that are not letters or digits,
    then checks whether a trailing number was present.
    """
    # Keep letters and digits, replace everything else with a single space
    cleaned = re.sub(r"[^A-Za-z0-9_:]+", " ", token).strip()
    # After cleaning we may have e.g. "INT 4" or just "BOOL"
    parts = cleaned.split()

    if not parts:
        raise ValueError(f"Empty datatype after cleaning: '{token}'")

    base_type = parts[0].upper()                     # e.g. "INT"
    if  len(parts) > 1:
        is_array = int(parts[1])
    else:
        is_array = 0

    base_type = base_type.replace(":", "_")

    return base_type, is_array


def parse_line(line: str) -> Tuple[str, str, bool]:
    """
    Split a line like:
        TurnsCounters    INT$$4$$    Decimal    Read/Write

    Returns (name, base_type, is_array).
    """
    parts = re.split(r"\s+", line.strip())
    if len(parts) < 2:
        raise ValueError(f"Cannot parse line: {line!r}")

    name = parts[0]
    raw_dtype = parts[1]

    base_type, is_array = normalize_datatype(raw_dtype)
    return name, base_type, is_array


def build_one_line(name: str, base_type: str, array: int) -> str:
    try:
        factory = base_type
        ua_type = UA_VARIANT_MAP.get(base_type, "ua.VariantType.ExtensionObject")
    except KeyError as exc:
        missing = base_type
        raise KeyError(
            f"Missing mapping for type '{missing}'. Add it to the dictionaries."
        ) from exc

    if array > 0:
        # Example:
        # TurnsCounters: Array[INT] = field(init=False,
        #                                   default_factory=lambda: ArrayINT,
        #                                   metadata={"ua_type": ua.VariantType.Int16})
        return (
            f'    {name}: Array[{factory}] = field('
            f'init=False, '
            f'default_factory=lambda: Array[{factory}]({factory},[{factory}()] * {array}), '
            f'metadata={{"ua_type": {ua_type}}})'
        )
    else:
        # Example:
        # EnableIn: BOOL = field(init=False,
        #                         default_factory=BOOL,
        #                         metadata={"ua_type": ua.VariantType.Boolean})
        return (
            f'    {name}: {factory} = field('
            f'init=False, '
            f'default_factory={factory}, '
            f'metadata={{"ua_type": {ua_type}}})'
        )

header_lines = [
    "@DataTypeRegistry.register",
    "@dataclass",
    "class 11111XXXXXXXXXXXXXXXXXXXXXXXXXX:",
]
# --------------------------------------------------------------
# 3️⃣  Core conversion
# --------------------------------------------------------------
def convert_file(in_path: Path, out_path: Path) -> None:
    with in_path.open("r", encoding="utf-8") as fin, \
         out_path.open("w", encoding="utf-8") as fout:

        for hdr in header_lines:
            fout.write(hdr + "\n")

        for raw in fin:
            if not raw.strip():               # skip empty lines
                continue
            try:
                name, base_type, array = parse_line(raw)
                fout.write(build_one_line(name, base_type, array) + "\n")
            except Exception as e:
                # Write a comment so you can see which line failed
                fout.write(f"# ERROR on line: {raw.rstrip()} – {e}\n")


# --------------------------------------------------------------
# 4️⃣  Script entry point
# --------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) == 3:
        inp = Path(sys.argv[1])
        out = Path(sys.argv[2])
    else:
        inp = Path("tools/input.txt")
        out = Path("tools/output.txt")

    if not inp.is_file():
        raise FileNotFoundError(f"Input file not found: {inp}")

    convert_file(inp, out)
    print(f"Done – output written to {out.resolve()}")