def main():
    print("Welcome to RT-Thread MicroPython!")
    oled.fill(0)
    oled.text("app stop",0,0)
    
    oled.show()

    
if __name__ == '__main__':
    main()