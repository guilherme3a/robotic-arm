#include <ctype.h>
#include <string.h>
#include "core.h"
#include "config.h"

#include "motorBip.h"
#include "uart.h"

void defineValues(char *Buffer, unsigned int *m, unsigned int *s, unsigned int *d)
{
    *m = convStr(&Buffer[0], 1);
    *s = convStr(&Buffer[1], 3);
    *d = convStr(&Buffer[4], 1);
}

unsigned int convStr(const char *vec, unsigned char len)
{
    unsigned int conv;
    unsigned char i;
    
    for(conv = 0, i = 0; len > 0 && isdigit(vec[i]); len--, i++)
        conv = conv * 10 + vec[i] - '0';
    
    return conv;
}

void autoHome()
{
    __delay_ms(100);
    
    //UART_Tx_Text("entrou no autoHome\n");
    while(fc1 == 0)
    {
        stepBip(1, 1, 0);
        
        //char tt[5];
        //sprintf(tt, "%u\n", fc1);
        //UART_Tx_Text(tt);
    }
    while(fc2 == 0)
    {
        stepBip(3, 1, 1);
    }
    while(fc3 == 0)
    {
        stepBip(2, 1, 0);
    }
    
    stepBip(1, 14, 1);
    __delay_ms(20);
    stepBip(3, 45, 0);
}