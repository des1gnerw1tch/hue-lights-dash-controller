import asyncio
from bleak import BleakScanner
import HueBLE
from dash import Dash, dcc, html, callback, Output, Input
import dash_daq as daq

light = None
app = Dash()

async def connect_to_bulb():

    # Address of light to connect to
    # TODO: Hide this address in ENV variable, or do a discovery mode
    address = ""

    # Obtain the BLEDevice from bleak
    device = await BleakScanner.find_device_by_address(address, timeout=60.0)

    # Initialize the light object
    global light
    light = HueBLE.HueBleLight(device)

    # Will automatically connect to the light and turn it off
    await light.set_power(False)

    # Wait
    await asyncio.sleep(2)

    # Turn the light back on again
    await light.set_power(True)
    print(f"Successfully connected to lightbulb at {address}")



app.layout = html.Div([
    daq.BooleanSwitch(id='on-boolean-switch', on=False),
    html.Div(id='boolean-switch-result')
])

@callback(
    Output('boolean-switch-result', 'children'),
    Input('on-boolean-switch', 'on'),
    prevent_initial_call = True
)
async def update_output(onOrOff):
    await light.set_power(onOrOff)
    return f'The lightbulb is {onOrOff}.'


if __name__ == '__main__':
    asyncio.run(connect_to_bulb())
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=True
    )
