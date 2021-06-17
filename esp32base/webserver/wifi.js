
setType = document.getElementById("set-type")
wifiMan = document.getElementById("wifi-man")
wifiAuto = document.getElementById("wifi-auto")
wifiPwdRow = document.getElementById("wifi-pwd-row")
wifiPwd = document.getElementById("wifi-pwd")
wifiPwdShowRow = document.getElementById("wifi-pwd-show-row")
wifiPwdShow = document.getElementById("wifi-pwd-show")
showPwd = document.getElementById("show-pwd")

changeType=function(){
    wifiMan.hidden=!setType.checked
    wifiAuto.hidden=setType.checked
}
showPwdHandle = function(){
    if(showPwd.checked){
        wifiPwdRow.style.display = "none"
        wifiPwdShowRow.style.display = "block"
    }else{
        wifiPwdRow.style.display = "block"
        wifiPwdShowRow.style.display = "none"
    }
}
pwdchanged = function(){
    wifiPwdShow.value=wifiPwd.value
    console.log(wifiPwdShow.value ,wifiPwd.value)
   
}
pwdShowchanged = function(){
    wifiPwd.value = wifiPwdShow.value
    console.log(wifiPwdShow.value ,wifiPwd.value) 
}

submit = function(){
    var ssid
    var pwd
    
    ssid = setType.checked? wifiMan.value:wifiAuto.value
    pwd = showPwd.checked? wifiPwdShow.value:wifiPwdShow.value
    location.href="/setwifi?ssid="+ssid+"&pwd="+pwd
}