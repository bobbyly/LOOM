#LOOM
import pyautogui as pg
import time
import numpy
from pynput.mouse import Listener
import logging

logging.basicConfig(level=logging.DEBUG)
start_time = time.time()
calibration_point = None
calibration_point_coordinates = {
    'Top left': None,
    'Top right': None,
    'Bottom right': None,
    'Bottom left': None}

def on_click(calibration_x, calibration_y, button, pressed):
    global calibration_point
    if pressed:
        calibration_point = None
        print('Mouse clicked at ({0}, {1})'.format(calibration_x, calibration_y))
        calibration_point = (calibration_x, calibration_y)
        return False

def calibration_point_set(coordinate):
    global calibration_point
    calibration_point_coordinates[coordinate] = calibration_point
    calibration_point = None
    return


calibration_response = pg.confirm('Would you like to calibrate your screen', 'Calibration Query', buttons=['Yes','No'])
if calibration_response == 'Yes':
    pg.alert(text='Please confirm then click on the Top Left corner', title='Confirmation', button='OK')
    for points in calibration_point_coordinates:
        Listener(on_click=on_click).start()
        try:
            while calibration_point_coordinates[points] is None:
                time.sleep(0.5)
                if calibration_point is not None:
                    calibration_point_set(points)
            if points != 'Bottom left':
                pg.alert(text= str(points) + ' coordinates captured. Confirm then click on the next clockwise corner',
                         title='Confirmation', button='OK')
        except Exception as e:
            logging.info(e)
            pass
    pg.alert(text='All corner coordinates captured:\n' + str(calibration_point_coordinates), title='Success',
             button='OK')


end_x, end_y = pg.size()

#variables
off = 'OFF'
on = 'ON'
turn = 0
origin_x, origin_y = 800, 365 #the starting point of the draw
distance = 100 #how intially big the draw is
duration = 0.1 #the draw time (0 == 0.1)
updown = 0 #north south
leftright = 0 #east west
NEWS_modifier = 0 #FKA fukitup
gap = 4 #the gap that reduces distance at each turn
oblong_factor = 1 #oblong factor
steps = (distance/gap)/2
height = origin_y + (distance - gap) #the intial length of the line after the first turn
width = origin_x + distance #the intial length of the first line
stop_here = 0 #either another variable or an integer
mods = 'off'
draw_these_lines = ['N', 'S', 'E']
move_these_lines = ['W']#['E', 'W', 'S', 'N']
cardinal_direction_of_drawing = ['NE', 'SW'] #['NE', 'SW'] is equilibrium

variables_dictionary = {
    'turn': 0,
    'origin_x': origin_x,
    'origin_y': origin_y,
    'distance': distance,
    'duration': duration,
    'updown': updown,
    'leftright': leftright,
    'NEWS_modifier': NEWS_modifier,
    'gap': gap,
    'oblong_factor': oblong_factor,
    'steps': steps,
    'stop_here': stop_here,
    'mods': mods,
    'draw_these_lines': draw_these_lines,
    'move_these_lines': move_these_lines,
    'cardinal_direction_of_drawing': cardinal_direction_of_drawing
}


print('this will take approx ' + str(steps) + ' steps. approx ' + str(steps * max(duration, 0.11) * 4) + ' seconds.')

pg.doubleClick(330, 65)
pg.moveTo(origin_x, origin_y)
pg.rightClick()  #click to put drawing program in focus


while distance > stop_here and width < end_x and height < end_y and leftright < end_x and updown < end_y:

    if 'NE' in cardinal_direction_of_drawing:
        turn = 1

    if 'E' in draw_these_lines:
        if turn == 0:
            pg.dragRel((distance * oblong_factor) - gap, leftright, duration=duration)  # draw right
            turn += 1
        else:
            pg.dragRel(distance * oblong_factor, leftright, duration=duration)  # draw right
    elif 'E' in move_these_lines:
        pg.moveRel(distance * oblong_factor, leftright) #move right

    if 'NE' in cardinal_direction_of_drawing:
        distance = distance - gap

    if 'S' in draw_these_lines:
        pg.dragRel(updown, distance, duration=duration)   # draw down
    elif 'S' in move_these_lines:
        pg.moveRel(updown, distance)   # draw down

    if 'SE' in cardinal_direction_of_drawing:
        distance = distance - gap #this controls SE

    if 'W' in draw_these_lines:
        pg.dragRel(-distance*oblong_factor, -leftright, duration=duration)  # draw left
    elif 'W' in move_these_lines:
        pg.moveRel(-distance * oblong_factor, -leftright)  #move left

    if 'SW' in cardinal_direction_of_drawing:
        distance = distance - gap #this controls SW

    if 'N' in draw_these_lines:
        pg.dragRel(-updown, -distance, duration=duration)  # draw up
    elif 'N' in move_these_lines:
        pg.moveRel(-updown,-distance) #move up

    if 'NW' in cardinal_direction_of_drawing:
        distance = distance - gap #this controls NW

    if mods == 'on':
        leftright = leftright + NEWS_modifier
        updown = updown - NEWS_modifier

    turn += 1

    print('turn:       ' + str(turn).rjust(3))
    print('distance:   ' + str(distance).rjust(3))
    print('up down:    ' + str(updown).rjust(3))
    print('left right: ' + str(leftright).rjust(3) + '\n')

print("seconds taken: ", time.time() - start_time)

logfilename = pg.prompt(text='Would you like to save these variables?',
          title='Would you like to save these variables?' , default='file name')
if logfilename is not None:
    numpy.savetxt(logfilename+'.txt', variableslist, fmt="%s", delimiter=',')


