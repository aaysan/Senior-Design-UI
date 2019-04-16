from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import re
import pprint as pp

def finditemandcolor(imageurl):

    app = ClarifaiApp(api_key='e5af645934f34cee8ec140028c1fff12')
    model = app.models.get('apparel')
    image = ClImage(filename=imageurl)
    itemspredict = model.predict([image])

    # pp.pprint(itemspredict)
    model2 = app.models.get('color')
    # image = ClImage(url=imageurl)
    # print(image)

    colorpredict = model2.predict_by_filename(imageurl)
    # print(clorpredict)
    # pass
    try:
        itemlist = sorted(itemspredict["outputs"][0]["data"]["concepts"], key=lambda k: k['value'],reverse=True)
        if(len(itemlist)>5):
            itemlist = itemlist[:5]
        else:
            itemlist = itemlist
    except:
        itemlist = []

    # pp.pprint(colorpredict)
    # pp.pprint(itemlist)
    # pass
    try:
        colorlist = sorted(colorpredict["outputs"][0]["data"]["colors"], key=lambda k: k['value'],reverse=True)
        if(len(colorlist)>5):
            colorlist = itemlist[:5]
        else:
            colorlist = colorlist
    except:
        colorlist = []

    finalitemlist = []
    finalcolorlist = []
    tempdict = dict()

    for i in itemlist:
        tempdict["name"] = i["name"]
        tempdict["value"] = i["value"]
        tempdict["Occasion"] = get_occasion(tempdict["name"])
        finalitemlist += [tempdict]
        tempdict = dict()
    tempdict = dict()
    for i in colorlist:
        print(i)
        try:
            tempdict["name"] = i["w3c"]["name"]
            tempdict["value"] = i["value"]
            tempdict["hex"] = i["w3c"]["hex"]

            finalcolorlist += [tempdict]
            tempdict = dict()
        except:
            print(i)

    return(finalitemlist,finalcolorlist)


def get_occasion(name):
    # Casual, Sportwear, Business/Business Casual

    sportspattern = ".*Activewear.*"
    sportwear = re.search(sportspattern,name)


    if sportwear is not None:
        return "Sports|Activewear"

    businesspattern = "Blazer|Button-Down|Blouse|Button-Up|Pant Suit|Tie|Vest"
    businesswear = re.search(businesspattern,name)

    if businesswear is not None:
        return "Business|Business Casual"



    return "Casual|Daily"

if __name__ == "__main__":
    temp1,temp2 = finditemandcolor("static/Alp Aysan/1.jpg")
    # pp.pprint(temp1)
    # print("-------------------")
    # pp.pprint(temp2)