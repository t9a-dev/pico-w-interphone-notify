# screen /dev/tty.usb_name 115200
import os
import board
import analogio
import time
import setupWifi
import apiClient

socket = setupWifi.run()
notify = apiClient.notify(socket)

# ADC2(Raspberrypi Pico W GPIOピン34)の値を取得
adc2 = analogio.AnalogIn(board.A2)
notifySensorThreshold = os.getenv('NOTIFY_SENSOR_THRESHOLD')

# 起動時に一度LINEに通知を送る。(正しくネットワークに接続していることを確認するため)
notify.pushToNtfy('test','Raspberry Pi Pico Wが起動しました。')

def get_voltage(pin):
    return (pin.value * 3.3) / 65536


while True:
    notify.requestTest()
    time.sleep(1)
    # 光センサーの値。センサーを光で照らしたり手で覆ったりすると値が変わるのでこの値を参考にしてsettings.tomlのNOTIFY_SENSOR_THRESHOLDを調整すること。
    print(get_voltage(adc2))
    if get_voltage(adc2) > notifySensorThreshold:
        notify.pushToNtfy('bell','インターホンが押されました')
