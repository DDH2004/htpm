/* HTP!m MODCORE Firmware
 * Firmware flashed onto the ATmega328 chips in HTP!m MODCOREs to actuate and
 * control up to 16 separate lines of power, receiving commands and sending
 * responses via I2C.
 */

#include <Wire.h>
#include "config.h"
#include "sr.h"

void receive()
{
	uint16_t buffer = 0;
	byte message[16] = {0};

	/* Skip the register byte. */
	Wire.read();

	for (uint64_t i = 0; Wire.available() && i < 16; i++)
		message[i] = Wire.read();

	buffer = message[0] << 8 | message[1];

	Serial.println("Received a message.");
	Serial.println(buffer, BIN);

	sr_write(buffer);
}

void setup()
{
	Serial.begin(9600);

	Wire.begin(ADDRESS);
	Wire.onReceive(receive);

	sr_init();
	sr_write(0x0000);
}

void loop()
{
	delay(1000);
}
