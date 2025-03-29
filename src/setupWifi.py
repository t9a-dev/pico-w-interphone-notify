# SPDX-FileCopyrightText: 2022 Liz Clark for Adafruit Industries
#
# SPDX-License-Identifier: MIT
import os
import microcontroller
import wifi
import socketpool


def run():
    print()
    print("Connecting to WiFi")

    try:
        #  connect to your SSID
        wifi.radio.connect(os.getenv('CIRCUITPY_WIFI_SSID'),
                           os.getenv('CIRCUITPY_WIFI_PASSWORD'))
    except:
        # Wi-Fiアクセスポイントに接続できなければ再起動(ハードリセット)する。
        # https://learn.adafruit.com/circuitpython-essentials/circuitpython-resetting#hard-reset-3087083
        microcontroller.reset()

    print("Connected to WiFi")

    #  prints MAC address to REPL
    print("My MAC addr:", [hex(i) for i in wifi.radio.mac_address])

    #  prints IP address to REPL
    print("My IP address is", wifi.radio.ipv4_address)

    #  pings Google
    # ipv4 = ipaddress.ip_address("8.8.4.4")
    # print("Ping google.com: %f ms" % (wifi.radio.ping(ipv4)*1000))

    return socketpool.SocketPool(wifi.radio)
