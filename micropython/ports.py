import os
import platform

# ----- MacOS ------------------------------------------------------------------
MACOS = [
    "/dev/tty.SLAB_USBtoUART",
    "/dev/tty.usbserial-01BC57F9",
    # KB2040 | CircuitPlayground Express
    "/dev/tty.usbmodem143301"
]

# ----- Linux -----------------------------------------------------------------
LINUX = [
    "/dev/ttyUSB0",
    # KB2040 | CircuitPlayground Express
    "/dev/ttyACM0"
]

PORTS = {
    "Linux": LINUX,
    "Darwin": MACOS
}


def find_port():
    system = platform.system()
    ports = PORTS.get(system, [])
    found_port = None

    for port in ports:
        if os.path.exists(port):
            found_port = port
            break

    return found_port
