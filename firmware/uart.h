#include <stdint.h>
#include "config.h"

void UART_Init       (const long int Baudrate);
void UART_Tx_Char    (char data);
char UART_Tx_Empty   (void);
void UART_Tx_Text    (const char *Buffer);
char UART_Rx_Ready   (void);
char UART_Rx_Char    (void);
void UART_Rx_Text    (char *Buffer);