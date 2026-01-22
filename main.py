import asyncio
from bleak import BleakScanner
import HueBLE
from dash import Dash, dcc, html, callback, Output, Input, State
import dash_daq as daq
import os
from color import rgbToXY

# light = None
app = Dash()
address = os.getenv("HUE_BULB_MAC")

async def connect_to_bulb():
    # Address of light to connect to
    # TODO: Hide this address in ENV variable, or do a discovery mode

    # Obtain the BLEDevice from bleak
    device = await BleakScanner.find_device_by_address(address, timeout=60.0)

    # Initialize the light object
    global light
    light = HueBLE.HueBleLight(device)

    # Will automatically connect to the light and turn it off
    await light.set_power(False)

    await asyncio.sleep(2)

    # Turn the light back on again
    await light.set_power(True)
    print(f"Successfully connected to lightbulb at {address}")



app.layout = html.Div([
    daq.BooleanSwitch(id='on-boolean-switch', on=True, label="Toggle power"),
    html.Div(id='boolean-switch-result', style={"textAlign": "center"}),
    html.Br(),
    html.Br(),
    daq.ColorPicker(
        id='our-color-picker',
        label='Color Picker',
        value=dict(hex='#119DFF')
    ),
    html.Div(id='color-picker-result', style={"textAlign": "center"}),
    html.Div(
        html.Button('Submit', id='submit-color', n_clicks=0, style={"align": "center"}),
        style={"textAlign": "center"}
    ),
    html.Div(id='color-picker-light-result', style={"textAlign": "center"}),
    html.Br(),
    html.Br(),
    html.P("Temperature of light (no RGB)", style={"textAlign": "center"}),
    dcc.Slider(153, 500, 5,
               value=153,
               id='temp-slider'
    ),
    html.Div(id='temp-slider-output-container'),
    html.Br(),
    html.Br(),
    html.P("Brightness", style={"textAlign": "center"}),
    dcc.Slider(0, 255, 5,
               value=255,
               id='brightness-slider'
    ),
    html.Div(id='brightness-slider-output-container')
])

@callback(
    Output('boolean-switch-result', 'children'),
    Input('on-boolean-switch', 'on'),
    prevent_initial_call = True
)
async def update_lightbulb_power(onOrOff):
    device = await BleakScanner.find_device_by_address(address, timeout=5.0)
    light = HueBLE.HueBleLight(device)
    await light.set_power(onOrOff)
    return f'Is lightbulb on? {onOrOff}.'

@callback(
    Output('color-picker-result', 'children'),
    Input('our-color-picker', 'value')
)
def update_color_picker_output(value):
    return f'The selected color is {value}.'

@callback(
    Output('color-picker-light-result', 'children'),
    Input('submit-color', 'n_clicks'),
    State('our-color-picker', 'value'),
    prevent_initial_call=True
)
async def update_color_picker_output(n_clicks, value):
    red = value["rgb"]["r"]
    green = value["rgb"]["g"]
    blue = value["rgb"]["b"]
    print(f"{red}, {green}, {blue}")
    x, y = rgbToXY(red, green, blue)
    device = await BleakScanner.find_device_by_address(address, timeout=5.0)
    light = HueBLE.HueBleLight(device)
    await light.set_colour_xy(x, y)
    return 'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    )

@callback(
    Output('temp-slider-output-container', 'children'),
    Input('temp-slider', 'value'),
    prevent_initial_call=True)
async def update_temp(value):
    device = await BleakScanner.find_device_by_address(address, timeout=5.0)
    light = HueBLE.HueBleLight(device)
    await light.set_colour_temp(value)
    return 'You have selected "{}" mireds for warmth'.format(value)


@callback(
    Output('brightness-slider-output-container', 'children'),
    Input('brightness-slider', 'value'),
    prevent_initial_call=True)
async def update_brightness(value):
    device = await BleakScanner.find_device_by_address(address, timeout=5.0)
    light = HueBLE.HueBleLight(device)
    await light.set_brightness(value)
    return 'You have selected "{}" brightness'.format(value)


if __name__ == '__main__':
    # TODO: This way of connecting to bulb once and then using the module level variable in dash does not work.
    # Error is try to write to bulb but didn't work. Learn why this is the case, it would be good if we could
    # connect to the bulb once on startup instead of every operation
    # asyncio.run(connect_to_bulb())
    app.run(
        host="0.0.0.0",
        port=8050,
        debug=True
    )
