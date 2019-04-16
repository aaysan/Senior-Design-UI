# Mehmet Alp Aysan

import re
import requests
import json
import pprint as pp

def make_suggestions(weather,occasion,attires):


    temperature = weather["Temperature"] - 273
    print(temperature)
    # get inputs about the occasion

    rainpattern = r"rain|snow|shower|flurries|storm"
    coldpattern = r"sweat|hoodie|cardigan"
    verycoldpattern = r"coat|jacket|turtleneck"
    warmpattern = r"short|t-shirt|tshirt"

    suggestions = set()

    # occasion = input("What is the occasion? ((B)usiness,Casual,Sportwear\n->")
    # pp.pprint(attires)

    for elem in attires:

        if int(temperature) < 15:
            cold_match = re.search(coldpattern, elem.description)
            if cold_match is not None:
                suggestions.add(elem.static_filename)

        if int(temperature) < 2:
            very_cold_match = re.search(verycoldpattern, elem.description)
            # print("its too cold. Would you like a jacket? " );
            if very_cold_match is not None:
                suggestions.add(elem.static_filename)

        if int(temperature) > 15:
            warm_match = re.search(warmpattern, elem.description)
            if warm_match is not None:
                suggestions.add(elem.static_filename)

        isRainy = re.search(rainpattern,weather["Description"].lower())
        if isRainy is not None:
           suggestions.add("Umbrealla")

        if elem.occasion == occasion:
            suggestions.add(elem.static_filename)

    pp.pprint(suggestions)
    # final_url_list = set()
    #
    # for elem in possible_attires:
    #
    #     if elem['cloth']['name'] in suggestions:
    #         final_url_list.add(elem['_id']['$oid'])

    return suggestions


#
# weather = dict()
# weather["Description"] = "Partly Cloudy"
# weather["Temperature"] = "22"
# res = make_suggestions(weather, "Alp", "Casual")
# print("--done--")
# print(res)
# # print(len(res))