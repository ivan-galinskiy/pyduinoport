# -*- coding: utf-8 -*-
"""
Created on Sun May 27 01:37:26 2018

@author: Ivan Galinskiy
"""

from __future__ import print_function
from __future__ import division

import serial
import struct
import time

class Arduino:
    def __init__(self, port="COM11", baud=115200, reset=False):
        self._cmd_struct = struct.Struct("<BB")
        
        if reset:
            # Black magic below resets Arduino Micro
            # First, we need to open the port at 9600 baud
            ser_reset = serial.Serial(port, 9600)
            ser_reset.close()
            
            # Then, open it at 1200 baud and that will trigger reset.
            ser_reset = serial.Serial(port, 1200)
            ser_reset.close()
            time.sleep(10)
        
        self._ser = serial.Serial(port, baud)
        
        # Wait for the Duino to reboot if it does
        time.sleep(3)
        
        try:
            self._ser.reset_input_buffer()
            self._ser.reset_output_buffer()
        except AttributeError:
            # Happens for older versions of PySerial
            self._ser.flushInput()
            self._ser.flushOutput()
        return
    
    
    def _gen_cmd_code(self, direction, port):
        """
        direction is either "w" or "r"
        port can be "PORTB", "PIND", etc
        value is a 8-bit integer
        """
        cmd_code = 0
        
        direction = int(direction.lower() == 'w')
        
        ports = ["PIN", "PORT", "DDR"]
        letters = ["B", "C", "D", "E", "F"]
        
        port = port.upper()
        port_type = port[:-1]
        port_letter = port[-1]
        
        port_type_num = ports.index(port_type)
        port_letter_num = letters.index(port_letter)
        
        cmd_code |= direction << 7
        cmd_code |= port_type_num << 5
        cmd_code |= port_letter_num
        
        return cmd_code
    
    def write_port(self, port, value):
        cmd_code = self._gen_cmd_code('w', port)
        
        self._ser.write(self._cmd_struct.pack(cmd_code, value))
        return
    
    def read_port(self, port):
        cmd_code = self._gen_cmd_code('r', port)
        
        self._ser.write(self._cmd_struct.pack(cmd_code, 0))
        
        # Now wait for the response
        answer = self._ser.read(size=self._cmd_struct.size)
        (ret_code, ret_val) = self._cmd_struct.unpack(answer)
        
        assert ret_code == cmd_code, "Returned command code incorrect"
        
        return ret_val
    
if __name__ == "__main__":
    ar = Arduino(port="COM11")
    
    led_bit = ((1 << 4) | (1 << 5))
    ar.write_port("DDRB", led_bit)
    ar.write_port("PORTB", led_bit)
    
    print("{0:b}".format(ar.read_port("PORTB")))