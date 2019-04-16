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

from flask_cors import CORS
app = Flask(__name__, instance_relative_config=False)
CORS(app)


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
            sb.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))

        return ', '.join(sb)


class Information:
    name = "Alp Aysan"
    count = 0
    filename_to_clothes = {
        # Dummy inits
        '1111.jpg': Clothes('1111.jpg', 'Alp Aysan', 1),
        '2222.jpg': Clothes('2222.jpg', 'Alp Aysan', 2, description='tshirt2'),
        '3333.jpg': Clothes('3333.jpg', 'Alp Aysan', 3, description='jeans'),
        '4444.jpg': Clothes('4444.jpg', 'Alp Aysan', 4, description='random'),
        '5555.jpg': Clothes('5555.jpg', 'Alp Aysan', 5, description='alp'),

    }

    def __init__(self):
        return


@app.route("/", methods=['GET', 'POST'])
def hello():
    return render_template('main_page.html')


@app.route("/fr_res")
def face_recog():
    a = b.get_name()
    pattern = r'Name:(.*)\n'
    res = re.findall(pattern, a)

    if len(res) > 0:
        name = res[0].strip()
        Information.name = name
        if name != 'outsider':
            return render_template('main_page_recognized.html', name=name)
    return render_template('main_page_not_recognized.html')


@app.route("/logged_in")
def show_options():
    if request.args.get('door_close'):
        print("please call close door")
        # call blttest.close_door()
        time.sleep(3)
    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    return render_template('post_login_main.html', name=Information.name, temperature=temperature)


@app.route("/add_clothes", methods=['GET', 'POST'])
def add_clothes():
    if request.method == 'POST':
        if 'take_pic' in request.form:

            # Take Picture

            split_name = Information.name.split()
            name = Information.name
            lastname = ""
            if len(split_name) > 1:
                name = split_name[0]
                last_name = split_name[1]

            cap = cv2.VideoCapture(0)
            time.sleep(0.5)

            ret, frame = cap.read()
            cap.release()

            opening_slot = 1  # TODO (logic to find opening space)
            # TODO (what happens if all spots are filled??)
            filename = str(random.getrandbits(128)) + '.jpg'
            Information.filename_to_clothes[filename] = Clothes(
                filename, Information.name, opening_slot)
            file_path = Information.filename_to_clothes[filename].static_filename
            cv2.imwrite(file_path, frame)
            names, colors = Apparel.finditemandcolor(file_path)

            # Change camelCase to camel case
            for item in colors:
                item['name'] = re.sub(
                    "([a-z])([A-Z])", "\g<1> \g<2>", item['name'])

            return render_template('add_new_radio_buttons.html', names=names, colors=colors, filename=filename)

        if 'add_existing' in request.form:
            return "This should be the page that display existing stuff"

    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    return render_template('add_clothes.html', name=Information.name, temperature=temperature)


@app.route("/add_new_clothes", methods=['GET'])
def add_new_clothes():
    filename = request.args['filename']
    Information.filename_to_clothes[filename].description = request.args['desc']
    Information.filename_to_clothes[filename].color = request.args['color']
    # print(Information.filename_to_clothes[filename])
    return str(Information.filename_to_clothes[filename])


@app.route("/remove_clothes")
def remove_clothes():
    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    data = []
    for filename in os.listdir("./static/{}".format(Information.name.replace(" ", "_"))):
        clothe = Information.filename_to_clothes[filename]
        if not clothe.in_closet:
            continue
        data.append(clothe)
    return render_template('remove_clothes.html', name=Information.name, temperature=temperature, filename_tup=data, data_len=len(data))


@app.route("/retrieve_select_loading")
def retrieve_select_loading():
    filename = request.args.get('clothe')
    return render_template('load.html', filename=filename)


@app.route("/retrieve_select_done")
def retrieve_select_done():
    time.sleep(3)
    filename = request.args.get('clothe')
    return "done fetching {}".format(filename)


@app.route("/close_door_begin")
def close_door_begin():
    return render_template('close_door.html')


@app.route("/display_clothes")
def display_clothes():
    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    return render_template('select_clothes.html', name=Information.name)


@app.route("/recommend_clothes")
def recommend_clothes():
    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    return render_template('recommend_clothes.html', name=Information.name, temperature=temperature)


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
    app.run(debug=True)
