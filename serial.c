#include <Wire.h>
#include <I2C_LCD.h>

I2C_LCD LCD;
extern GUI_Bitmap_t bmlogo;       //Declare bitmap data package.
uint8_t I2C_LCD_ADDRESS = 0x51;  //Device address configuration, the default value is 0x51.

String instring;

void setup(void)
{
    Serial.begin(9600); // opens serial port, sets data rate to 9600 bps
    Wire.begin();         //I2C controller initialization.
    LCD.CleanAll(WHITE);    //Clean the screen with black or white.


    // bitmap dispaly mode.
    LCD.WorkingModeConf(ON, ON, WM_BitmapMode);

    // display logo
    LCD.DrawScreenAreaAt(&bmlogo, 0, 8);

    // character mode
    LCD.WorkingModeConf(ON, ON, WM_CharMode);

    // 8*16 font size, auto new line, black on white background
    LCD.FontModeConf(Font_6x8, FM_ANL_AAA, BLACK_BAC);
}

void loop(void)
{

    LCD.CharGotoXY(0,0);
    LCD.print("Hello World:");


    while(Serial.available()) {

        instring = Serial.readString();// read the incoming data as string

        Serial.println(instring);

            //Set the start coordinate.
            LCD.CharGotoXY(0,32);
            LCD.print(instring);

    }
}