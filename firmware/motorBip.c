#include <stdio.h>
#include <stdint.h>
#include "motorBip.h"
#include "config.h"
#include "uart.h"

void stepBip(unsigned char motor, unsigned char n_steps, unsigned char dir)
{
    //__delay_ms(15);
    //UART_Tx_Text("stepBip\n");
    static const unsigned char stepsA[] = {0x01, 0x01, 0x00, 0x01, 0x00, 0x00, 0x01, 0x00};
    static const unsigned char stepsH[] = {0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x01, 0x01};
    
    char aux, total = 0;
    static unsigned char lastB = 0;
    
    //char teste[50];

    for (aux = lastB; total < n_steps; aux += 2, total++)
    {
        __delay_ms(15);
        if (dir == 0)
        {
            if (motor == 1)
            {
                m1out1 = stepsA[aux];
                m1out2 = stepsA[aux + 1];
                //sprintf(teste,"RA2: %u | RA1: %u \n", m1out1, m1out2);
                //UART_Tx_Text(teste);
            }
            else if (motor == 2)
            {
                m2out1 = stepsA[aux];
                m2out2 = stepsA[aux + 1];
                //sprintf(teste,"RA0: %u | RA7: %u \n", m2out1, m2out2);
                //UART_Tx_Text(teste);
            }
            else if (motor == 3)
            {
                m3out1 = stepsA[aux];
                m3out2 = stepsA[aux + 1];
                //sprintf(teste,"RA6: %u | RB7: %u \n", m3out1, m3out2);
                //UART_Tx_Text(teste);
            }
        }
        else if (dir == 1)
        {
            if (motor == 1)
            {
                m1out1 = stepsH[aux];
                m1out2 = stepsH[aux + 1];
                //sprintf(teste,"RA2: %u | RA1: %u \n", m1out1, m1out2);
                //UART_Tx_Text(teste);
            }
            if (motor == 2)
            {
                m2out1 = stepsH[aux];
                m2out2 = stepsH[aux + 1];
                //sprintf(teste,"RA0: %u | RA7: %u \n", m2out1, m2out2);
                //UART_Tx_Text(teste);
            }
            else if (motor == 3)
            {
                m3out1 = stepsH[aux];
                m3out2 = stepsH[aux + 1];
                //sprintf(teste,"RA6: %u | RB7: %u \n", m3out1, m3out2);
                //UART_Tx_Text(teste);
            }
        }

        if (aux == 6) {
            lastB = 0;
            aux = -2;
        }

        // periodo entre os passos
        __delay_us(1000);
    }

    // armazena o indice do ultimo passo na variavel lastB
    lastB = aux;
}