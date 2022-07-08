#include "config.h"

// mXoutY faz referencia a saida (out) Y do motor X

#define m1out1 PORTAbits.RA2
#define m1out2 PORTAbits.RA1
#define m2out1 PORTAbits.RA0
#define m2out2 PORTAbits.RA7
#define m3out1 PORTAbits.RA6
#define m3out2 PORTBbits.RB7

void stepBip(unsigned char motor, unsigned char n_steps, unsigned char dir);