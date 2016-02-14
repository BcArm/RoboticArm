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

	char x;
	uint32_t y;
	uint32_t sum[6]={0,0,0,0,0,0};
	uint32_t oldSum[6]={0,0,0,0,0,0};
	uint32_t i,j,k,l;
	while(1)
	{
		for(k = 0 ; k < 6 ; k++)
		{
			sum[k] = 0;
		}

		for(i = 0 ; i < 6 ; i++)
		{
			for(j = 0 ; j < 3 ; j++)
			{
				x = UART_InChar();
				y = (x -'0') * pow(10,2-(j));
				sum[i] += y;
			}
		}

		oldSum[0] = 5000 - PWMPulseWidthGet(PWM1_BASE, PWM_OUT_0);
		oldSum[1] = 5000 - PWMPulseWidthGet(PWM1_BASE, PWM_OUT_1);
		oldSum[2] = 5000 - PWMPulseWidthGet(PWM1_BASE, PWM_OUT_2);
		oldSum[3] = 5000 - PWMPulseWidthGet(PWM1_BASE, PWM_OUT_5);
		oldSum[4] = 5000 - PWMPulseWidthGet(PWM1_BASE, PWM_OUT_6);
		oldSum[5] = 5000 - PWMPulseWidthGet(PWM1_BASE, PWM_OUT_7);

		while((sum[0]!=oldSum[0])||(sum[1]!=oldSum[1])||(sum[2]!=oldSum[2])||(sum[3]!=oldSum[3])||(sum[4]!=oldSum[4])||(sum[5]!=oldSum[5]))
		{
			//delayMS(100);
			if(sum[0]!=oldSum[0])
			{
				if(sum[0] > oldSum[0])
					oldSum[0]+=1;
				else
					oldSum[0]-=1;
				PWMPulseWidthSet(PWM1_BASE, PWM_OUT_0,5000 - oldSum[0]);
			}
			if(sum[1]!=oldSum[1])
			{
				if(sum[1] > oldSum[1])
					oldSum[1]+=1;
				else
					oldSum[1]-=1;
				PWMPulseWidthSet(PWM1_BASE, PWM_OUT_1,5000 - oldSum[1]);
			}
			if(sum[2]!=oldSum[2])
			{
				if(sum[2] > oldSum[2])
					oldSum[2]+=1;
				else
					oldSum[2]-=1;
				PWMPulseWidthSet(PWM1_BASE, PWM_OUT_2,5000 - oldSum[2]);
			}
			if(sum[3]!=oldSum[3])
			{
				if(sum[3] > oldSum[3])
					oldSum[3]+=1;
				else
					oldSum[3]-=1;
				PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5,5000 - oldSum[3]);
			}
			if(sum[4]!=oldSum[4])
			{
				if(sum[4] > oldSum[4])
					oldSum[4]+=1;
				else
					oldSum[4]-=1;
				PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,5000 - oldSum[4]);
			}
			if(sum[5]!=oldSum[5])
			{
				if(sum[5] > oldSum[5])
					oldSum[5]+=1;
				else
					oldSum[5]-=1;
				PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,5000 - oldSum[5]);
			}
		}
	}
}
