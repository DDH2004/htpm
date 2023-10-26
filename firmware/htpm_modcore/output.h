#ifndef OUTPUT_H
#define OUTPUT_H

/* Print a 2-digit zero-padded hex value with the "0x" prefix. */
void p2hexln(byte value)
{
	Serial.print("0x");
	if (value < 0x10)  Serial.print("0");
	Serial.println(value, HEX);
}

#endif
