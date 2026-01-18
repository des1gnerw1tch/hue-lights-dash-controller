import asyncio
from bleak import BleakScanner
import HueBLE


async def main():

    # Address of light to connect to
    # TODO: This is the UUID because mac doesn't show MAC addresses, but when we switch to Ubuntu container we should use MAC address.
    address = ""

    # Obtain the BLEDevice from bleak
    device = await BleakScanner.find_device_by_address(address, timeout=60.0)

    # Initialize the light object
    light = HueBLE.HueBleLight(device)

    # Optionally we could call connect but it will be called automatically
    # on the first request to the light. You might want to call this if
    # you want to subscribe to state changes without changing the lights state.
    # await light.connect()

    while(True):
        # Will automatically connect to the light and turn it off
        await light.set_brightness(255)

        # Wait
        await asyncio.sleep(1)

        # Turn the light back on again
        await light.set_brightness(0)
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
