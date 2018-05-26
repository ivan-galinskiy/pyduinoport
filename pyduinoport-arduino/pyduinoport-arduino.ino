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

    // If we are about to write...
    if (r_cmd.c.op_code == 1)
    {
      *(general_ports[r_cmd.c.reg_type][r_cmd.c.reg_letter]) = r_cmd.c.contents;
    }

    // If we are about to read, then send a command to the PC
    else
    {
      CMDu s_cmd;
      s_cmd.c.op_code = 0;
      s_cmd.c.reg_type = r_cmd.c.reg_type;
      s_cmd.c.reg_letter = r_cmd.c.reg_letter;

      // Load the response with the contents of a given port
      s_cmd.c.contents = *(general_ports[r_cmd.c.reg_type][r_cmd.c.reg_letter]);
      Serial.write(s_cmd.arr, sizeof(CMD));
    }
    
  }
}
