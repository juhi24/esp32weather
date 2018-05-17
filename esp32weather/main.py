import time
import machine
import ubinascii
import ssd1306
from umqtt.robust import MQTTClient
from config import mqtt_broker, mqtt_user, mqtt_pass


CLIENT_ID = ubinascii.hexlify(machine.unique_id())


def reset_oled(pin_id=16):
    p_rst = machine.Pin(pin_id, machine.Pin.OUT)
    p_rst.value(0)
    time.sleep_ms(50)
    p_rst.value(1)


def init_oled(rst_pin_id=16, scl_pin_id=15, sda_pin_id=4):
    reset_oled(rst_pin_id)
    i2c = machine.I2C(scl=machine.Pin(15), sda=machine.Pin(4))
    oled = ssd1306.SSD1306_I2C(128, 64, i2c)
    oled.fill(0)
    return oled


OLED = init_oled()


def sub_cb(topic, msg):
    print(msg)
    OLED.fill(0)
    OLED.text('Kum: ' + msg.decode() + ' C', 0, 0)
    OLED.show()


def main():
    mqtt = MQTTClient(CLIENT_ID, mqtt_broker, user=mqtt_user, password=mqtt_pass)
    mqtt.set_callback(sub_cb)
    print('connecting MQTT')
    mqtt.connect()
    mqtt.subscribe('fmi/kumpula/t2m')
    mqtt.check_msg()
    time.sleep(1)
    #mqtt.check_msg()
    while True:
        mqtt.check_msg()
        time.sleep(300)
    mqtt.disconnect()


if __name__ == '__main__':
    main()
