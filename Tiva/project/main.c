#include "driverlib/pin_map.h"
#include <stdint.h>
#include <stdbool.h>
#include "inc/hw_gpio.h"
#include "inc/hw_types.h"
#include "inc/hw_memmap.h"
#include "driverlib/sysctl.h"
#include "driverlib/pin_map.h"
#include "driverlib/gpio.h"
#include "driverlib/pwm.h"
#include "UART.h"
#include <stdio.h>
#include "math.h"
#include "tm4c123gh6pm.h"


void delayMS(int ms)
{
	SysCtlDelay( (SysCtlClockGet()/(3*1000))*ms ) ; // It delays 3 clock cycles in one period so SysCtlClockGet returns the current operating freq
													// which is here 16 MHz by deviding by 1000 we get ms and 3 for the three cycles.
}

int main(void)
{
	uint32_t period = 5000; //20ms (16Mhz / 64pwm_divider / 50) //for the pwm freq to be 50 Hz///5000
	uint32_t duty = 300;

	//Set the clock to 16 MHz
	SysCtlClockSet(SYSCTL_SYSDIV_1 | SYSCTL_USE_OSC |   SYSCTL_OSC_MAIN | SYSCTL_XTAL_16MHZ);

	//Configure PWM Clock divide system clock by 64
	SysCtlPWMClockSet(SYSCTL_PWMDIV_64);

	// Enable the peripherals used by this program.
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOD); //PWM PINS (0,1)
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE); //PWM PINS (4)
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF); //PWM PINS (1,2,3)
	SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM1);  //Enable pwm module 1

	//Configure PE4,PF1,PF2,PF3,PD0,PD1 Pins as PWM
	GPIOPinConfigure(GPIO_PD0_M1PWM0);
	GPIOPinConfigure(GPIO_PD1_M1PWM1);
	GPIOPinConfigure(GPIO_PE4_M1PWM2);
	GPIOPinConfigure(GPIO_PF1_M1PWM5);
	GPIOPinConfigure(GPIO_PF2_M1PWM6);
	GPIOPinConfigure(GPIO_PF3_M1PWM7);
	GPIOPinTypePWM(GPIO_PORTD_BASE, GPIO_PIN_0 | GPIO_PIN_1);
	GPIOPinTypePWM(GPIO_PORTE_BASE, GPIO_PIN_4);
	GPIOPinTypePWM(GPIO_PORTF_BASE, GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3);

	//Configure PWM Options
	//PWM_GEN_0 Covers M1PWM0 and M1PWM1
	//PWM_GEN_1 Covers M1PWM2 and M1PWM3
	//PWM_GEN_2 Covers M1PWM4 and M1PWM5
	//PWM_GEN_3 Covers M1PWM6 and M1PWM7
	PWMGenConfigure(PWM1_BASE, PWM_GEN_0, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
	PWMGenConfigure(PWM1_BASE, PWM_GEN_1, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
	PWMGenConfigure(PWM1_BASE, PWM_GEN_2, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);
	PWMGenConfigure(PWM1_BASE, PWM_GEN_3, PWM_GEN_MODE_DOWN | PWM_GEN_MODE_NO_SYNC);

	//Set the Period (expressed in clock ticks)
	PWMGenPeriodSet(PWM1_BASE, PWM_GEN_0, period-1);
	PWMGenPeriodSet(PWM1_BASE, PWM_GEN_1, period-1);
	PWMGenPeriodSet(PWM1_BASE, PWM_GEN_2, period-1);
	PWMGenPeriodSet(PWM1_BASE, PWM_GEN_3, period-1);

	//Set PWM duty
	PWMPulseWidthSet(PWM1_BASE, PWM_OUT_0,5000 - 364);
	PWMPulseWidthSet(PWM1_BASE, PWM_OUT_1,5000 - 130);
	PWMPulseWidthSet(PWM1_BASE, PWM_OUT_2,5000 - 400);
	PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5,5000 - 386);
	PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,5000 - 590);
	PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,5000 - 300);

	/*PWMPulseWidthSet(PWM1_BASE, PWM_OUT_0,364);
		PWMPulseWidthSet(PWM1_BASE, PWM_OUT_1,130);
		PWMPulseWidthSet(PWM1_BASE, PWM_OUT_2,400);
		PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5,386);
		PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,590);
		PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,300);*/

	// Enable the PWM generator
	PWMGenEnable(PWM1_BASE, PWM_GEN_0);
	PWMGenEnable(PWM1_BASE, PWM_GEN_1);
	PWMGenEnable(PWM1_BASE, PWM_GEN_2);
	PWMGenEnable(PWM1_BASE, PWM_GEN_3);

	// Turn on the Output pins
	PWMOutputState(PWM1_BASE, PWM_OUT_0_BIT | PWM_OUT_1_BIT | PWM_OUT_2_BIT | PWM_OUT_5_BIT | PWM_OUT_6_BIT | PWM_OUT_7_BIT, true);

	UART_Init();    // call the subroutine defined in "uart.h"
	// to initialize UART for printingwhile(1)

	char x[3];
	uint32_t y[] = {0,0,0};
	uint32_t sum = 0;
	int i;
	unsigned char motorNo;

	int v;
	while(1)
	{
		sum = 0 ;
		for(i=0; i<4; i++)
		{
			if( i == 0 )
			{
				motorNo = UART_InChar();
			}
			else
			{
				x[i-1] = UART_InChar();
				y[i-1] = (x[i-1]-'0') * pow(10,2-(i-1));
				sum += y[i-1];
			}
		}

		switch(motorNo)
		{
			case '1':
				PWMPulseWidthSet(PWM1_BASE, PWM_OUT_0,5000 - sum);
				break;
			case '2':
				PWMPulseWidthSet(PWM1_BASE, PWM_OUT_1,5000 - sum);
				break;
			case '3':
				PWMPulseWidthSet(PWM1_BASE, PWM_OUT_2,5000 - sum);
				break;
			case '4':
				PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5,5000 - sum);
				break;
			case '5':
				PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,5000 - sum);
				break;
			case '6':
				PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,5000 - sum);
				break;
			default:;
		}

		/*PWMPulseWidthSet(PWM1_BASE, PWM_OUT_0,200);
		PWMPulseWidthSet(PWM1_BASE, PWM_OUT_1,200);
		PWMPulseWidthSet(PWM1_BASE, PWM_OUT_2,200);
					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5,200);
					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,200);
					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,200);

delayMS(4000);

					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_0,300);
					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_1,300);
					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_2,300);
					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5,300);
					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,300);
					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,300);
					delayMS(4000);*/
/*
					for( v = 200 ; v < 351 ; v+=2 )
		{
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_0,v);
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_1,v);
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_2,v);
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5,v);
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,v);
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,v);
			delayMS(20);
		}
		for( v = 350 ; v > 199 ; v-=2 )
		{
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_0,v);
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_1,v);
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_2,v);
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5,v);
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,v);
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,v);
			delayMS(20);
		}*/
	}
}
