#include "config.h"

// fcZ faz referencia a entrada destinada a chave fim de curso Z

#define fc1 PORTBbits.RB5
#define fc2 PORTBbits.RB4
#define fc3 PORTBbits.RB6

void defineValues(char *Buffer, unsigned int *m, unsigned int *s, unsigned int *d);
unsigned int convStr(const char *vec, unsigned char len);
void autoHome();