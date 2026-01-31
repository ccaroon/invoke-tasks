BOARDS = {
    "kb2040": {
        "name": "Adafruit KB2040",
        "desc": "AdaFruit KB2040 (Kee Boar Driver)",
        "urls": {
            "product": "https://www.adafruit.com/product/5302",
            "guide": "https://learn.adafruit.com/adafruit-kb2040/overview"
        },
        "chip": "rp2040",
        "firmware": "SPARKFUN_PROMICRO-20251209-v1.27.0.uf2",
        "install": {
            "tool": "manual",
            "doc": "https://github.com/ccaroon/mikros/blob/master/micropython/docs/rp2040/kb2040.md"
        }
    },
    "feather-m4-ex": {
        "name": "Feather M4 Express",
        "desc": "ATSAMD51 32-bit Cortex M4 core running at 120 MHz, 32-bit, 3.3V logic and power",
        "urls": {
            "product": "https://www.adafruit.com/product/3857",
            "guide": "https://learn.adafruit.com/adafruit-feather-m4-express-atsamd51"
        },
        "chip": "cortex-m4",
        "firmware": "ADAFRUIT_FEATHER_M4_EXPRESS-20250911-v1.26.1.uf2",
        "install": {
            "tool": "manual",
            "doc": "https://github.com/ccaroon/mikros/blob/master/micropython/docs/feather-m4-ex/README.md"
        }
    },
    "huzzah-32": {
        "name": "AdaFruit Huzzah-32 Feather",
        "desc": "Uses the GENERIC OTA firmware",
        "urls": {
            "product": "https://www.adafruit.com/product/3405",
            "guide": "https://learn.adafruit.com/adafruit-huzzah32-esp32-feather"
        },
        "chip": "esp32",
        "firmware":"ESP32_GENERIC-OTA-20250911-v1.26.1.bin",
        "install": {
            "tool": "esptool",
            "address": 0x1000
        },
    },
    "esp32-generic": {
        "name": "Generic ESP32",
        "desc": "Any board that can use the GENERIC firmware",
        "models": ["SparkFun MicroMod-ESP32"],
        "chip": "esp32",
        "firmware": "ESP32_GENERIC-20241025-v1.24.0.bin",
        "install": {
            "tool": "esptool",
            "address": 0x1000
        },
    },
    "huzzah-8266": {
        "name": "AdaFruit Huzzah 8266 Feather",
        "desc": "",
        "urls": {
            "product": "https://www.adafruit.com/product/2821",
            "guide": "https://learn.adafruit.com/adafruit-feather-huzzah-esp8266"
        },
        "chip": "esp8266",
        "firmware":"ESP8266_GENERIC-20241025-v1.24.0.bin",
        "install": {
            "tool": "esptool",
            "address": 0x0,
        },
    }
}
