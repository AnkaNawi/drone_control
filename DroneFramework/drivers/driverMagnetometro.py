#!/usr/bin/python
import smbus
import time
import math

bus = smbus.SMBus(0)
address = 0x1e


def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def write_byte(adr, value):
    bus.write_byte_data(address, adr, value)

try:
	while 1 :
		write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
		write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
		write_byte(2, 0b00000000) # Continuous sampling

		scale = 0.92

		x_out = read_word_2c(3) * scale
		y_out = read_word_2c(7) * scale
		z_out = read_word_2c(5) * scale

		bearing  = math.atan2(y_out, x_out)
		if (bearing < 0):
			bearing += 2 * math.pi

		print "Bearing: ", math.degrees(bearing)
		time.sleep( .2 )
except KeyboardInterrupt:
	print "Termino la lectura: magnetometro"


#modified by Diego Garcia
from driver import Driver
class DriverMagnetometro(Driver):

	def getData(self):

		write_byte(0, 0b01110000) # Set to 8 samples @ 15Hz
		write_byte(1, 0b00100000) # 1.3 gain LSb / Gauss 1090 (default)
		write_byte(2, 0b00000000) # Continuous sampling

		scale = 0.92

		x_out = read_word_2c(3) * scale
		y_out = read_word_2c(7) * scale
		z_out = read_word_2c(5) * scale

		bearing  = math.atan2(y_out, x_out)
		if (bearing < 0):
			bearing += 2 * math.pi

		return {'angulo' : math.degrees(bearing)}

	def getStatus(self):
		# tiene los datos del sensor
		#  ok, no_ok, excepcion,
		raise NotImplementedError( "Should have implemented this" )

	def forceRead(self):
		# fuerza a hacer una nueva lectura al sensor
		return self.getData()

	def reset(self):
		# inicializa datos sensor
		raise NotImplementedError( "Should have implemented this" )