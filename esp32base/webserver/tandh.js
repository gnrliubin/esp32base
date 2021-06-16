var equipName = document.getElementById('equip-name')
var no = document.getElementById('equip-no')
var tower = document.getElementById('equip-tower')
var unit = document.getElementById('equip-unit')
var unitRow = document.getElementById('equit-unit-row')
console.log(unitRow)

folder = function(){
    if (tower.value=="f"){
        unitRow.style.display='none'
    }else{
        unitRow.style.display='block'
    }
}

submit = function(){
    towerCode = ''
    topic = ''
    if (tower.value=='f'){
        towerCode = no.value+'-'+tower.value
    }else{
        towerCode = no.value+'-'+tower.value+'-'+unit.value
    }

    topic = 'tandh/'+equipName.value+'/rexroth/'+towerCode
    console.log(topic)
}