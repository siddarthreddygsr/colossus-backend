import time
import RPi.GPIO as GPIO


sensor_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor_pin, GPIO.IN)


def read_and_print_data():
    while True:
        sensor_data = GPIO.input(sensor_pin)
        print("Sensor Data:", sensor_data)
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        read_and_print_data()
    except KeyboardInterrupt:
        GPIO.cleanup()
