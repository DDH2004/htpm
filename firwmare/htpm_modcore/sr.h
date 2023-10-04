void sr_write(uint8_t ser, uint8_t rclk, uint8_t srclk, uint16_t val)
{
	digitalWrite(rclk, LOW);

	for (uint8_t i = 0; i < 16; i++)
	{
		digitalWrite(ser, (val >> i) & 1);
		digitalWrite(srclk, HIGH);
		digitalWrite(srclk, LOW);
	}

	digitalWrite(rclk, HIGH);
}
