#include <ESP8266WiFi.h>

#define SSID "Family Wi-Fi"
#define PASS "butterfly!"

void setup()
{
	Serial.begin(9600);

	Serial.print("\nSetting up network \"");
	Serial.print(SSID);
	Serial.print("\" with password \"");
	Serial.print(PASS);
	Serial.println("\".");

	bool r = WiFi.softAP(SSID, PASS);

	if (r)
		Serial.println("Network successfully set up.");
	else
		Serial.println("Network setup failed.");
}

void loop()
{
	Serial.printf("Stations connected = %d\n", WiFi.softAPgetStationNum());
	delay(20000);
}
