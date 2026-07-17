# L5X Emulator

**Emulating Software for Rockwell PLC**

> ⚠️ **Work in Progress** – This project is still under active development.

---

## Overview

This emulator provides a simulated Rockwell PLC environment with an **OPC-UA layer**, allowing external applications to access tags. It's designed to test external applications without requiring access to a physical PLC.

### Key Features

| Feature | Description |
|---------|-------------|
| **OPC-UA Layer** | External applications can connect and interact with PLC tags |
| **GUI Option** | Optional graphical interface for rudimentary tag access and value modification |
| **Headless Mode** | Can run without GUI for CI/CD or automated testing |
| **YAML Hardware Interface** | Simulates hardware components (custom or community-shared) |
| **Language Support** | Currently supports Ladder Logic (L5X) and Structured Text (ST) |

---

## Hardware Simulation

The YAML interface allows simulation of hardware components that can be either:
- **Custom** – Created for your specific needs
- **Community Library** – Shared templates for common hardware

Example configuration: [`library/hardware/0275_1101834.yaml`](library/hardware/0275_1101834.yaml) *(work in progress)*

**Use Case:** Start a motor in your simulation, then verify that your PLC code correctly receives feedback from the hardware component.

---

## Roadmap / TODO

- [ ] Complete implementation of all "normal" instructions
- [ ] Improve `plc_emulator.L5X` parser to cover all L5X patterns
- [ ] Add persistence feature to save simulation state back to the L5X file
- [ ] Expand hardware component library
- [ ] Additional improvements (TBD)

---

## Getting Started

*Instructions coming soon...*

---

## Contributing

Contributions are welcome! This project is actively being developed. Feel free to open issues or submit pull requests.

---

## License
[`LICENSE`](LICENSE)