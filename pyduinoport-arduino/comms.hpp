// Define the structure of commands received from and sent to the computer
typedef struct 
{
  // Cmd code that is write/read bit, 2 bits to select PIN/PORT/DDR (0: PIN, 1:PORT, 2:DDR), 5 bits for register letter (B, C, D, E, F)
  uint8_t cmd_code;

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

