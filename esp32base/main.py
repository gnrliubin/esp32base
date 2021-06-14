def main():
    global err

    print(err)
    oled.fill(0)
    oled.text("app stop",0,0)
    
    oled.show()

    
if __name__ == '__main__':
    main()