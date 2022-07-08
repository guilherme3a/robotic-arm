#include "motorUni.h"

unsigned char stepsU[] = {0x01, 0x01, 0x00, 0x00};

// envia os passos ao motor de passo unipolar
void stepUni(char dir)
{
    int cont;
    // aprox 4075 passos para um volta completa
    for(cont=0; cont<=400; cont++)
    {
        m4out1 = stepsU[0];
        m4out2 = stepsU[1];
        m4out3 = stepsU[2];
        m4out4 = stepsU[3];

      atualizaUni(stepsU, dir);

      __delay_ms(10);
    }
}

// atualiza o numero de passos de acordo com a direcao
void atualizaUni(unsigned char *stp, char dir)
{
    if(dir == 0)
    {
        unsigned char aux = stp[3];

        stp[3] = stp[2];
        stp[2] = stp[1];
        stp[1] = stp[0];
        stp[0] = aux;
    }
    else if(dir == 1)
    {
        unsigned char aux = stp[0];

        stp[0] = stp[1];
        stp[1] = stp[2];
        stp[2] = stp[3];
        stp[3] = aux;
    }
}