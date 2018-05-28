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
        # Some constants
        self._cmd_struct = struct.Struct("<BB")
        self._port_names = ["PIN", "PORT", "DDR"]
        self._port_letters = ["B", "C", "D", "E", "F"]
        
        # Indicate that the register values have not yet been read into the 
        # dict
        self._updated = False
        
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
            
        # Generate a dictionary that holds the ports' values (read them first)
        self._port_vals = {}
        for n in self._port_names:
            for let in self._port_letters:
                pf = "{0}{1}".format(n, let)
                self._port_vals[pf] = self[pf]
                
        # Indicate that the dict has been updated
        self._updated = True
            
        return
    
    
    def _gen_cmd_code(self, direction, port):
        """
        direction is either "w" or "r"
        port can be "PORTB", "PIND", etc
        value is a 8-bit integer
        """
        cmd_code = 0
        
        direction = int(direction.lower() == 'w')
        
        port = port.upper()
        port_type = port[:-1]
        port_letter = port[-1]
        
        port_type_num = self._port_names.index(port_type)
        port_letter_num = self._port_letters.index(port_letter)
        
        cmd_code |= direction << 7
        cmd_code |= port_type_num << 5
        cmd_code |= port_letter_num
        
        return cmd_code
    
    def __setitem__(self, port, value):
        port = port.upper()
        
        cmd_code = self._gen_cmd_code('w', port)
        
        self._ser.write(self._cmd_struct.pack(cmd_code, value))
        self._port_vals[port] = value
        
        return
    
    def __getitem__(self, port):
        port = port.upper()
        
        if (not self._updated) or port.startswith("PIN"):
            cmd_code = self._gen_cmd_code('r', port)
            
            self._ser.write(self._cmd_struct.pack(cmd_code, 0))
            
            # Now wait for the response
            answer = self._ser.read(size=self._cmd_struct.size)
            (ret_code, ret_val) = self._cmd_struct.unpack(answer)
            
            assert ret_code == cmd_code, "Returned command code incorrect"
        else:
            return self._port_vals[port]
        
        return ret_val
    
    def _bit_set(self, port, bit_num):
        self[port] = self[port] | (1 << bit_num)
            
    def _bit_clear(self, port, bit_num):
        self[port] = self[port] & (~(1 << bit_num))
    
    def set_pin_dir(self, pin, direction):
        pin_lett = pin[-2]
        pin_num = int(pin[-1])
        
        pin_ddr = "DDR{0}".format(pin_lett)
        
        if direction == "out":
            self._bit_set(pin_ddr, pin_num)
        elif direction == "in":
            self._bit_clear(pin_ddr, pin_num)
            
    def set_pin_val(self, pin, value):
        pin_lett = pin[-2]
        pin_num = int(pin[-1])
        
        pin_port = "PORT{0}".format(pin_lett)
        
        if value:
            self._bit_set(pin_port, pin_num)
        else:
            self._bit_clear(pin_port, pin_num)
    
if __name__ == "__main__":
    ar = Arduino(port="COM11")
    
#    led_bit = ((1 << 4) | (1 << 5))
#    ar["DDRB"] = led_bit
#    ar["PORTB"] = led_bit
#    
#    print("{0:b}".format(ar["PORTB"]))
    ar.set_pin_dir("PB4", "out")
    ar.set_pin_dir("PB5", "out")
    
    ar.set_pin_val("PB4", 1)
    ar.set_pin_val("PB5", 0)