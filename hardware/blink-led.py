import time
import board
import digitalio

def main():
    led = digitalio.DigitalInOut(board.C7)
    led.direction = digitalio.Direction.OUTPUT

    while True:
        led.value = True
        time.sleep(1)
        led.value = False
        time.sleep(1)


if __name__ == "__main__":
    main()
