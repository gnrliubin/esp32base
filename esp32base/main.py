def main():
    global err

    print(err)
    oled.fill(0)
    oled.text("app stop",0,0)
    
    oled.show()

    
    print(sta.ifconfig())

    print('rebooting')
    machine.reset()

if __name__ == '__main__':
    main()