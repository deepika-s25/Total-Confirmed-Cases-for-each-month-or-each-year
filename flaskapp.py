from flask import Flask, jsonify
import requests
from requests.api import patch


app=Flask(__name__)



@app.route('/positive_cases',methods=['GET'])
def index():
    df = requests.get('https://api.rootnet.in/covid19-in/stats/testing/raw')
    return df.json()

@app.route('/positive_cases/monthly',methods=['GET'])
def hello():
    summ=0
    monthyr=[]
    datadict={}

    df = requests.get('https://api.rootnet.in/covid19-in/stats/testing/raw').json()

  
    for covid_daily_data in df["data"]:
        month = covid_daily_data["timestamp"][:7]
        samples = covid_daily_data["totalSamplesTested"]
        if month not in datadict:
            datadict[month]=0
        if samples is not None:
            datadict[month] += samples
    
    
    final_monthly_result=[]
    for i in datadict:
        final_dict={}
        final_dict['month']=i
        final_dict['confirmed_cases_count']=datadict[i]
        final_monthly_result.append(final_dict)

    
    return jsonify(final_monthly_result)

@app.route('/positive_cases/yearly',methods=['GET'])
def yearly():
    datadict={}
    df = requests.get('https://api.rootnet.in/covid19-in/stats/testing/raw').json()

  
    for covid_daily_data in df["data"]:
        year = covid_daily_data["timestamp"][:4]
        samples = covid_daily_data["totalSamplesTested"]
        if year not in datadict:
            datadict[year]=0
        if samples is not None:
            datadict[year] += samples
    
    
    final_yearly_result=[]
    for i in datadict:
        final_dict={}
        final_dict['year']=i
        final_dict['confirmed_cases_count']=datadict[i]
        final_yearly_result.append(final_dict)

    
    return jsonify(final_yearly_result)





if __name__=="__main__":
    app.run(debug=True)
    