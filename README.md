# invoke-tasks
Library of Invoke Tasks

## circuitpython
CircuitPython Project Management

```bash
clean                         Clean Stuff
shell                         Use picocom to run the REPL
install.clean                 Remove files from device.
install.file                  Copy given file to device
install.main                  Always copy given file as `main.py`
install.project               Install the named Project and Dependencies
install.settings              Install settings.toml
install.view (install.list)   View / List the contents of the device
```

## micropython
Micropython Project Management

```bash
shell               Use picocom to run the REPL
clean.device        Erase all files on the device
clean.mpy           Delete all local .mpy files
firmware.clean      Clean Up Firmware Droppings
firmware.download   Download Micropython Firmware
firmware.erase      Erase Firmware
firmware.install    Install Micropython Firmware
firmware.list       Print Firmware (and other) information for all supported Boards
install.boot        Install source file as `boot.py`
install.compile     Compile a .py source file to .mpy
install.file        Install a file on a device
install.main        Install source file as `main.py`
install.project     Install a Project from a YML File
```

## system
System Tasks

```bash
backup.status   Status of a Duplicity Backup Collection
```
