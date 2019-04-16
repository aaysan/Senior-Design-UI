# Mehmet Alp Aysan
import sys
import os
sys.path.insert(0, './../Senior_Design/')
# print(sys.path)

from flask import render_template
from flask import request
from flask import Flask
import re
import blttest as b
import get_weather as gw
import time
import cv2
import Apparel
import json
import random
import pickle as pkl
import pprint
import make_suggestions as ms

from flask_cors import CORS
app = Flask(__name__, instance_relative_config=False)
CORS(app)
TOTAL_INDICES = 10
MODES = {'select', 'remove', 'add-existing'}
VIEWER_NAME = "Alp Aysan"  # default
FILENAME_TO_CLOTHES = {}
CLOSET_POSITION = 0


class Clothes:
    def __init__(self, filename, owner, position, description="T-Shirt", in_closet=True, color="#fff", occasion="Casual"):
        self.filename = filename
        self.static_filename = "static/{}/{}".format(
            owner.replace(" ", "_"), filename)
        self.owner = owner
        self.position = position
        self.description = description
        self.in_closet = in_closet
        self.color = color
        self.occasion = occasion

    def __repr__(self):
        sb = []
        for key in self.__dict__:
            sb.append("{key}='{value}'".format(
                key=key, value=self.__dict__[key]))

        return ', '.join(sb)


def _save_global_state():
    with open('saved_state.pkl', 'wb') as fp:
        pkl.dump({
            "filename_to_clothes": FILENAME_TO_CLOTHES,
            "closet_position": CLOSET_POSITION,
        }, fp, protocol=pkl.HIGHEST_PROTOCOL)
        pprint.pprint(FILENAME_TO_CLOTHES)
        print("CLOSET_POSITION\t{}".format(CLOSET_POSITION))


def _calc_displacement(target_position):
    if target_position >= CLOSET_POSITION:
        return target_position - CLOSET_POSITION
    return target_position + TOTAL_INDICES - CLOSET_POSITION


def _find_opening_slot():
    indices_available = {i for i in range(TOTAL_INDICES)}
    for filename, item in FILENAME_TO_CLOTHES.items():
        if item.position in indices_available:
            indices_available.remove(item.position)
    for i in range(TOTAL_INDICES):
        if i in indices_available:
            return i
    raise Exception("CLOSET IS FULL--TODO HANDLE THIS CASE")


@app.route("/", methods=['GET', 'POST'])
def hello():
    return render_template('main_page.html')


@app.route("/fr_res")
def face_recog():
    global VIEWER_NAME

    a = b.get_name()
    pattern = r'Name:(.*)\n'
    res = re.findall(pattern, a)

    if len(res) > 0:
        name = res[0].strip()
        VIEWER_NAME = name
        if name != 'outsider':
            return render_template('main_page_recognized.html', name=name)
    return render_template('main_page_not_recognized.html')


@app.route("/logged_in")
def show_options():
    mode = request.args.get('mode')
    if request.args.get('mode'):
        # call blttest.close_door()
        time.sleep(3)
        filename = request.args.get('filename')
        if mode == 'select':
            FILENAME_TO_CLOTHES[filename].in_closet = False
        elif mode == 'remove':
            os.remove(FILENAME_TO_CLOTHES[filename].static_filename)
            FILENAME_TO_CLOTHES.pop(filename)
        elif mode == 'add-existing':
            FILENAME_TO_CLOTHES[filename].in_closet = True
        _save_global_state()

    weather = {'Temperature': 300}  # gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    return render_template('post_login_main.html', name=VIEWER_NAME, temperature=temperature)


@app.route("/add_clothes", methods=['GET', 'POST'])
def add_clothes():
    weather = {'Temperature': 300}  # gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    return render_template('add_clothes.html', name=VIEWER_NAME, temperature=temperature)


@app.route("/add_new_clothes", methods=['GET', 'POST'])
def add_new_clothes():
    # Take Picture
    cap = cv2.VideoCapture(0)
    time.sleep(0.5)

    ret, frame = cap.read()
    cap.release()

    opening_slot = _find_opening_slot()
    # TODO (what happens if all spots are filled??)
    filename = str(random.getrandbits(32)) + '.jpg'

    FILENAME_TO_CLOTHES[filename] = Clothes(
        filename, VIEWER_NAME, opening_slot, in_closet=False)


    file_path = FILENAME_TO_CLOTHES[filename].static_filename

    cv2.imwrite(file_path, frame)
    names, colors = Apparel.finditemandcolor(file_path)

    # Change camelCase to camel case for colors
    for item in colors:
        item['name'] = re.sub(
            "([a-z])([A-Z])", "\g<1> \g<2>", item['name'])
                
    return render_template('add_new_radio_buttons.html', names=names, colors=colors, filename=filename)


@app.route("/add_new_clothes_response", methods=['GET'])
def add_new_clothes_response():
    filename = request.args['filename']
    FILENAME_TO_CLOTHES[filename].description = request.args['desc'].split(',')[0]
    FILENAME_TO_CLOTHES[filename].occasion = request.args['desc'].split(',')[1]
    if 'color' in request.args:
        FILENAME_TO_CLOTHES[filename].color = request.args['color']


    return render_template('load.html', filename=filename,
                           title="Finding an opening for {}".format(request.args['desc']), mode="add-existing")


@app.route("/clothes_viewer")
def clothes_viewer():
    mode = request.args['mode']
    assert mode in MODES
    weather = {'Temperature': 300}  # gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)

    if mode == 'select':
        title = "Select your desired clothes"

        def valid_clothes(clothes):
            return clothes.in_closet
    elif mode == 'remove':
        title = "Select clothes to permanently remove"

        def valid_clothes(clothes):
            return clothes.in_closet
    elif mode == 'add-existing':
        title = "Select clothes you would like to add"

        def valid_clothes(clothes):
            return not clothes.in_closet

    data = []
    for filename, clothes in FILENAME_TO_CLOTHES.items():
        if clothes.owner == VIEWER_NAME and valid_clothes(clothes):
            data.append(clothes)

    return render_template('clothes_viewer.html', name=VIEWER_NAME, temperature=temperature,
                           filename_tup=data, data_len=len(data), title=title, mode=mode)


@app.route("/retrieve_select_loading")
def retrieve_select_loading():
    filename = request.args.get('filename')
    mode = request.args.get('mode')
    if mode == 'select' or mode == 'remove':
        title = "Retrieving selected clothes"
    elif mode == 'add-existing':
        title = "Finding an opening"
    return render_template('load.html', filename=filename, title=title, mode=mode)


@app.route("/retrieve_select_done")
def retrieve_select_done():
    global CLOSET_POSITION
    filename = request.args.get('filename')
    displacement = _calc_displacement(FILENAME_TO_CLOTHES[filename].position)
    print("Calling: blttest.closet_open({})\ttarget={}\tcurr_pos={}".format(
        displacement, FILENAME_TO_CLOTHES[filename].position, CLOSET_POSITION))
    time.sleep(3)  # call blttest.closet_open(displacement) here
    CLOSET_POSITION = FILENAME_TO_CLOTHES[filename].position
    return "done fetching {}".format(filename)  # return response is not used


@app.route("/close_door_begin")
def close_door_begin():
    mode = request.args.get('mode')
    if mode == 'select':
        title = "Please take out clothes from opening"
    elif mode == 'remove':
        title = "Please take out clothes from opening, removing clothes from system"
    elif mode == 'add-existing':
        title = "Please insert clothes onto the opening"
    return render_template('close_door.html', title=title, mode=mode, filename=request.args.get('filename'))


@app.route("/recommend_clothes",methods=['GET','POST'])
def recommend_clothes():
    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    print(temperature)
    if request.method == 'POST':
        occasion = request.form['options']

        possible_attires = []
        for filename, item in FILENAME_TO_CLOTHES.items():
            # print("----------------------------")
            # print(VIEWER_NAME)
            # print(item.owner)
            if item.owner == VIEWER_NAME:
                possible_attires.append(item)

        result = ms.make_suggestions(weather,occasion,possible_attires)





        return str(result)

    return render_template('recommend_clothes.html', name=VIEWER_NAME, temperature=temperature)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


if __name__ == '__main__':
    with open("saved_state.pkl", 'rb') as fp:
        metadata = pkl.load(fp)
        FILENAME_TO_CLOTHES = metadata['filename_to_clothes']
        CLOSET_POSITION = metadata['closet_position']
        # for key, item in FILENAME_TO_CLOTHES.items():
        #     print(item)
        # del FILENAME_TO_CLOTHES['2222.jpg']
        # del FILENAME_TO_CLOTHES['5555.jpg']
        # del FILENAME_TO_CLOTHES['217017092728452067427996135764960391696.jpg']
        # del FILENAME_TO_CLOTHES['2678892138.jpg']
        # del FILENAME_TO_CLOTHES['1111.jpg']
        # del FILENAME_TO_CLOTHES['4444.jpg']
        # del FILENAME_TO_CLOTHES['3333.jpg']
        # del FILENAME_TO_CLOTHES['4037302841.jpg']

    # _save_global_state()
    app.run(debug=True)
