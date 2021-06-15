from network import AP_IF, STA_IF, WLAN
import random
import ESP8266WebServer
import ujson

global err

# 随机产生ssid
apId = str(random.getrandbits(16))
# apId = "esp"
# 定义密码
pwd = "esp123456"

# 开启热点
ap = WLAN(AP_IF)
ap.active(True)
# 密码默认为：micropythoN
# 密码需要8位以上，否则会报错OSError: can't set AP config
# 密码不能纯数字，否则会拒绝接入
ap.config(essid=apId,password=pwd,channel=11)
ip = ap.ifconfig()[0]

sta = WLAN(STA_IF)
sta.active(True)




# 屏幕提示信息
oled.fill(0)
oled.text("setup model",0,0)
oled.text("ssid:"+apId,0,20)
oled.text("pwd:"+pwd,0,30)
oled.text("ip:"+ip,0,40)
oled.text("open ip to setup",0,50)
oled.show()




def scanWIFI():
    ssidList = ""
    print("scaning start")
    ssids = sta.scan()
    print("scaning stop")
    for ssid in ssids:
        ssidList+="<option value='"+ssid[0].decode()+"'>"+ssid[0].decode()+"</option>"
    return ssidList


def getAppList():
    appsOption = ""
    try:
        with open('conf/appList.conf','r') as appList:
            apps=ujson.load(appList)
            for app in apps:
                appsOption += "<option value='%s'>%s</option>" % (apps[app]['web'],apps[app]["name"])
            print(appsOption)
    except Exception as e:
        print('read app list:',e.__class__.__name__,e) 
        err['info'] = 'read app list:'+e.__class__.__name__,e
        appsOption = '''<option value = "">%s</option>''' % e.__class__.__name__
    return appsOption

ledData = {
    "appsOption":getAppList(),
    "wifiOption":scanWIFI(),
    "equitNo":"1",
    "towerNo":"1",
    "towerPosition":"d",
    "sensorPoint":"rexroth"
}
print(ledData)

def indexHandel(socket,args):
    
    if 'ssid' in args and 'pwd' in args:
        wifi = {
            "ssid":args['ssid'],
            "pwd":args['pwd']
        }
        try:
            wifiJson=ujson.dumps(wifi)
            print(wifiJson)
            with open("conf/wifi.conf",'w') as f:
                f.write(wifiJson)
        except Exception as e :
            print('write wifi.conf:',e.__class__.__name__,e) 
            err['info'] = 'write wifi.conf:'+e.__class__.__name__,e

        ESP8266WebServer.ok(socket,"200","ok")
    else:
        ESP8266WebServer.ok(socket,"200","nothing to do")

ESP8266WebServer.begin(80)

ESP8266WebServer.onPath('/cmd',indexHandel)
ESP8266WebServer.onPath('/webserver',indexHandel)
ESP8266WebServer.setDocPath('/')
ESP8266WebServer.setTplData(ledData)

try:
    while True:
        # Let server process requests
        ESP8266WebServer.handleClient()
except:
    ESP8266WebServer.close()

