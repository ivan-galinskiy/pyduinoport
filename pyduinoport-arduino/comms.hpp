// Define the structure of commands received from and sent to the computer
typedef struct 
{
  // Whether to read or write (read=0, write=1)
  bool op_code : 1;

  // Type of register to write to (0: PIN, 1:PORT, 2:DDR)
  uint8_t reg_type: 2;

  // Letter of the register: (B, C, D, E, F)
  uint8_t reg_letter: 5;

  // Contents to write to this register
  uint8_t contents;
} __attribute__((__packed__)) CMD;

// Test that the command indeed has the right size
static_assert(sizeof(CMD) == 2, "Command structure size incorrect");

// What's below is just to be able to access the command both as a command and as a byte list (for easy serial reading)
typedef union
{
  CMD c;
  byte arr[sizeof(CMD)];
} CMDu;

static_assert(sizeof(CMDu) == 2, "Command structure size incorrect");

