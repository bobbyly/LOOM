#LOOM
import pyautogui as pg
import time
from pynput.mouse import Listener
import logging
import re

logging.basicConfig(level=logging.DEBUG)

# for the calibration cycle
calibration_point = None
calibration_point_coordinates = [
    'Top_left',
    'Top_right',
    'Bottom_right',
    'Bottom_left']
end_x, end_y = pg.size()

# variables
variables_dict = {
    'turn': 0,
    'origin_x': None,
    'origin_y': None,
    'distance': None,
    'duration': None,
    'updown': None,
    'leftright': None,
    'NEWS_modifier': None,
    'gap': None,
    'oblong_factor': None,
    'stop_here': None,
    'mods': None,
    'draw_these_lines': None,
    'move_these_lines': None,
    'cardinal_direction_of_drawing': None,
    'Top_left': (0, 0),
    'Top_right': (0, end_y),
    'Bottom_right': pg.size(),
    'Bottom_left': (end_x, 0)
}


with open("config_file.txt") as config_file:
    for line in config_file:
       try:
           (key, val) = line.split(maxsplit=1)
           float_re = re.findall("\.", val)
           int_re = re.findall('\d', val)
       except ValueError:
           pass
       if float_re:
        variables_dict[str(key)] = float(val.strip('\n'))
       elif int_re:
           variables_dict[str(key)] = int(val.strip('\n'))
       else:
           variables_dict[str(key)] = val.strip('\n')


def on_click(calibration_x, calibration_y, button, pressed):
    global calibration_point
    if pressed:
        calibration_point = None
        print('Mouse clicked at ({0}, {1})'.format(calibration_x, calibration_y))
        calibration_point = (calibration_x, calibration_y)
        return False


def calibration_point_set(coordinate):
    global calibration_point
    variables_dict[coordinate] = calibration_point
    calibration_point = None
    return "{0} point set".format(coordinate)


calibration_response = pg.confirm('Would you like to calibrate your screen', 'Calibration Query', buttons=['Yes', 'No'])
if calibration_response == 'Yes':
    # if we need to reset calibration, then clear the CPO values
    for each in calibration_point_coordinates:
        variables_dict[each] = None
    pg.alert(text='Please confirm then click on the Top Left corner', title='Confirmation', button='OK')
    for points in calibration_point_coordinates:
        Listener(on_click=on_click).start()
        try:
            while variables_dict[points] is None:
                time.sleep(0.5)
                if calibration_point is not None:
                    print(calibration_point_set(points))
            if points != 'Bottom_left':
                pg.alert(text=str(points) + ' coordinates captured. Confirm then click on the next clockwise corner',
                         title='Confirmation', button='OK')
        except Exception as e:
            logging.info(e)
            pass
    pg.alert(text='All corner coordinates captured:\n' + str(variables_dict['Top_left']) + '\n'
                  + str(variables_dict['Top_right']) + '\n' + str(variables_dict['Bottom_right']) + '\n'
                  + str(variables_dict['Bottom_left']),
             title='Success',
             button='OK')

# start timer and set corners
start_time = time.time()
x_points = []
y_points = []
for each in calibration_point_coordinates:
    x_point, y_point = variables_dict[each]
    x_points.append(x_point)
    y_points.append(y_point)

right_x = max(x_points)
left_x = min(x_points)
top_y = max(y_points)
bottom_y = min(y_points)


# the engine room

steps = (variables_dict['distance'] / variables_dict['gap']) / 2
height = variables_dict['origin_y'] + (variables_dict['distance'] - variables_dict['gap'])
width = variables_dict['origin_x'] + variables_dict['distance']
origin_turn = variables_dict['turn']
origin_distance = variables_dict['distance']
print('this will take approx ' + str(steps) + ' steps or approx ' + str(steps * max(variables_dict['duration'], 0.11) * 4) + ' seconds.')

# pg.doubleClick(330, 65)
pg.moveTo(variables_dict['origin_x'], variables_dict['origin_y'])
pg.rightClick()  # click to put drawing program in focus
end_point_x, end_point_y = pg.position()

while variables_dict['distance'] > variables_dict['stop_here'] and width < right_x and height < top_y \
        and variables_dict['leftright'] < right_x and variables_dict['updown'] < top_y and \
        end_point_x < right_x and end_point_y < top_y and end_point_x > left_x and end_point_y > bottom_y:

    if 'NE' in variables_dict['cardinal_direction_of_drawing']:
        turn = 1

    if 'E' in variables_dict['draw_these_lines']:
        if variables_dict['turn'] == 0:
            pg.dragRel((variables_dict['distance'] * variables_dict['oblong_factor']) - variables_dict['gap'], variables_dict['leftright'], duration=variables_dict['duration'])  # draw right
            variables_dict['turn'] += 1
        else:
            pg.dragRel(variables_dict['distance'] * variables_dict['oblong_factor'], variables_dict['leftright'], duration=variables_dict['duration'])  # draw right
    elif 'E' in variables_dict['move_these_lines']:
        pg.moveRel(variables_dict['distance'] * variables_dict['oblong_factor'], variables_dict['leftright']) #move right

    if 'NE' in variables_dict['cardinal_direction_of_drawing']:
        variables_dict['distance'] = variables_dict['distance'] - variables_dict['gap']

    if 'S' in variables_dict['draw_these_lines']:
        pg.dragRel(variables_dict['updown'], variables_dict['distance'], duration=variables_dict['duration'])   # draw down
    elif 'S' in variables_dict['move_these_lines']:
        pg.moveRel(variables_dict['updown'], variables_dict['distance'])   # move down

    if 'SE' in variables_dict['cardinal_direction_of_drawing']:
        variables_dict['distance'] = variables_dict['distance'] - variables_dict['gap'] #this controls SE

    if 'W' in variables_dict['draw_these_lines']:
        pg.dragRel(-variables_dict['distance']*variables_dict['oblong_factor'], -variables_dict['leftright'], duration=variables_dict['duration'])  # draw left
    elif 'W' in variables_dict['move_these_lines']:
        pg.moveRel(-variables_dict['distance'] * variables_dict['oblong_factor'], -variables_dict['leftright'])  #move left

    if 'SW' in variables_dict['cardinal_direction_of_drawing']:
        variables_dict['distance'] = variables_dict['distance'] - variables_dict['gap'] #this controls SW

    if 'N' in variables_dict['draw_these_lines']:
        pg.dragRel(-variables_dict['updown'], -variables_dict['distance'], duration=variables_dict['duration'])  # draw up
    elif 'N' in variables_dict['move_these_lines']:
        pg.moveRel(-variables_dict['updown'],-variables_dict['distance']) #move up

    if 'NW' in variables_dict['cardinal_direction_of_drawing']:
        variables_dict['distance'] = variables_dict['distance'] - variables_dict['gap'] #this controls NW

    if variables_dict['mods'] == 'on':
        variables_dict['leftright'] = variables_dict['leftright'] + variables_dict['NEWS_modifier']
        variables_dict['updown'] = variables_dict['updown'] - variables_dict['NEWS_modifier']

    variables_dict['turn'] += 1

    print('turn:       ' + str(variables_dict['turn']).rjust(3))
    print('distance:   ' + str(variables_dict['distance']).rjust(3))
    print('up down:    ' + str(variables_dict['updown']).rjust(3))
    print('left right: ' + str(variables_dict['leftright']).rjust(3) + '\n')

    end_point_x, end_point_y = pg.position()

print("seconds taken: ", time.time() - start_time)

logfilename = pg.prompt(text='Would you like to save these variables?',
                        title='Would you like to save these variables?', default='file name')
if logfilename is not None:
    write_file = open(logfilename+'.txt',"w")
    variables_dict['turn'] = origin_turn
    variables_dict['distance'] = origin_distance
    config_write = str(variables_dict).replace(', ','\n',15).replace("{","").replace("}","").replace("'","").replace(":","")
    write_file.write(config_write)
    write_file.close()

