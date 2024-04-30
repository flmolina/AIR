import os
import sys
import time


class RaspberryPi:
    # Pin definition
    RST_PIN     = 18
    CS_PIN      = 22
    DRDY_PIN    = 17
    BREAK_PIN   = 23 #Señal de disparo 

    def __init__(self):
    # SPI device, bus = 0, device = 0
        import spidev
        import RPi.GPIO
        
        self.GPIO = RPi.GPIO
        self.SPI = spidev.SpiDev(0, 0)

    def digital_write(self, pin, value):
        self.GPIO.output(pin, value)

    def digital_read(self, pin):
        return self.GPIO.input(pin)

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.SPI.writebytes(data)
        
    def spi_readbytes(self, reg):
        return self.SPI.readbytes(reg)
        
    def module_init(self):
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(self.RST_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.CS_PIN, self.GPIO.OUT)
        self.GPIO.setup(21,self.GPIO.OUT)
        self.GPIO.setup(self.DRDY_PIN, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
        self.SPI.max_speed_hz = 2000000
        self.SPI.mode = 0b01
        return 0;

    def module_exit(self):
        self.SPI.close()
        self.GPIO.output(self.RST_PIN, 0)
        self.GPIO.output(self.CS_PIN, 0)
        
        
class JetsonNano:
    # Pin definition
    RST_PIN         = 18
    CS_PIN          = 22
    DRDY_PIN        = 17

    def __init__(self):
        import spidev
        self.SPI = spidev.SpiDev(0, 0)
        
        #import Jetson.GPIO
        self.GPIO = 1#Jetson.GPIO

    def digital_write(self, pin, value):
        self.GPIO.output(pin, value)

    def digital_read(self, pin):
        return self.GPIO.input(pin)

    def delay_ms(self, delaytime):
        time.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.SPI.writebytes(data)
        
    def spi_readbytes(self, reg):
        return self.SPI.readbytes(reg)

    def module_init(self):
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)
        self.GPIO.setup(self.RST_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.CS_PIN, self.GPIO.OUT)
        self.GPIO.setup(self.DRDY_PIN, self.GPIO.IN)
        self.SPI.max_speed_hz = 100000000
        self.SPI.mode = 0b01
        return 0

    def module_exit(self):
        self.SPI.close()
        self.GPIO.output(self.RST_PIN, 0)

        self.GPIO.cleanup()



        
if os.path.exists('/sys/bus/platform/drivers/gpiomem-bcm2835'):
    implementation = RaspberryPi()
else:
    implementation = JetsonNano()

for func in [x for x in dir(implementation) if not x.startswith('_')]:
    setattr(sys.modules[__name__], func, getattr(implementation, func))
