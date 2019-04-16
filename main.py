#Mehmet Alp Aysan
import sys
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

app = Flask(__name__,instance_relative_config=False)

class Information:
    name = "Alp Aysan"
    flag = 0
    count = 0

    def __init__(self):
        return


@app.route("/",methods=['GET', 'POST'])
def hello():
    return render_template('main_page.html')

@app.route("/fr_res")
def face_recog():
    a = b.get_name()
    pattern = r'Name:(.*)\n'
    res = re.findall(pattern,a)

    if len(res) > 0:
        name = res[0].strip()
        Information.name = name
        if name != 'outsider':
            return render_template('main_page_recognized.html', name=name)
    return render_template('main_page_not_recognized.html')

@app.route("/logged_in")
def show_options():

    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    return render_template('post_login_main.html',name=Information.name,temperature=temperature)

@app.route("/add_clothes", methods=['GET', 'POST'])
def add_clothes():


    if request.method == 'POST':
        if 'take_pic' in request.form:

            #Take Picture
            cap = cv2.VideoCapture(0)
            time.sleep(0.5)

            ret, frame = cap.read()
            file_path = Information.name + str(Information.count) + ".png"
            cv2.imwrite(file_path, frame)

            temp1, temp2 = Apparel.finditemandcolor(file_path)

            cap.release
            print("released")

            return json.dumps([temp1,temp2])

    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    return render_template('add_clothes.html', name=Information.name,temperature=temperature)

@app.route("/remove_clothes")
def remove_clothes():
    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    #
    if (Information.flag == 1):
        Information.flag = 0
        time.sleep(50)
        render_template('display.html',name=Information.name,temperature=temperature)
    # return make_response('POST request successful', 200)
    #
    Information.flag = 1
    return render_template('temp.html', name=Information.name,temperature=temperature)


@app.route("/display_clothes")
def display_clothes():
    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    return render_template('select_clothes.html', name=Information.name)

@app.route("/recommend_clothes")
def recommend_clothes():
    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    return render_template('recommend_clothes.html', name=Information.name,temperature=temperature)

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
