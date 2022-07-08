/*
 * Project:     Controle de braco robotico via serial
 * GitHub       https://github.com/guilherme3a/robotic-arm
 * MCU:         PIC16F648A
 * Compiller:   MPLAB XC8 Compiler v2.36
 * Author:      Guilherme Augusto
 * Date:        06/2022
 */

/* ========================= BIBLIOTECAS ========================== */

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

#include "config.h"
#include "core.h"
#include "uart.h"
#include "motorUni.h"
#include "motorBip.h"

/* ====================== VARIAVEIS GLOBAIS ====================== */

unsigned int motor, steps, direction;

/* ==================== FUNCAO CONFIG DO MCU ===================== */

void setup()
{
    CMCON = 0x07;                       // desabilita os comparadores internos
    TRISA = 0x20;                       // seta RA5 como entrada e o resto do porta como saida
    TRISB = 0x72;                       // seta RB1, RB4, RB5 e RB6 como entrada o resto do PORTB como saida
    PORTA = 0x00;                       // inicia os pinos do PORTA em nivel baixo
    PORTB = 0x00;                       // inicia os pinos do PORTB em nivel baixo
    
    UART_Init(4800);                    // config UART com baud rate de 4800 no modo assincrono
    __delay_ms(100);                    // delay para estabilizar a UART
}

/* ======================= FUNCAO PRINCIPAL ======================= */

void main(void)
{
    setup();
    
    UART_Tx_Text("start\n\r");
    
    char buff[10];       // char buff[5];
    
    autoHome();
    //stepUni(1);
    
    while(1)
    {
        if(UART_Rx_Ready())
        {            
            UART_Rx_Text(buff);
            defineValues(buff, &motor, &steps, &direction);
            
//            char msg[20];
//            sprintf(msg, "%u%u%u\n\r", motor, steps, direction);
//            UART_Tx_Text(msg);
            __delay_ms(500);
            //UART_Tx_Text(buff);
            
            if(motor == '4')        // if(motor == 4)
            {
                stepUni(direction);
            }else
            {
                stepBip(motor, steps, direction);
                UART_Tx_Text("ok");
            }
            
            memset(buff, 0, sizeof buff);       // limpa o buffer
        }
    }
}

/* ================================================================ */