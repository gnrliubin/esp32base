# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()

import time
import ssd1306
from machine import Pin,I2C


# ssd1306初始化
i2c = I2C(scl=Pin(14), sda=Pin(2), freq=100000)
oled = ssd1306.SSD1306_I2C(128,64,i2c)

# boot按钮定义
boot = Pin(0,Pin.IN)

# 提示信息
oled.text("press [boot]",0,0)
oled.text("to setup",0,10)
oled.show()
for i in range(3):    
    time.sleep(1)
    oled.pixel(75+i*4,17,1)
    oled.show()

# 读取boot按钮状态
bootValue = boot.value()
if bootValue:
    exec(open('./main.py').read(),globals())
else:
    exec(open('./setup/setup.py').read(),globals())