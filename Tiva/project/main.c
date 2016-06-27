#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include "driverlib/pin_map.h"
#include "tm4c123gh6pm.h"
#include "inc/hw_gpio.h"
#include "inc/hw_types.h"
#include "inc/hw_memmap.h"
#include "inc/hw_ints.h"
#include "driverlib/sysctl.h"
#include "driverlib/interrupt.h"
#include "driverlib/pin_map.h"
#include "driverlib/gpio.h"
#include "driverlib/timer.h"
#include "driverlib/pwm.h"
#include "driverlib/eeprom.h"
#include "UART.h"
#include "math.h"
#include <stdlib.h>

#define EEPROM_ADRESS 0x0000

uint8_t flag = 0;

//timer interrupt handler
void intHandler(void)
{
	// Clear the timer interrupt (ACK)
	TimerIntClear(TIMER5_BASE, TIMER_TIMA_TIMEOUT);
	if(flag)
	{
		GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_2,  0);
	}
	else
	{
		GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_2,  GPIO_PIN_2);
	}
	flag^=1;
}

struct MotorAngles
{
	uint32_t m1;
	uint32_t m2;
	uint32_t g;
	uint32_t m4;
	uint32_t m5;
	uint32_t m3;
} initialPos,currentPos;

void delayMS(int ms)
{
	SysCtlDelay( (SysCtlClockGet()/(3*1000))*ms ) ; // It delays 3 clock cycles in one period so SysCtlClockGet returns the current operating freq
													// which is here 16 MHz by deviding by 1000 we get ms and 3 for the three cycles.
}

int main(void)
{
	unsigned long ulPeriod;
	uint32_t returnCode;
	uint32_t period = 5000; //20ms (16Mhz / 64pwm_divider / 50) //for the pwm freq to be 50 Hz///5000

	//Set the clock to 16 MHz
	SysCtlClockSet(SYSCTL_SYSDIV_1 | SYSCTL_USE_OSC |   SYSCTL_OSC_MAIN | SYSCTL_XTAL_16MHZ);

	UART_Init();

	//Configure PWM Clock divide system clock by 64
	SysCtlPWMClockSet(SYSCTL_PWMDIV_64);

	//EEPROM SETTINGS
	SysCtlPeripheralEnable(SYSCTL_PERIPH_EEPROM0); // EEPROM activate

	do
	{
		returnCode=EEPROMInit(); // EEPROM start
	}
	while(returnCode!=EEPROM_INIT_OK);

	initialPos.m1 =   364;
	initialPos.m2 =   650;
	initialPos.g  =   200;
	initialPos.m4 =   165;
	initialPos.m5 =   348;
	initialPos.m3 =   546;

	//EEPROMProgram((uint32_t*) &initialPos, EEPROM_ADRESS, sizeof(currentPos));
	EEPROMRead((uint32_t*) &currentPos, EEPROM_ADRESS, sizeof(currentPos));

	// Enable the peripherals used by this program.
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOD); //PWM PINS (0,1)
	SysCtlDelay(3);
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOE); //PWM PINS (4)
	SysCtlDelay(3);
	SysCtlPeripheralEnable(SYSCTL_PERIPH_GPIOF); //PWM PINS (0,1,2,3)
	SysCtlDelay(3);

	GPIOPinTypeGPIOOutput(GPIO_PORTE_BASE, GPIO_PIN_2); // pin2 output

	GPIOPinWrite(GPIO_PORTE_BASE, GPIO_PIN_2,  GPIO_PIN_2);

	SysCtlPeripheralEnable(SYSCTL_PERIPH_PWM1);  //Enable pwm module 1


	HWREG(GPIO_PORTF_BASE + GPIO_O_LOCK) = GPIO_LOCK_KEY;
	HWREG(GPIO_PORTF_BASE + GPIO_O_CR)  |= 0x01;

	//TIMER5 Configuration

	//Configure PE4,PF0,PF1,PF2,PF3,PD0,PD1 Pins as PWM
	GPIOPinConfigure(GPIO_PD0_M1PWM0);
	GPIOPinConfigure(GPIO_PD1_M1PWM1);
	GPIOPinConfigure(GPIO_PE4_M1PWM2);
	GPIOPinConfigure(GPIO_PF0_M1PWM4);
	GPIOPinConfigure(GPIO_PF1_M1PWM5);
	GPIOPinConfigure(GPIO_PF2_M1PWM6);
	GPIOPinConfigure(GPIO_PF3_M1PWM7);


	GPIOPinTypePWM(GPIO_PORTD_BASE, GPIO_PIN_0 | GPIO_PIN_1);
	GPIOPinTypePWM(GPIO_PORTE_BASE, GPIO_PIN_4);
	GPIOPinTypePWM(GPIO_PORTF_BASE, GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3);


	SysCtlPeripheralEnable(SYSCTL_PERIPH_TIMER5); //enable TIMER5 clock
	SysCtlDelay(3);
	TimerConfigure(TIMER5_BASE, TIMER_CFG_PERIODIC); //configure TIMER5 to have A and B as counter
	ulPeriod = (SysCtlClockGet()/10); // every 1 sec
	TimerLoadSet(TIMER5_BASE, TIMER_A, ulPeriod -1); //set timer period to be 1 second
	TimerIntRegister(TIMER5_BASE, TIMER_A, intHandler);
	IntEnable(INT_TIMER5A); //enable TIMER5 interrupt in NVIC with the vector associated with TIMER5
	TimerIntEnable(TIMER5_BASE, TIMER_TIMA_TIMEOUT); //enable interrupt from the TIMER5 itself on timeout
	IntMasterEnable(); //enable global interrupts
	TimerEnable(TIMER5_BASE, TIMER_A);//enable TIMER5

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

	// Enable the PWM generator
	PWMGenEnable(PWM1_BASE, PWM_GEN_0);
	PWMGenEnable(PWM1_BASE, PWM_GEN_1);
	PWMGenEnable(PWM1_BASE, PWM_GEN_2);
	PWMGenEnable(PWM1_BASE, PWM_GEN_3);

	// Turn on the Output pins
	PWMOutputState(PWM1_BASE, PWM_OUT_0_BIT | PWM_OUT_1_BIT | PWM_OUT_4_BIT | PWM_OUT_5_BIT | PWM_OUT_6_BIT | PWM_OUT_7_BIT, true);

	//Array initialization with number of rows are the first 3 characters received from matlab, each row consists of 6 columns *angles* where each column consists of 3 characters
	uint32_t nrows, initialCount, b;
	char ch;

	uint32_t sum[140][6];
	//variable n is the rows counter, z is a counter *row number* in the loop to set the PWM
	uint32_t n,i,j,k,y,z;
	uint32_t oldSum[6];
	char x;

	/////////////////
	delayMS(6);
	oldSum[0] =   currentPos.m1;
	oldSum[1] =   currentPos.m2;
	oldSum[2] =   currentPos.g;
	oldSum[3] =   currentPos.m4;
	oldSum[4] =   currentPos.m5;
	oldSum[5] =   currentPos.m3;
	if(!((oldSum[0]!=364)||(oldSum[1]!=450)||(oldSum[2]!=300)||(oldSum[3]!=200)||(oldSum[4]!=400)||(oldSum[5]!=600)))
	{
		PWMPulseWidthSet(PWM1_BASE, PWM_OUT_0,  364);//////motor1 PD0
		PWMPulseWidthSet(PWM1_BASE, PWM_OUT_1,  450);//////motor2 PD1
		PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,  300);//////motor5 PF2 gripper
		PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5,  200);//////motor4 PF1
		PWMPulseWidthSet(PWM1_BASE, PWM_OUT_4,  300);//////gripper PF2 fel gdeda :D mn gher na2s 5000s
		PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,  600);///////motor3 PF3
	}

	while((oldSum[0]!=364)||(oldSum[1]!=450)||(oldSum[2]!=300)||(oldSum[3]!=200)||(oldSum[4]!=400)||(oldSum[5]!=600))
	{
		delayMS(4);
		if(364!=oldSum[0])
		{
			if(364 > oldSum[0])
				oldSum[0]+=1;
			else
				oldSum[0]-=1;
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_0,  oldSum[0]);
		}
		if(450!=oldSum[1])
		{
			if(450 > oldSum[1])
				oldSum[1]+=1;
			else
				oldSum[1]-=1;
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_1,  oldSum[1]);
		}
		if(300!=oldSum[2])
		{
			if(300 > oldSum[2])
				oldSum[2]+=1;
			else
				oldSum[2]-=1;
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,  oldSum[2]);
		}
		if(200!=oldSum[3])
		{
			if(200 > oldSum[3])
				oldSum[3]+=1;
			else
				oldSum[3]-=1;
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5,  oldSum[3]);
		}
		if(400!=oldSum[4])
		{
			if(400 > oldSum[4])
				oldSum[4]+=1;
			else
				oldSum[4]-=1;
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_4,  oldSum[4]);
		}
		if(600!=oldSum[5])
		{
			if(600 > oldSum[5])
				oldSum[5]+=1;
			else
				oldSum[5]-=1;
			PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,  oldSum[5]);
		}
	}

	currentPos.m1 =   oldSum[0];
	currentPos.m2 =   oldSum[1];
	currentPos.g =   oldSum[2];
	currentPos.m4 =   oldSum[3];
	currentPos.m5 =   oldSum[4];
	currentPos.m3 =   oldSum[5];
	EEPROMProgram((uint32_t*) &currentPos, EEPROM_ADRESS, sizeof(currentPos));
	///////////////

	while(1)
	{
		n=0;
		nrows=0;
		for(initialCount = 0 ; initialCount < 3 ; initialCount++)
		{
			ch = UART_InChar();
			b = (ch -'0') * pow(10,2-(initialCount));
			nrows+=b;
		}

		while(n!=nrows)
		{
			for(k = 0 ; k < 6 ; k++)
			{
				sum[n][k] = 0;
			}
			for(i = 0 ; i < 6 ; i++)
			{
				for(j = 0 ; j < 3 ; j++)
				{
					x = UART_InChar();
					y = (x -'0') * pow(10,2-(j));
					sum[n][i] += y;
				}
			}
			n++;
		}

		for (z=0; z<nrows; z++)
		{
			delayMS(6);
			oldSum[0] =   PWMPulseWidthGet(PWM1_BASE, PWM_OUT_0);
			oldSum[1] =   PWMPulseWidthGet(PWM1_BASE, PWM_OUT_1);
			oldSum[2] =   PWMPulseWidthGet(PWM1_BASE, PWM_OUT_6);
			oldSum[3] =   PWMPulseWidthGet(PWM1_BASE, PWM_OUT_5);
			oldSum[4] =   PWMPulseWidthGet(PWM1_BASE, PWM_OUT_4);
			oldSum[5] =   PWMPulseWidthGet(PWM1_BASE, PWM_OUT_7);

			while((oldSum[0]!=sum[z][0])||(oldSum[1]!=sum[z][1])||(oldSum[2]!=sum[z][2])||(oldSum[3]!=sum[z][3])||(oldSum[4]!=sum[z][4])||(oldSum[5]!=sum[z][5]))
			{
				delayMS(4);
				if(sum[z][0]!=oldSum[0])
				{
					if(sum[z][0] > oldSum[0])
						oldSum[0]+=1;
					else
						oldSum[0]-=1;
					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_0,  oldSum[0]);
				}
				if(sum[z][1]!=oldSum[1])
				{
					if(sum[z][1] > oldSum[1])
						oldSum[1]+=1;
					else
						oldSum[1]-=1;
					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_1,  oldSum[1]);
				}
				if(sum[z][2]!=oldSum[2])
				{
					if(sum[z][2] > oldSum[2])
						oldSum[2]+=1;
					else
						oldSum[2]-=1;
					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_6,  oldSum[2]);
				}
				if(sum[z][3]!=oldSum[3])
				{
					if(sum[z][3] > oldSum[3])
						oldSum[3]+=1;
					else
						oldSum[3]-=1;
					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_5,  oldSum[3]);
				}
				if(sum[z][4]!=oldSum[4])
				{
					if(sum[z][4] > oldSum[4])
						oldSum[4]+=1;
					else
						oldSum[4]-=1;
					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_4,  oldSum[4]);
				}
				if(sum[z][5]!=oldSum[5])
				{
					if(sum[z][5] > oldSum[5])
						oldSum[5]+=1;
					else
						oldSum[5]-=1;
					PWMPulseWidthSet(PWM1_BASE, PWM_OUT_7,  oldSum[5]);
				}
			}
			currentPos.m1 =   oldSum[0];
			currentPos.m2 =   oldSum[1];
			currentPos.g =   oldSum[2];
			currentPos.m4 =   oldSum[3];
			currentPos.m5 =   oldSum[4];
			currentPos.m3 =   oldSum[5];
			EEPROMProgram((uint32_t*) &currentPos, EEPROM_ADRESS, sizeof(currentPos));
		}
	}
}
