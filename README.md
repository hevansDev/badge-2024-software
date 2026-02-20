# Badge Sim Autostart on Raspberry Pi (labwc)

The most reliable way to autostart the badge simulator on boot is via labwc's built-in autostart mechanism. This works better than systemd services (both system and user level) because it runs commands directly after the Wayland compositor has fully initialised, avoiding display environment timing issues.

Create ~/.config/labwc/autostart with the following line:

```bash/home/hugh/.local/share/virtualenvs/sim-BNHWup2C/bin/python /home/hugh/badge-2024-software/sim/run.py &```

The & is required to background the process so labwc continues starting normally.

## Why not systemd?

System-level services (/etc/systemd/system/) start too early and can't access the Wayland socket. User-level services (~/.config/systemd/user/) have better timing but still struggle to reliably inherit the correct Wayland session environment (WAYLAND_DISPLAY, XDG_RUNTIME_DIR) on this setup. The labwc autostart file sidesteps all of this by running within the compositor's own context.

> Note: If you update your pipenv environment and the virtualenv hash changes, update the path in the autostart file accordingly. Run pipenv --venv from the sim directory to get the current path.


[![Build Micropython](https://github.com/emfcamp/badge-2024-software/actions/workflows/build.yml/badge.svg)](https://github.com/emfcamp/badge-2024-software/actions/workflows/build.yml)

# Tildagon Firmware

Web flasher is available @ https://emfcamp.github.io/badge-2024-software/

## Running from a checkout

Clone the repository including submodules:

    git clone --recursive git@github.com:emfcamp/badge-2024-software.git

Connect your badge via usb, run mpremote to reset, connect to the badge and run the software:

    ./micropython/tools/mpremote/mpremote.py reset; sleep 3; ./micropython/tools/mpremote/mpremote.py mount modules
    import main

NB: mpremote can also be installed separately: https://docs.micropython.org/en/latest/reference/mpremote.html

## Building

To build with a consistent toolchain, use docker.

Pull the firmware build image:

    docker pull ghcr.io/emfcamp/esp_idf:v5.2.1

(Or build it yourself, if you prefer):

    docker build . -t ghcr.io/emfcamp/esp_idf:v5.2.1

Initialize submodules:

    git submodule update --init --recursive

To make the docker container with the right version of the ESP-IDF for the latest micropython.

Before you build the first time, apply any patches to vendored content:

    ./scripts/firstTime.sh

Then to build the images run:

    docker run -it --rm --env "TARGET=esp32s3" -v "$(pwd)"/:/firmware ghcr.io/emfcamp/esp_idf:v5.2.1

Alternatively, to flash a badge:
    put the badge into bootloader by disconnecting the usb in, press and hold bat and boop buttons for 20 seconds  then reconnect the usb in and run:

    docker run -it --rm --device /dev/ttyACM0:/dev/ttyUSB0 --env "TARGET=esp32s3" -v "$(pwd)"/:/firmware ghcr.io/emfcamp/esp_idf:v5.2.1 deploy

where /dev/ttyACM0 is the device's endpoint. This value is correct on Linux.

> [!IMPORTANT]  
> On macOS, Docker does not have access to the host's USB devices. You will need to use a different method to flash the badge, such as [using the web flasher](flasher/README.md).

## Contributing

Please install pre-commit to ensure ruff is run:

    python3 -m pip install pre-commit
    pre-commit install
