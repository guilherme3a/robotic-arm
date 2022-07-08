#include "config.h"

// mXoutY faz referencia a saida (out) Y do motor X

#define m4out1 PORTAbits.RA3
#define m4out2 PORTAbits.RA4
#define m4out3 PORTBbits.RB0
#define m4out4 PORTBbits.RB3

void stepUni(char dir);
void atualizaUni(unsigned char *stp, char dir);