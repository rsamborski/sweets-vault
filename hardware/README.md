# Sweets Vault Hardware

This directory contains the Python scripts and drivers for interfacing with the physical hardware of the Sweets Vault. The vault consists of two electronically controlled drawers and a status LED, connected via an FTDI GPIO adapter (i.e. [FT232H](https://www.adafruit.com/product/2264?srsltid=AfmBOoojWa4ts0aPHlZS4HmEat6Cn22-PtWglOr7HJQRLL6tJ4RsI8Ub)).

## Hardware Components

- **Drawers (0 & 1)**: Electromagnetically controlled lockers.
- **Status LED**: A general-purpose LED for connectivity testing and status indication.
- **FTDI Adapter**: Used to provide GPIO pins to a computer via USB (supported via `pyftdi` and `adafruit-blinka`).

## Pinout Mapping (FTDI C-Port)

| Pin | Component | Usage | Logic |
|-----|-----------|-------|-------|
| `C0` | Drawer 0 | Primary locker control | `HIGH` = Locked, `LOW` = Unlocked |
| `C1` | Drawer 1 | Secondary locker control | `HIGH` = Locked, `LOW` = Unlocked |
| `C7` | LED | Status / Testing | `HIGH` = ON, `LOW` = OFF |

## Scripts

### 1. `drawers.py`
This is the core driver for the vault's physical locks.
- **Features**:
  - Encapsulates lock/unlock logic in a `Drawers` class.
  - **Safety**: Automatically unlocks all drawers when the script is terminated (via SIGINT/SIGTERM) to prevent accidental lock-ins during development.
  - Includes a test loop that cycles through unlocking and locking both drawers every 5 seconds.

### 2. `blink-led.py`
A simple diagnostic utility to verify if the Blinka/FTDI environment is correctly set up.
- **Action**: Blinks the LED connected to pin `C7`.

## Development Setup

The project uses `uv` for dependency management.

### Installation

```bash
# Sync dependencies from pyproject.toml
uv sync
```

### Running Tests

```bash
# Test the drawer logic
uv run drawers.py

# Test the LED connection
uv run blink-led.py
```

## Dependencies

- **`adafruit-blinka`**: Provides the CircuitPython `board` and `digitalio` APIs.
- **`pyftdi`**: Underlying driver for FTDI USB-to-GPIO communication.
