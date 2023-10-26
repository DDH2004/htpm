/* HTP!m MODCORE Firmware
 * Firmware flashed onto the ATmega328 chips in HTP!m MODCOREs to actuate and
 * control up to 16 separate lines of power, receiving commands and sending
 * responses via I2C.
 */

#include <Wire.h>
#include "config.h"
#include "protocol.h"
#include "sr.h"

/* Communication state variables. */
uint16_t mid;
bool valid;

void receive()
{
	byte message[BUFFSIZE] = {0};

	/* Skip the register byte. */
	Wire.read();

	for (uint64_t i = 0; Wire.available() && i < BUFFSIZE; i++)
		message[i] = Wire.read();

	Serial.println("Received a message.");

	if (!validate(message, BUFFSIZE))
	{
		Serial.println("Invalid message.");
		valid = false;
		return;
	}

	mid = ((_b(message,4) & 0x0F) << 8) | _b(message,5);
	valid = true;
	Serial.println("<<<<<<<<");
	debug_print(message);
}

void reply()
{
	if (valid == false)
		return;

	Serial.println("Sending a reply.");
	send_ack(mid, ADDRESS, 0, VERSION);
}

void setup()
{
	Serial.begin(9600);

	Wire.begin(ADDRESS);
	Wire.onReceive(receive);
	Wire.onRequest(reply);

	sr_init();
	sr_write(0x0000);

	/* Initialize variables. */
	valid = 0;
}

void loop()
{
	delay(1000);
}
