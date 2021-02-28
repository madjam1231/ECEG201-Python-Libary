"""CircuitPython Essentials Internal RGB LED rainbow example"""
import time
import board

import neopixel
ring = neopixel.NeoPixel(board.D5,24, brightness=0.3)

ring.brightness = .1
#Ring color (color, flash rate) -
#command all 24 LEDs of the ring to illuminate a particular color with
#an optional flash rate to turn the ring off/on at a desired rate

def ring_color(color, flash_rate, num_leds = 24, ring = ring):
    ring.fill(color)


#Bar graph (color, position, dot/fill)
#treat the ring like a bar graph.
#Think of a speedometer on a car.
#Input the color for the LEDs to illuminate,
#how far to illuminate, and whether it operates in dot mode
#(only a single LED illuminates) or in fill mode (all LEDs up to the stop level illuminate).
#A nice optional feature would be to have the last LED or the last n LEDs taper off in brightness.

def bar_graph(color, end_pos, fill_mode, start_pos = 0, num_leds = 24, ring = ring):


    if(end_pos > num_leds):
        print("ERROR: Your end position can't be more than the number of LEDS")
        return
    if(start_pos < 0):
        print("ERROR: Your start position can't be less than 0")
        return


    ring.fill((0,0,0))

    if fill_mode == True:
        for i in range(start_pos, end_pos):
            ring[i] = color
    else:
        ring[pos] = color


#Shaded bar graph (start color, stop color, position, dot/fill, dot color) -
#same as bar graph except the color transitions from a start to finish color)

def shaded_bar_graph(start_color, end_color, end_pos, start_pos = 0, num_leds = 24, ring = ring):

    if(end_pos > num_leds):
        print("ERROR: Your end position can't be more than the number of LEDS")
        return
    if(start_pos < 0):
        print("ERROR: Your start position can't be less than 0")
        return
    ring.fill((0,0,0))
    transition_length = (end_pos-start_pos)
    slope = [
        (end_color[0] - start_color[0]) / transition_length,
        (end_color[1] - start_color[1]) / transition_length,
        (end_color[2] - start_color[2]) / transition_length
    ]

    y_offset = [
        start_color[0],
        start_color[1],
        start_color[2]
    ]

    for i in range(0,transition_length):

        calculated_color = (
            slope[0]*i + y_offset[0],
            slope[1]*i + y_offset[1],
            slope[2]*i + y_offset[2]
        )
        ring[start_pos + i] = calculated_color


#Dot on background (color, position, dot color) -
#ring is one color but a single dot is a different color; input ring color, dot position, dot color.
def dot_on_background(fill_color, dot_pos, dot_color, ring = ring):
    ring.fill(fill_color)
    ring[dot_pos] = dot_color

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

#barGraph((0,0,255), 12, True)
#time.sleep(.2)
#for i in range(10):
shaded_bar_graph((255,0,0),(0,0,255),24,5)

time.sleep(2)
shaded_bar_graph((0,255,0),(0,0,255),24)

dot_on_background((255,0,0),-43,(0,0,255))

#ring[15] = (15,0,0)
'''
while True:

    for j in range(255):
        for i in range(24):
            color = wheel(j)
            color = (i*(color[0]/24),i*(color[1]/24),i*(color[2]/24))
            #print(color)
            ring[i] = color
            #ringColor(color,0)
            #led[i] = wheel(j)
            #time.sleep(.003)
'''