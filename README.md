# Hue lights dash controller
Control Phillips Hue lights hosted on a Linux machine. Does not require a Hue Bridge. Perfect for raspberry pi or other small SBCs. 

1. Make sure bluetooth is up on linux machine and BlueZ is installed
2. Make sure uv is installed https://docs.astral.sh/uv/
3. Run `uv sync`
4. Find MAC address of bulb using `uv run scan.py`
5. Make sure Phillips Hue lightbulb is in pairing mode
6. Then go through bluetoothctl to pair your linux server to the bulb
```
$ bluetoothctl
scan on
pair AA:BB:CC:DD:EE:FF   # Replace with your bulb's MAC
trust AA:BB:CC:DD:EE:FF
```
7. `uv run main.py`
8. Open dash frontend, and now can use features (turn on and off bulb, brightness, warmth, color, etc.)
