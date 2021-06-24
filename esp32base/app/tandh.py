
from network import  STA_IF, WLAN
import ujson
import dht 
import time
from umqtt.simple import MQTTClient
from machine import Pin,WDT
import usys
import micropython

global err
wdt = WDT(timeout = 5000)

##################读取配置##########################
# 读取wifi配置并尝试连接wifi
try:
    with open('conf/wifi.conf','r') as f:
        wifiConf = ujson.load(f)
        print(wifiConf)
except Exception as e:
    print('read wifi:',e.__class__.__name__,e) 
    err['info'] = 'read wifi:',e.__class__.__name__,e
    usys.exit()

print("ssid = " +wifiConf['ssid'])
wdt.feed()

oled.fill(0)
oled.text(wifiConf['ssid'],0,10)
oled.text("connecting ...",0,20)
oled.show()

sta = WLAN(STA_IF)
sta.active(True)
sta.connect(wifiConf['ssid'],wifiConf['pwd'])
while not sta.isconnected():
    wdt.feed()
    time.sleep(1)
print(sta.isconnected())
print(sta.ifconfig())

# 读取感应器位置信息和发送主题
try:
    with open('conf/inspector.conf','r') as f:
        inspector = ujson.load(f)
        print(inspector)
except Exception as e:
    print('read inspector:',e.__class__.__name__,e) 
    err['info'] = 'read inspector:',e.__class__.__name__,e
    usys.exit()
wdt.feed()


#######################应用功能实现########################

# mqtt信息
# @status 状态【online offline restart update】
# @msg 一般为空，当status因为错误导致restart时，会包含错误信息
payload = {
    'id':inspector['tower'],
    't':0,
    'h':0,
    'r':-300,
    "status":"offline",
    "msg":""
}
clientid = inspector['topic']

oled.fill(0)
oled.text(inspector['tower'],0,0)
oled.text(str(sta.ifconfig()[0]),0,20)
oled.show()

wdt.feed()
client = MQTTClient(clientid,server="measure.sumg.press",user="goss_rexroth",password="goss_rexroth_1234",port=8883,ssl=True,keepalive=5)
payloadJson = ujson.dumps(payload)
print(payloadJson)
client.set_last_will(inspector['topic'],payloadJson,retain=True)
# client.set_last_will(topic, b"{'id':'"+tower+"','t':0,'h':0,'r':0,'status':'offline'}",retain=True)
try:
    client.connect()
except Exception as e:
        print("mqtt connect error,restart")
        err['info'] = 'connect:',e.__class__.__name__,e
        usys.exit()
        # machine.reset()

wdt.feed()

oled.text("mqtt connected!",0,40)
oled.show()

# DHT11温湿度
d = dht.DHT22(Pin(5))

while True:
    try:
        d.measure()
        payload['status'] = "online"
        payload['t'] = d.temperature()
        payload['h'] = d.humidity()
        payload['r']= sta.status("rssi")
        payloadJson = ujson.dumps(payload)
        print(payloadJson)
    except Exception as e:
        print("dht22 error,restart:",e.__class__.__name__,e)
        payload['status'] = "DHTError"
        payload['t'] = 0
        payload['h'] = 0
        payload['r']=sta.status("rssi")
        payloadJson = ujson.dumps(payload)
        print(payloadJson)
    try:
        client.publish(inspector['topic'], payloadJson)
    except Exception as e:
        print("publish:",e.__class__.__name__,e)
        err['info'] = 'publish:',e.__class__.__name__,e
        usys.exit()
        # machine.reset()
    # print("t: "+str(t)+" °C")
    # print("h: "+str(h)+" %RH")
    # print(wlan.status("rssi"))
    print(micropython.mem_info())
    wdt.feed()
    time.sleep(1)