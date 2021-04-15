
print("main.py: Hello")

import time
from boot import do_connect, scan_wlan
import utils.screen_utils as screen
from mqtt_connection import start_mqqt_connection
import ntptime
from erika import Erika
import uasyncio as asyncio
import gc
import network


# scan_wlan()
# set time
try:
    ntptime.NTP_DELTA = ntptime.NTP_DELTA - (2 * 3600) # Delta of -2 = UTC +2 = CEST
    ntptime.settime()
except:
    print("Could not set time.")

erika = Erika()
time.sleep(1)
screen.starting()

async def wlan_strength(max=5):
    while True:
        # we use this for Garbage Collection too.
        gc.collect()
        ##
        ip = do_connect()
        wlan = network.WLAN()
        strength = wlan.status('rssi')
        screen.network(ip,strength)
        await asyncio.sleep(max)

async def main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
       erika.receiver(),
       erika.printer(erika.queue),
       wlan_strength(5),
       start_mqqt_connection(erika)
    )

asyncio.run(main())