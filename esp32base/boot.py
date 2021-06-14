# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()



import ujson
import time
import ssd1306
from machine import Pin,I2C

# 全局错误消息字典
err = {
    'info':'',
}

# wifi配置信息判断
def hasWifiConfig():
    try:
        f = open('conf/wifi.conf','r')
        wifiJson = f.read()
        print(wifiJson)
        wifiDict = ujson.loads(wifiJson)
        print(wifiDict)
        f.close()
        if wifiDict["ssid"]:
            return True
        else:
            return False
    except:
        return False

# ssd1306初始化
# i2c = I2C(scl=Pin(14), sda=Pin(2), freq=100000)
i2c = I2C(scl=Pin(25), sda=Pin(26), freq=100000)
oled = ssd1306.SSD1306_I2C(128,64,i2c)

# boot按钮定义
boot = Pin(0,Pin.IN)

# 如果有wifi配置信息，则执行3秒等待，等待用户手动进入wifi配网程序
if hasWifiConfig():
    # 提示信息
    oled.text("press [boot]",0,0)
    oled.text("to setup",0,10)
    oled.show()
    for i in range(3):    
        time.sleep(1)
        oled.pixel(75+i*4,17,1)
        oled.show()

    # 读取boot按钮状态
    # 如果boot被按下，则进入WiFi配网程序，否则进入功能程序
    bootValue = boot.value()
    if bootValue:
        exec(open('./setup/tandh.py').read(),globals())
    else:
        exec(open('./setup/setup.py').read(),globals())
# 如果没有WiFi配置信息，则自动进入wifi配网程序
else:
    exec(open('./setup/setup.py').read(),globals())