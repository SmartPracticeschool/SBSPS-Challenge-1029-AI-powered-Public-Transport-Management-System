from tensorflow.keras.models import load_model
import numpy as np
import pickle

data=[]
prev_sch=None
bus_limit=200

static_model=load_model("model24hrspredict.h5")
dynamic_model=load_model("model2hrspredict(6hrsinput).h5")
static_scaler=pickle.load(open("scalernew.pkl",'rb'))
dynamic_scaler=pickle.load(open("scaler6hrswala.pkl",'rb'))


def schedule(prediction):
    sch=[]
    for i,j in enumerate(prediction):
        print(f"{int(round(j[0]/bus_limit))} AT {str(i).zfill(2)}:00")
        sch.append([int(round(j[0]/bus_limit)),i])
    return sch


def special_events(prediction):
    start=prediction['START']
    stop=prediction['STOP']
    magnitude=prediction['MAGNITUDE']
    prediction['TIMESERIES'][start:stop]=prediction['TIMESERIES'][start:stop]*(1.0+magnitude/100)
    return prediction


def static_time_table(data,special_timeseries=None):
    y_pred=static_model.predict(data)[0]
    if special_timeseries!=None:
        special_timeseries['TIMESERIES']=y_pred[0]
        y_pred=special_events(special_timeseries)['TIMESERIES']
    y_pred=static_scaler.inverse_transform(y_pred.reshape(-1,1))
    number=schedule(y_pred)
    return [number,y_pred]


def normalizer(lenght,mu,sigma,max_val=20):
    "Using standard distribution to increase the value in HSV"
    temp=np.arange(0,lenght)
    temp=np.exp( - (temp - mu)**2 / (2 * sigma**2) )/(sigma * np.sqrt(2 * np.pi))
    slope=max_val/(max(temp)-min(temp))
    intercept=max_val-(max(temp)*max_val/(max(temp)-min(temp)))
    temp=temp*slope+intercept
    return temp


def dynamic_changes(data,sch,start_time):
    pred=dynamic_model.predict(data)[0]
    pred=schedule(dynamic_scaler.inverse_transform(pred.reshape(-1,1)))
    #temp=sch[start_time:start_time+2]
    sch[start_time:start_time+2]=list(map(lambda x:x[0],pred))
    return sch


def get_static_timetable():
    global data,prev_sch
    norm=normalizer(24,12,8,0.6)
    rand=np.random.random_sample(24)/5
    norm+=rand
    data+=list(norm)
    sch,pred=static_time_table(np.asarray(data[-24:]).reshape(1,-1,1))
    prev_sch=sch
    return sch


def get_dynamic_timetable(start_time,prev_sch):
    sch=dynamic_changes(
        np.asarray(data[-24-6+start_time:-24+start_time]).reshape(1,-1,1),
        list(map(lambda x:x[0],prev_sch)),
        start_time)
    return sch

