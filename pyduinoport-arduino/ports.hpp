//typeof(PORTB)* PORTs[] = {&PORTB, &PORTC, &PORTD, &PORTE, &PORTF};
//typeof(PORTB)* PINs[] = {&PINB, &PINC, &PIND, &PINE, &PINF};
//typeof(PORTB)* DDRs[] = {&DDRB, &DDRC, &DDRD, &DDRE, &DDRF};

typeof(PORTB)* general_ports[3][5] = {
  {&PINB, &PINC, &PIND, &PINE, &PINF},
  {&PORTB, &PORTC, &PORTD, &PORTE, &PORTF},
  {&DDRB, &DDRC, &DDRD, &DDRE, &DDRF}
};

