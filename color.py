import math
# https://stackoverflow.com/questions/54663997/convert-rgb-color-to-xy
def rgbToXY(red, green, blue):
    redC =  (red / 255)
    greenC = (green / 255)
    blueC = (blue / 255)

    redN = (redC > 0.04045) if math.pow((redC + 0.055) / (1.0 + 0.055), 2.4) else (redC / 12.92)
    greenN = (greenC > 0.04045) if math.pow((greenC + 0.055) / (1.0 + 0.055), 2.4) else (greenC / 12.92)
    blueN = (blueC > 0.04045) if math.pow((blueC + 0.055) / (1.0 + 0.055), 2.4) else (blueC / 12.92)
    print(redN, greenN, blueN)

    x = redN * 0.664511 + greenN * 0.154324 + blueN * 0.162028

    y = redN * 0.283881 + greenN * 0.668433 + blueN * 0.047685

    z = redN * 0.000088 + greenN * 0.072310 + blueN * 0.986039
    print(x, y, z)

    x = x / (x + y + z)

    y = y / (x + y + z)

    #x = x * 65536 
    #y = y * 65536
    print(x, y)
    return x, y
