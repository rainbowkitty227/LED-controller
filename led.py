from rpi_ws281x import *
from threading import Thread
import time
import random

"""idk what all these do, I just copy-pasted this whole block. you probably want to change some of these (specifically 'LED_COUNT')"""
# LED strip configuration:
LED_COUNT      = 600     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


go = True # set go to False to stop execution of an animation function

def setup():
    global LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    return strip

def setpixel(strip,pos,color):
    strip.setPixelColor(pos,color)

def wipe(strip, color, delay, speed=5, dir=1):
    global go
    for i in range(0,strip.numPixels(),speed)[::dir]:
        for ii in range(speed):
            if not go: return 0
            setpixel(strip,i+ii,color)
        strip.show()
        time.sleep(delay)

def color_swipe(strip,color,swipe_size=10,speed=1, dir=1):
    global go
    for i in range(swipe_size)[::dir]:
        if not go: return 0
        for pix in range(strip.numPixels()):
            if pix%swipe_size == i:
                setpixel(strip,pix,color)
        strip.show()

def color_spread(strip,color,spread_size=10,speed=1):
    global go
    for i in range(1 + spread_size//2):
        if not go: return 0
        for pix in range(strip.numPixels()):
            if pix%spread_size == i or pix%spread_size == (spread_size-i):
                setpixel(strip,pix,color)
        strip.show()

def colorAll(strip,color):
    for i in range(strip.numPixels()):
        setpixel(strip,i,color)
    strip.show()

def clear(strip,show=True):
    for i in range(strip.numPixels()):
        setpixel(strip,i,Color(0,0,0))
    if show:
        strip.show()

def rainbowWheel(pos, returnColor=True):
    if pos <= 255:
        clr = (255-pos, pos, 0)
    elif pos > 255 and pos <= 510:
        clr =(0,255 - (pos-255), pos-255)
    elif pos > 510 and pos <= 765:
        clr =(pos-510,0,255 - (pos-510))

    if returnColor:
        return Color(clr[0],clr[1],clr[2])
    else:
        return clr

def rainbowColor(strip, iterations):
    global go
    i=0
    while (i < iterations or iterations==0) and go:
        for pos in range(765):
            if not go: return 0
            colorAll(strip, rainbowWheel(pos))
        i+=1

def perPixelRainbowColor(strip, iterations):
    global go
    pixelList = [i for i in range(strip.numPixels())]
    i=0
    while (i < iterations or iterations==0) and go:
        for pos in range(765):
            if not go: return 0
            for pixel in range(len(pixelList)):
                pixelPos = (pos + pixelList[pixel]) % 765
                color=rainbowWheel(pixelPos)
                setpixel(strip,pixel,color)
            strip.show()
        i+=1

def randomized(strip,iterations,RGBonly=False):
    global go
    i=0
    while i < iterations or iterations == 0:
        if not go: return 0
        for pixel in range(strip.numPixels()):
            if RGBonly:
                color = [Color(255,0,0),Color(0,255,0),Color(0,0,255)][random.randint(0,2)]
            else:
                color = Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            setpixel(strip,pixel,color)
        strip.show()
        i+=1

def bounce(strip, colors, tailLen, delay, iterations, background_colors=[Color(0,0,0)],speed=5):
    global go
    i = 0
    dir = 1
    delay = delay/1000.0
    hit_edge = False
    while i < iterations or iterations == 0:
        for head in range(0,strip.numPixels(),speed)[::dir]:
            if not go: return 0
            for pixel in range(strip.numPixels()):
                if head - pixel <= tailLen and head-pixel >= 0-tailLen:
                    setpixel(strip,pixel,colors[i%len(colors)])
                    if pixel < 0:
                        hit_edge = True
                else:
                    setpixel(strip,pixel,background_colors[i%len(background_colors)])
            strip.show()
            if hit_edge:
                hit_edge = False
                continue
            time.sleep(delay)

        i += 1
        dir = [1,-1][i%2]

def bounce_2(strip, colors, tailLen, delay, iterations, background_colors=[Color(0,0,0)], speed=1):
    global go
    i = 0
    dir = 1
    delay = delay/1000.0
    hit_edge = False
    max=strip.numPixels()
    while (i < iterations or iterations == 0) and go:
        for mid in range(0,max,speed)[::dir]:
            for pix in range(mid-(tailLen//2)-(1-dir*speed), mid+(tailLen//2)+(1-dir*speed),speed):
                for ii in range(speed):
                    if 0 < pix+(dir*ii) < max:
                        setpixel(strip,(pix+(dir*ii)),colors[i%len(colors)])
            setpixel(strip,mid+(dir*(tailLen//2)),background_colors[i%len(background_colors)])
            strip.show()
        dir *= -1
        i+=1

def alert(strip, iterations):
    global go
    i=0
    while (i<iterations or iterations == 0) and go:
        for _ in range(iterations):
            if not go: return 0
            colorAll(strip,Color(255,0,0))
            time.sleep(0.5)
            clear(strip)
            time.sleep(0.25)
        i+=1

def theatre_lights(strip, colors, delay, iterations, dir=1, background_color = Color(0,0,0)):
    global go
    i=1
    while (i<iterations or iterations==0) and go:
        for ii in range(3)[::dir]:
            if not go: return 0
            for pixel in range(strip.numPixels()):
                if pixel % 3 == ii:
                    setpixel(strip,pixel,colors[(pixel-(ii+3*i))%len(colors)])
                else:
                    setpixel(strip,pixel,background_color)
            strip.show()
            time.sleep(delay)
        i+=1

def multi_color_wipe(strip,colors,delay,iterations):
    global go
    i=1
    while (i < iterations or iterations == 0) and go:
        wipe(strip,colors[i%len(colors)],delay,dir=[1,-1][i%2])
        i+=1

def multi_color_swipe(strip,colors,delay,iterations):
    global go
    i=1
    while (i < iterations or iterations == 0) and go:
        color_swipe(strip,colors[i%len(colors)],25)
        i+=1


def no(strip,iterations,delay):
    global go
    colors=[Color(255,0,0),Color(0,255,0),Color(0,0,255)]
    i=0
    while (i<iterations or iterations==0) and go:
        for x in range(3):
            colorAll(strip,colors[x])
            time.sleep(delay)
        i+=1


def run(strip,colors,speed,length,dist=5,dir=1,delay=0,background_color=Color(0,0,0), mirrored=1, iterations=0):
    global go
    i=0
    base = []
    for color in colors:
        for i in range(length):
            base.append(color)
        for i in range(dist):
            base.append(background_color)
    if mirrored:
        total_len = strip.numPixels()//2
    else:
        total_len = strip.numPixels()

    while (i<iterations or iterations == 0) and go:
        for offset in range(0, len(base), speed)[::dir]:
            for pos in range(total_len):
                pixel_to_set = pos
                setpixel(strip, pixel_to_set, base[(pos + offset) % len(base)])
                if mirrored:
                    setpixel(strip, strip.numPixels() - pixel_to_set - 1, base[(pos + offset) % len(base)])
            strip.show()
            if not go: return 0
            if delay: time.sleep(delay)
        i += 1

def demo(strip):
    global go

    wipe(strip,Color(255,0,0),0.1)
    if not go: return 0
    wipe(strip,Color(0,255,0),0.1, dir=-1)
    if not go: return 0
    wipe(strip,Color(0,0,255),0.1)

    if not go: return 0

    bounce(strip, [Color(0,0,0)], 10, 0, 2, background_colors=[Color(0,0,255)])

    if not go: return 0

    wipe(strip, Color(0,0,0),0.1)

    if not go: return 0
    time.sleep(0.25);clear(strip);time.sleep(0.25)
    if not go: return 0

    rainbowColor(strip,iterations=1)

    if not go: return 0
    time.sleep(0.25);clear(strip);time.sleep(0.25)
    if not go: return 0

    perPixelRainbowColor(strip,1)

    if not go: return 0
    time.sleep(0.25);clear(strip);time.sleep(0.25)
    if not go: return 0

    bounce(strip,[Color(255,0,0),Color(0,255,0),Color(0,0,255)],10,0,2)

    if not go: return 0
    time.sleep(0.25);clear(strip);time.sleep(0.25)
    if not go: return 0

    randomized(strip,100)

    if not go: return 0
    time.sleep(0.25);clear(strip);time.sleep(0.25)


"""
pre made animations for webserver
('_a' means its a pre-set animation, so as to not interfere with other functions)
"""

def wipe_a(strip,rgb,iterations=0):
    wipe(strip, Color(rgb[0],rgb[1],rgb[2]), 0, 1)

def color_wave_t_a(strip,rgb,iterations = 0):
    color_wave(strip, ((0,161,232),(255,161,232),(255,255,255),(255,161,232),(0,161,232)), 0.2, iterations, 1)

def flowing_rainbow_a(strip,rgb,iterations = 0):
    perPixelRainbowColor(strip,iterations)

def fast_flowing_rainbow_a(strip,rgb,iterations=0):
    run(strip,[rainbowWheel(x) for x in range(0,765)],10,1,0,mirrored=0,iterations=iterations)

def clear_a(strip,rgb,iterations = 0): # default value is 0,0,0, so will clear when button pushed.
    colorAll(strip,Color(rgb[0],rgb[1],rgb[2]))

def bounce_a(strip,rgb,iterations = 0):
    bounce(strip, [Color(rgb[0],rgb[1],rgb[2])],40,0,iterations,speed=5)

def rainbow_bounce_a(strip,rgb,iterations = 0):
    bounce(strip, [rainbowWheel(i) for i in range(0,765,45)],40,0,iterations,speed=5)

def negative_rainbow_bounce_a(strip,rgb,iterations = 0):
    bounce(strip, [Color(0,0,0)], 40, 0, iterations, background_colors=[rainbowWheel(i) for i in range(0,765,45)],speed=5)

def rainbow_wipe_a(strip,rgb,iterations=0):
    list_a = []
    list_b = []
    list_c = []
    color_list = []
    rainbow_list = [rainbowWheel(i) for i in range(0,765,51)]
    for clr1, clr2 in zip(rainbow_list[:len(rainbow_list)//2],rainbow_list[len(rainbow_list)//2:]):
        color_list.append(clr1)
        color_list.append(clr2)
    multi_color_wipe(strip,color_list,0,iterations)

def rainbow_swipe_a(strip,rgb,iterations=0):
    list_a = []
    list_b = []
    list_c = []
    color_list = []
    rainbow_list = [rainbowWheel(i) for i in range(0,765,51)]
    for clr1, clr2 in zip(rainbow_list[:len(rainbow_list)//2],rainbow_list[len(rainbow_list)//2:]):
        color_list.append(clr1)
        color_list.append(clr2)
    multi_color_swipe(strip,color_list,0,iterations)

def set_color_a(strip,rgb,iterations = 0):
    color_spread(strip,Color(rgb[0],rgb[1],rgb[2]),spread_size=50)

def static_rainbow_a(strip,rgb,iterations = 0):
    length = strip.numPixels()
    scale = 765/length
    for pixel in range(length):
        setpixel(strip, pixel, rainbowWheel(int(pixel * scale)))
        if pixel % 5 == 0: strip.show() # <-- comment out this line to show all @ once, keep to 'wipe'
    strip.show()

def negative_bounce_a(strip,rgb,iterations = 0):
        bounce(strip, [Color(0,0,0)], 40, 0, iterations, background_colors=[Color(rgb[0],rgb[1],rgb[2])],speed=5)

def rainbow_fade_a(strip,rgb,iterations = 0):
    rainbowColor(strip, iterations)

def demo_a(strip,rgb,iterations = 0):
    demo(strip)

def alarm_a(strip,rgb,iterations = 1):
    global go
    i=0
    while (i<iterations or iterations==0) and go:
        alert(strip, 5)
        i+=1

def random_flash_a(strip,rgb,iterations = 0):
    randomized(strip,iterations)

def random_flash_rgb_only_a(strip,rgb,iterations = 0):
    randomized(strip,iterations,True)

def cycle_all_a(strip,rgb,iterations = 0):
    global go, animations
    if rgb == Color(0,0,0):
        rgb == Color(255,0,0)
    i=1 # bc this func will call iteslt with iter=1, and this way it wont exec
    while (i<iterations or iterations==0) and go:
        for func in animations.keys():
            if not go: return 0
            if func == "demo" or func == "cycle all functions":
                continue
            iter = {"bounce":2, "negative bounce":2, "rainbow bounce":3, "negative rainbow bounce":3, "random flash":100, "theatre lights":4, "rainbow theatre lights":4}.get(func, 1)
            print(func,flush=True);time.sleep(1)
            animations[func](strip,rgb,iterations = iter)
            time.sleep(1)
            clear(strip)
            time.sleep(1)
        i+=1

def theatre_lights_a(strip,rgb,iterations=0):
    run(strip, [Color(rgb[0],rgb[1],rgb[2])], 1, 1, 2, mirrored=False, dir=1, delay=0.5, iterations=iterations)
    # theatre_lights(strip,[Color(rgb[0],rgb[1],rgb[2])],0.5, iterations)

def rainbow_theatre_lights_a(strip,rgb,iterations=0):
    run(strip, [rainbowWheel(x) for x in range(0,765,85)], 1, 1, 2, mirrored=False, dir=1, delay=0.5, iterations=iterations)
    # theatre_lights(strip,[rainbowWheel(i) for i in range(0,765,45)], 0.5, iterations)

def run_a(strip,rgb,iterations=0):
    run(strip, [Color(rgb[0],rgb[1],rgb[2])], 4, 16, 24, mirrored=True, dir=-1)

def rainbow_run_a(strip, rgb, iterations=0):
    run(strip, [rainbowWheel(x) for x in range(0,765,85)], 4, 16, 24, mirrored=True, dir=-1)

def no_a(strip,rgb,iterations=0):
    no(strip,iterations,delay=0.5)

def also_no_a(strip,rgb,iterations=0):
    no(strip,iterations,delay=0.1)

def really_just_dont_a(strip,rgb,iterations=0):
    no(strip,iterations,delay=0)

def reset_a(strip,rgb,iterations=0):
    global go
    clear(strip)
    go=False

animations = {"set color":set_color_a, "bounce":bounce_a, "negative bounce":negative_bounce_a, "rainbow bounce":rainbow_bounce_a, "negative rainbow bounce":negative_rainbow_bounce_a, "rainbow wipe":rainbow_wipe_a, "rainbow swipe":rainbow_swipe_a, "flowing rainbow":flowing_rainbow_a, "fast flowing rainbow":fast_flowing_rainbow_a, "rainbow fade":rainbow_fade_a, "static rainbow":static_rainbow_a, "random flash":random_flash_a, "random flash rgb only":random_flash_rgb_only_a, "theatre lights":theatre_lights_a, "rainbow theatre lights":rainbow_theatre_lights_a, "run":run_a, "rainbow run":rainbow_run_a, "alarm":alarm_a, "no":no_a, "also no":also_no_a, "really, just dont":really_just_dont_a, "cycle all functions":cycle_all_a, "demo":demo_a, "reset":reset_a, "clear":clear_a}


"""working, but unused because it might clutter up the menu. (maybe I could have an 'advanced' section?)"""


def mirrored_fast_rainbow_a(strip):
    run(setup(),[rainbowWheel(x) for x in range(0,765)],10,1,0, mirrored=True, dir=-1)


if __name__ == "__main__":
    """setup"""
    print("starting...")
    strip = setup()

    demo(strip)
    clear(strip)


"""obsolete"""

def rainbow_theatre_lights_a(strip,rgb,iterations=0):
    theatre_lights(strip,[rainbowWheel(i) for i in range(0,765,45)], 0.5, iterations)

def theatre_lights_a(strip,rgb,iterations=0):
    theatre_lights(strip,[Color(rgb[0],rgb[1],rgb[2])],0.5, iterations)

""" works in progress """

def run_first_try(strip,colors,speed,delay,length,dir=1,background_color=Color(0,0,0), iterations=0):
    global go
    i=0
    while (i<iterations or iterations == 0) and go:
        for ii in range(0,length,speed)[::dir]:
            if not go: return 0
            for pixel in range(strip.numPixels()):
                if pixel % length == ii:
                    setpixel(strip,pixel,colors[(pixel-(ii+(length*i)))%len(colors)])
                else:
                    setpixel(strip,pixel,background_color)
            strip.show()
            time.sleep(delay)
        i += 1

def warm_color_wave_a(strip,rgb,iterations = 0):
    """not currently in use"""
    colors = [rainbowWheel(x, False) for x in range(0,255,51)]
    colors.append(colors[0])
    color_wave(strip,colors, 0, iterations, 1)

def cool_color_wave_a(strip,rgb,iterations = 0):
    """not currently in use"""
    colors = [rainbowWheel(x, False) for x in range(510,765,51)]
    colors.append(colors[0])
    color_wave(strip,colors, 0, iterations, 1)

def color_wave(strip,colors,delay,iterations, dir=1):
    """NOT CURRENTLY WORKING"""
    """FIRST AND LAST COLOR SHOULD BE THE SAME IF DIR != 0
    COLORS ARE RGB VALUE TUPLES, NOT COLOR OBJECT"""
    global go
    dist=strip.numPixels()/(len(colors)-1)
    color_centers = [int(x*dist) for x in range(len(colors))]
    offset=0
    i=0
    while (i < iterations or iterations == 0) and go:
        for pixel in range(strip.numPixels()):
            if not go: return 0
            for j in range(len(color_centers)):
                if pixel >= color_centers[j] and pixel < color_centers[(j+1)%len(colors)]:
                    color_to_left=colors[j]
                    color_to_right=colors[(j+1)%len(colors)]
                    percentage = (pixel-color_centers[j])/dist
                    """if j>=len(color_centers):
                        color_to_right=colors[color_centers[j]]
                    else:
                        color_to_right=colors[color_centers[j+1]] # if color_to_left is the farthest right, color_to_right will be the same"""


            pixel_to_set = (pixel+offset)%strip.numPixels()
            """if pixel_to_set > strip.numPixels():
                pixel_to_set = 0
            elif pixel_to_set < 0:
                pixel_to_set = strip.numPixels()"""

            setpixel(strip,pixel_to_set,fade([color_to_left,color_to_right],percentage))

        strip.show()
        i+=1
        offset += dir
        time.sleep(delay)

def fade(colors, percentage):
    """NOT CURRENTLY WORKING"""
    """colors is a list of 2 rgb values to mix, percentage is much of the first color to mix (seond would be 100-percenage). so 50% would be exact average, 0 would be just the second color. expects int from 0 to 100"""
    avg_red = int((colors[0][0]*(percentage) + colors[1][0]*100-(percentage))/200)
    avg_green = int((colors[0][1]*(percentage) + colors[1][1]*100-(percentage))/200)
    avg_blue = int((colors[0][2]*(percentage) + colors[1][2]*100-(percentage))/200)
    return Color(avg_red,avg_green,avg_blue)
