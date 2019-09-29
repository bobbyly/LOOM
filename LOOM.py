#LOOM

import pyautogui as pg
import time
import numpy
start_time = time.time()
end_x, end_y = pg.size()

#variables
origin_x, origin_y = 600, 155 #the starting point of the draw
distance = 40 #how intially big the draw is
duration = 0.1 #the draw time (0 == 0.1)
updown = -5 #north south
leftright = 10 #east west
NEWS_modifier = 5 #FKA fukitup
gap = 5 #the gap that reduces distance at each turn
o_factor = 1 #oblong factor
steps = (distance/gap)/2
height = origin_y + (distance - gap) #the intial length of the line after the first turn
width = origin_x + distance #the intial length of the first line
stop_here = -80 #either another variable or an integer

mods = 'on'
draw_lines = ['N', 'S', 'E']
move_lines = []#['E', 'W', 'S', 'N']
cardinal = ['NE', 'SW']
turn = 0

variableslist = ['origin_x, origin_y = '+str(origin_x)+', '+str(origin_y),
'distance = '+str(distance),
'duration = '+str(duration),
'updown = '+str(updown),
'leftright = '+str(leftright),
'NEWS_modifier = '+str(NEWS_modifier),
'gap = '+str(gap),
'o_factor = '+str(o_factor),
'stop_here = '+str(stop_here),
'mods = '+str(mods),
'draw_lines = '+str(draw_lines),
'move_lines = '+str(move_lines),
'cardinal = '+str(cardinal)]

print('this will take approx ' + str(steps) + ' steps. approx ' + str(steps * max(duration, 0.11) * 4) + ' seconds.')

pg.doubleClick(330, 65)
pg.moveTo(origin_x, origin_y)
pg.rightClick()  #click to put drawing program in focus


while distance > stop_here and width < end_x and height < end_y and leftright < end_x and updown < end_y:
    if 'E' in draw_lines:
        if turn == 0:
            pg.dragRel((distance * o_factor) - gap, leftright, duration=duration)  # draw right
            turn += 1
        else:
            pg.dragRel(distance * o_factor, leftright, duration=duration)  # draw right
    elif 'E' in move_lines:
        pg.moveRel(distance * o_factor, leftright) #move right

    if 'NE' in cardinal:
        distance = distance - gap #this controls NE also turn should be 1

    if 'S' in draw_lines:
        pg.dragRel(updown, distance, duration=duration)   # draw down
    elif 'S' in move_lines:
        pg.moveRel(updown, distance)   # draw down

    if 'SE' in cardinal:
        distance = distance - gap #this controls SE

    if 'W' in draw_lines:
        pg.dragRel(-distance*o_factor, -leftright, duration=duration)  # draw left
    elif 'W' in move_lines:
        pg.moveRel(-distance * o_factor, -leftright)  #move left

    if 'SW' in cardinal:
        distance = distance - gap #this controls SW

    if 'N' in draw_lines:
        pg.dragRel(-updown, -distance, duration=duration)  # draw up
    elif 'N' in move_lines:
        pg.moveRel(-updown,-distance) #move up

    if 'NW' in cardinal:
        distance = distance - gap #this controls NW

    if mods == 'on':
        leftright = leftright + NEWS_modifier
        updown = updown - NEWS_modifier

    turn += 1

    print('turn:       ' + str(turn).rjust(3))
    print('distance:   ' + str(distance).rjust(3))
    print('up down:    ' + str(updown).rjust(3))
    print('left right: ' + str(leftright).rjust(3))

print("seconds taken: ", time.time() - start_time)

logfilename = pg.prompt(text='Would you like to save these variables?',
          title='Would you like to save these variables?' , default='file name')
if logfilename is not None:
    numpy.savetxt(logfilename+'.txt', variableslist, fmt="%s", delimiter=',')