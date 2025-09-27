"""
micropython.org/download
"""
import os
import shutil
from invoke import task

import ports
from boards import BOARDS

FIRMWARE_DIR = "./.firmware"
FIRMWARE_BASE_URL = "https://www.micropython.org/resources/firmware"


def _get_firmware(board_id):
    return BOARDS.get(board_id, {}).get("firmware")


@task
def list(ctx):
    """ Print Firmware (and other) information for all supported Boards """
    for brd_id, info in BOARDS.items():
        print(f"===== {brd_id} =====")
        desc = info.get("desc")
        if desc:
            print(f"{info['name']} // {desc}")
        else:
            print(info["name"])

        product_url = info.get("urls", {}).get("product")
        guide_url = info.get("urls", {}).get("guide")
        chip = info.get("chip", "UNSPECIFIED")
        firmware = _get_firmware(brd_id)

        specs = f"""
* Product: {product_url}
* Guide: {guide_url}
* Chip: {chip}
* Firmware: {firmware}
        """.strip()
        print(specs)
        print()


@task
def download(ctx, board_id):
    """ Download Micropython Firmware """
    firmware = _get_firmware(board_id)
    if firmware:
        dl_dir = f"{FIRMWARE_DIR}/{board_id}"
        os.makedirs(dl_dir, exist_ok=True)

        ctx.run(f"wget -O {dl_dir}/{firmware} {FIRMWARE_BASE_URL}/{firmware}")
    else:
        print(f"=> Unknown board: '{board_id}'")


@task
def erase(ctx, board_id):
    """
    Erase Firmware
    """
    port = ports.find_port()
    board = BOARDS.get(board_id, {})
    install_opts = board.get("install", {})
    install_tool = install_opts.get("tool", None)

    match install_tool:
        case "esptool":
            __esptool_erase(ctx, board["chip"], port)
        case _:
            print(f"=> Board not supported OR No device found: [{port}]")

@task
def install(ctx, board_id):
    """
    Install Micropython Firmware

    **ONLY** Supports ESP
    """
    board = BOARDS.get(board_id, {})
    install_opts= board.get("install", {})
    install_tool = install_opts.get("tool", None)

    port = ports.find_port()

    firmware = _get_firmware(board_id)
    fw_path = f"{FIRMWARE_DIR}/{board_id}/{firmware}"
    if not os.path.exists(fw_path):
        download(ctx, board_id)

    match install_tool:
        case "manual":
            doc = install_opts.get("doc")
            if doc:
                print(f"=> See {doc}")
            else:
                print(f"=> '{board_id}' has to be manually installed. No other informatin available.")
        case "esptool":
            __esptool_flash(ctx,
                board["chip"], port, install_opts["address"], fw_path)
        case _:
            print("=> Unknown install tool: '{install_tool}'")


def __esptool_erase(ctx, chip, port):
    execute = input(f"Erase {chip} Device at {port}? ")
    if execute == "yes":
        ctx.run(f"esptool.py --port {port} erase_flash")
    else:
        print("=> Erase Operation Cancelled")


def __esptool_flash(ctx, chip, port, address, fw_path):
    execute = input(f"Install {fw_path} on {port}? ")
    if execute == "yes":
        __esptool_erase(ctx, chip, port)
        ctx.run(f"esptool.py --chip {chip} --port {port} write_flash --flash_size=detect {address} {fw_path}")
    else:
        print("=> Flash Operation Cancelled")


@task
def clean(ctx):
    """ Clean Up Firmware Droppings """
    shutil.rmtree(FIRMWARE_DIR)










#
