from network import  STA_IF, WLAN
import ujson

ssid = ''

try:
    with open('conf/wifi.conf','r') as f:
        wifiConf = ujson.load(f)
        print(wifiConf)
        ssid = wifiConf['ssid']
except Exception as e:
    print('read wifi',e.__class__.__name__,e) 

print("ssid = " +wifiConf['ssid'])

sta = WLAN(STA_IF)
sta.active(True)
sta.connect(wifiConf['ssid'],wifiConf['pwd'])
while not sta.isconnected():
    pass
print(sta.isconnected())
print(sta.ifconfig())