#Mehmet Alp Aysan
import sys
sys.path.insert(0, './../Senior_Design/')
# print(sys.path)


from flask import render_template
from flask import Flask
import re
import blttest as b
import get_weather as gw

app = Flask(__name__,instance_relative_config=False)

class Information:
    name = "Alp Aysan"

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

@app.route("/add_clothes")
def add_clothes():
    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    return render_template('add_clothes.html', name=Information.name,temperature=temperature)

@app.route("/remove_clothes")
def remove_clothes():
    weather = gw.get_weather_info()
    temperature = "%0d C" % (weather["Temperature"] - 273)
    return render_template('display.html', name=Information.name,temperature=temperature)


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
    app.run()
