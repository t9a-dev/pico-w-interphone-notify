# screen /dev/tty.usb_name 115200
import os
import board
import analogio
import time
import setupWifi
import apiClient

socket = setupWifi.run()
notify = apiClient.notify(socket)
loop_count = 0
sensor_val = 0
connection_test_interval = 0

# ADC2(Raspberrypi Pico W GPIOピン34)の値を取得
adc2 = analogio.AnalogIn(board.A2)
notifySensorThreshold = os.getenv('NOTIFY_SENSOR_THRESHOLD')

# 起動時に一度LINEに通知を送る。(正しくネットワークに接続していることを確認するため)
notify.pushToNtfy('https://home-ntfy.t9a.dev/test','Raspberry Pi Pico Wが起動しました。')

def get_voltage(pin):
    return (pin.value * 3.3) / 65536


while True:
    if connection_test_interval > 60:
        notify.requestTest()
        connection_test_interval = 0
        loop_count = 0

    connection_test_interval = connection_test_interval + 1
    time.sleep(1)
    # 光センサーの値。センサーを光で照らしたり手で覆ったりすると値が変わるのでこの値を参考にしてsettings.tomlのNOTIFY_SENSOR_THRESHOLDを調整すること。
    sensor_val = get_voltage(adc2)
    print(sensor_val)
    if sensor_val > notifySensorThreshold:
        notify.pushToNtfy('https://home-ntfy.t9a.dev/bell','インターホンが押されました')
    loop_count = loop_count + 1
    print('loop_count: ')
    print(loop_count)
