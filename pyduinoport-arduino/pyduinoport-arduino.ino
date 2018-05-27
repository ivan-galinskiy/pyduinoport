#include "comms.hpp"
#include "ports.hpp"

void setup() 
{
  Serial.begin(115200);
}

void loop() 
{
  // Wait for the full command to arrive
  if (Serial.available() == sizeof(CMD))
  {
    // Read the bytes into a CMDu structure
    CMDu r_cmd;
    for(unsigned int i=0; i < sizeof(CMD); i++)
    {
      r_cmd.arr[i] = byte(Serial.read());
    }

    bool rw_bit = ((r_cmd.c.cmd_code & 0b10000000) != 0);
    uint8_t reg_type = ((r_cmd.c.cmd_code & 0b01100000) >> 5);
    uint8_t reg_letter = (r_cmd.c.cmd_code & 0b00011111);

    // If we are about to write...
    if (rw_bit == 1)
    {
      *(general_ports[reg_type][reg_letter]) = r_cmd.c.contents;
      DDRC |= r_cmd.c.contents;
      PORTC |= r_cmd.c.contents;
    }

    // If we are about to read, then send a command to the PC
    else
    {
      CMDu s_cmd;
      s_cmd.c.cmd_code = r_cmd.c.cmd_code;      

      // Load the response with the contents of a given port
      s_cmd.c.contents = *(general_ports[reg_type][reg_letter]);
      Serial.write(s_cmd.arr, sizeof(CMD));
    }
    
  }
}
