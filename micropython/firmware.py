"""
micropython.org/download
"""
import os
import shutil
from invoke import task

import ports

FIRMWARE_DIR = "./.firmware"
FIRMWARE_BASE_URL = "https://www.micropython.org/resources/firmware"

# ------------------------------------------------------------------------------
# NOTE:
#   * Very specific to ESP
#   * Minimal support for other chips
# ------------------------------------------------------------------------------

ESP32 = {
    "generic": {
        "firmware": "ESP32_GENERIC-20241025-v1.24.0.bin",
        "models": [
            "SparkFun MicroMod-ESP32"
        ]
    },

    "spiram": {
        "firmware": "ESP32_GENERIC-SPIRAM-20241025-v1.24.0.bin",
        "models": []
    },

    "ota": {
        "firmware":"ESP32_GENERIC-OTA-20241025-v1.24.0.bin",
        "models": [
            "AdaFruit Huzzah-32 Feather"
        ]
    },

    "d2wd": {
        "firmware": "ESP32_GENERIC-D2WD-20241025-v1.24.0.bin",
        "models": []
    }
}

ESP8266 = {
    "generic": {
        "firmware": "ESP8266_GENERIC-20241025-v1.24.0.bin",
        "models": [
            "AdaFruit Huzzah 8266 Feather"
        ]
    },

    "ota": {
        "firmware": "ESP8266_GENERIC-OTA-20241025-v1.24.0.bin",
        "models": []
    },

    "512k": {
        "firmware": "ESP8266_GENERIC-FLASH_512K-20241025-v1.24.0.bin",
        "models": []
    },

    "1m": {
        "firmware": "ESP8266_GENERIC-FLASH_1M-20241025-v1.24.0.bin",
        "models": []
    }
}

RP2040 = {
    "promicro": {
        "firmware": "SPARKFUN_PROMICRO-20241025-v1.24.0.uf2",
        "models": [
            "AdaFruit KB2040 (Kee Boar Driver)"
        ]
    },

    "itsybitsy": {
        "firmware": "ADAFRUIT_ITSYBITSY_RP2040-20241025-v1.24.0.uf2",
        "models": []
    }
}

CHIPS = {
    "esp32": {
        "versions": ESP32,
        "install_hints": {
            "address": 0x1000
        },
    },
    "esp8266": {
        "versions": ESP8266,
        "install_hints": {
            # --baud 460800
            "address": 0x0
        },
    },
    "rp2040": {
        "versions": RP2040,
        "install_hints": {
            "doc": "docs/rp2040/kb2040.md"
        }
    }
}


def _get_firmware(chip, name):
    fw_versions = CHIPS.get(chip, {}).get("versions", {})
    return fw_versions.get(name, {}).get("firmware")


@task
def list(ctx):
    for chip_name, chip_info in CHIPS.items():
        print(f"===== {chip_name} =====")
        fw_vers = chip_info.get("versions")
        for fw_name, fw_info in fw_vers.items():
            print(f"* {fw_name} [{'|'.join(fw_info['models'])}]")


@task
def download(ctx, chip, fw_name):
    """ Download Micropython Firmware """
    firmware = _get_firmware(chip, fw_name)
    if firmware:
        dl_dir = f"{FIRMWARE_DIR}/{chip}"
        os.makedirs(dl_dir, exist_ok=True)

        ctx.run(f"wget -O {dl_dir}/{firmware} {FIRMWARE_BASE_URL}/{firmware}")
    else:
        print(f"=> Unknown firmware for {chip}/{fw_name}")


@task
def erase(ctx, chip):
    """
    Erase Firmware

    **ONLY** Supports ESP
    """
    port = ports.find_port()
    chip_ok = chip.startswith("esp")

    if chip_ok and port:
        execute = input(f"Erase {chip} Device at {port}? ")
        if execute == "yes":
            ctx.run(f"esptool.py --port {port} erase_flash")
        else:
            print("=> Operation Cancelled")
    else:
        print(f"=> Chip not supported: [{chip}] OR No device found: [{port}]")


@task
def install(ctx, chip, fw_name):
    """
    Install Micropython Firmware

    **ONLY** Supports ESP
    """
    port = ports.find_port()
    chip_ok = chip.startswith("esp")
    firmware = _get_firmware(chip, fw_name)
    install_hints = CHIPS.get(chip, {}).get("install_hints", {})

    if chip_ok and port and firmware:
        fw_dir = f"{FIRMWARE_DIR}/{chip}"
        fw_path = f"{fw_dir}/{firmware}"

        if not os.path.exists(fw_path):
            download(ctx, chip, fw_name)

        execute = input(f"Install {fw_path} on {port}? ")
        if execute == "yes":
            erase(ctx, chip)
            ctx.run(f"esptool.py --chip {chip} --port {port} write_flash --flash_size=detect {install_hints['address']} {fw_path}")
        else:
            print("=> Operation Cancelled")
    else:
        print(f"=> Unable to proceed with Chip <{chip}> | Port <{port}> | FWare <{firmware}>")
        doc = install_hints.get("doc")
        if doc:
            print(f"=> See {doc}")


@task
def clean(ctx):
    """ Clean Up Firmware Droppings """
    shutil.rmtree(FIRMWARE_DIR)










#
