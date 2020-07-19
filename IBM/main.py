from flask import Flask, render_template
import random, string
import UI_keliye as u
import datetime as dt

u.get_static_timetable()

main = Flask(__name__)
main.secret_key = "t0xic0der"


bruhmane = [
        [12, 0],
        [24, 1],
        [18, 2],
        [16, 3],
        [14, 4],
        [26, 5],
        [28, 6],
        [12, 7],
        [12, 8],
        [12, 9],
        [12, 10],
        [12, 11],
        [12, 12],
        [12, 13],
        [12, 14],
        [12, 15],
        [12, 16],
        [12, 17],
        [12, 18],
        [12, 19],
        [12, 20],
        [12, 21],
        [12, 22]
    ]


def timeconv(intg):
    if 0 <= intg < 10:
        return "0"+str(intg)+":00"
    else:
        return str(intg)+":00"


def getsched():
    totalist = []
    for indx in range(0, 23):
        pathkeys = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        randqant = random.randint(0, 40)
        pathlist = []
        for jndx in range(randqant):
            fromdest = {
                "srce": ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
                "dest": ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
            }
            pathlist.append(fromdest)
        semidict = {}
        semidict["pathkeys"] = pathkeys
        semidict["timedata"] = timeconv(indx)
        semidict["busquant"] = randqant
        semidict["trafdens"] = random.randint(0,50)
        semidict["occupanc"] = random.randint(0,25)
        semidict["delaposs"] = random.randint(0,25)
        semidict["distance"] = random.randint(90,100)
        semidict["pathlist"] = pathlist
        totalist.append(semidict)
    return totalist


def getstate():
    totalist = []
    actilist = u.get_static_timetable() #REPLACE THIS WITH STATIC ENUMERATED LIST (REMOVE THE GETSCHED FUNCTION IF THIS WORKS PERFECTLY)
    print(len(actilist))
    for indx in range(len(actilist)):
        pathkeys = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        randqant = actilist[indx][0]
        pathlist = []
        for jndx in range(randqant):
            fromdest = {
                "srce": ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
                "dest": ''.join(random.choices(string.ascii_uppercase + string.digits, k=8)),
            }
            pathlist.append(fromdest)
        semidict = {}
        semidict["pathkeys"] = pathkeys
        semidict["timedata"] = timeconv(actilist[indx][1])
        semidict["busquant"] = randqant
        semidict["trafdens"] = random.randint(0,50)
        semidict["occupanc"] = random.randint(0,25)
        semidict["delaposs"] = random.randint(0,25)
        semidict["distance"] = random.randint(90,100)
        semidict["pathlist"] = pathlist
        totalist.append(semidict)
    return totalist


@main.route("/", methods=["GET", "POST"])
def webinter():
    return render_template("webstate.html", pathdict=getstate())


@main.route("/dynasked/")
def dynasked():
    hour=dt.datetime.now().hour
    listdata = list(enumerate(u.get_dynamic_timetable(hour,u.prev_sch))) #REPLACE THIS WITH YOUR DYNAMIC ENUMERATED LIST
    dictdata = {}
    for indx in range(len(listdata)):
        singdict = {
            "idenfier": ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)),
            "timedata": timeconv(listdata[indx][0]),
            "buscount": listdata[indx][1],
        }
        dictdata[indx] = singdict
    print(dictdata)
    return dictdata


if __name__ == "__main__":
    main.run(port=9696, host="0.0.0.0")