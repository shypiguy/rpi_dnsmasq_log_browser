# rpi_dnsmasq_log_browser
Browse dnsmasq log files with a Raspberry Pi and Adafruit LCD Shield kit

## Purpose

If you're running your own DNS cache on a Raspberry Pi using dnsmasq, this program allows you to browse the sites, clients and request times of DNS requests ordered by the total number of requests and filtered by any combination of site, client or 15 minute time period. This is useful for quickly understanding the traffic on your network, and can help pinpoint which client is making requests to which domains to identify spyware or malware running on your network clients.

## User experience

The [Adafruit Pi LCD Shield](https://www.adafruit.com/products/772) has 5 momentary switch buttons, four grouped to represent up, down, left, and right, and a fifth button that can act as a "select" button. The dns.py python program quickly reads dnsmasq log files on the Raspberry Pi and lights the LCD when the "select" button is pressed. The user can cycle through the "Address", "Time", and "Client" lists with the left and right buttons. Pressing the "down" button brings up the most requested address, 15 minute time period with the most requests, or the client making the most requests depending on which setting is selected. The left and right buttons now scroll through the ordered list of most requested addresses, 15 minute time periods with the most requests, or the clients making the most requests, again depending on the list originally selected. From this point, pressing down again allows the user to select either of the two "dimensions" not selected in the first step to see a further ordered list filtered by the first selection, and so on down to the third level with two filters selected.

In practice it works like this: If you wanted to see the time period with the most requests made to the second most requested address by the fourth busiest client, you would browse to that information by pressing:

*  Select (to load the data from the log files)
*  Right or Left (to identify "Client" as the first browsing level)
*  Down (to see the busiest client)
*  Right x3 (to see the fourth busiest client)
*  Down (to see the further dimensions you can explore)
*  Right or left (to identify "Address" as the next level to browse)
*  Down (to see the most requested address by the client)
*  Right (to see the second most requested address by the client)
*  Down (to see the 15 minute period of time with the most requests to that address by that client)
  


## Interfaces

### Hardware

The python program controls and responds to an [Adafruit Raspberry Pi LCD Shield](https://www.adafruit.com/products/772) connected to a Raspberry Pi via I2C.

### Software

The python program reads the active log file and the firtst uncompressed backup log file of the [dnsmasq](https://www.raspberrypi.org/forums/viewtopic.php?t=46154) DNS caching program. It uses the [Adafruit Python Char LCD Library](https://github.com/adafruit/Adafruit_Python_CharLCD) to control the LCD Shield.
