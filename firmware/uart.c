#include <stdint.h>
#include "config.h"
#include "uart.h"

void UART_Init(const long int Baudrate)
{
    unsigned int Xbaud;
    Xbaud = (_XTAL_FREQ - Baudrate*64)/(Baudrate*64);

    if(Xbaud > 255)
    {
        Xbaud = (_XTAL_FREQ - Baudrate*16)/(Baudrate*16);
        TXSTAbits.BRGH = 1;         // baud rate de alta velocidade
    }else
    {
        TXSTAbits.BRGH = 0;         // baud rate de baixa velocidade
        SPBRG = Xbaud;              // config registrador baud rate
        TXSTAbits.SYNC = 0;         // habilita modo assincrono
        TXSTAbits.TXEN = 1;         // habilita transmissão
        RCSTAbits.CREN = 1;         // habilita recepção
        RCSTAbits.SPEN = 1;         // habilita porta serial
        
        TRISBbits.TRISB1 = 0x01;    // seta o pino de RX como entrada
        TRISBbits.TRISB2 = 0x00;    // seta o pino de TX como saída
    }  
}

// enviar um unico caracter
void UART_Tx_Char(char data)
{
    while(!TRMT);                   // TRMT = 0 enquanto há envio de dados em curso
    TXREG = data;                   // TXREG é o buffer de envio de dados da UART
}

// verifica se o buffer de dados esta vazio
char UART_Tx_Empty(void)
{
    return TRMT;
}

// envia um array de caracteres
void UART_Tx_Text(const char *Buffer)
{
    int i;
    
    for(i = 0; Buffer[i] != '\0'; i++)
        UART_Tx_Char(Buffer[i]);
}

// verifica se o buffer de recepcao esta cheio
char UART_Rx_Ready(void)
{
    return RCIF;                    // RCIF = 1 quando o buffer estiver cheio
}

// descarrega os dados do buffer de recepcao
char UART_Rx_Char(void)
{
    while(!RCIF);
    return RCREG;                   // RCREG é o buffer de recepção da UART
}

// descarrega os dados em um vetor de caracteres
void UART_Rx_Text(char *Buffer)
{
    char ch;
    unsigned char len = 0;
    
    while(1)
    {
        ch = UART_Rx_Char();
        //UART_Tx_Char(ch);

        if (ch == '\r' || ch == '\n' || ch == '\0')
        {
            Buffer[len] = 0;
            break;
        }
        else if ((ch == '\b') && (len != 0))
        {
            len--;
        }
        else
        {
            Buffer[len] = ch;
            len++;
        }
    }
}