from flask import Flask , jsonify , request
import pickle
import pandas as pd
import numpy as np
import getpass
import mysql.connector as sql

app = Flask(__name__)

pw = getpass.getpass('Enter your Password :')

mydb = sql.connect(host = 'localhost',
                   user = 'root',
                   passwd = pw,
                   use_pure=True)


print(mydb)

mycursor = mydb.cursor()

DT_model = pickle.load(open('dt_model.pkl','rb'))
# print('We have imported the model successfully')

@app.route('/')
def main():
    return jsonify({'Message from the system':'Loan Model Activated'})

# APPLICATION_ID,
# QUEUE_ID,
# CURRENT_STAGE,
# MARITAL_STATUS,
# GENDER,
# AGE,
# EDUCATION,
# RESIDENCE_TYPE,
# EMPLOY_CONSTITUTION,
# PAN_STATUS,
# CIBIL_SCORE,
# APPLICATION_SCORE,
# RESIDENTIAL_ADDRESS_SCORE,
# OFFICE_ADDRESS_SCORE,
# LOAN_TENOR,
# PRIMARY_ASSET_CTG,
# VOTER_ID,
# DRIVING_LICENSE,
# AADHAAR,
# PAN,
# BANK_PASSBOOK,
# APPLIED_AMOUNT_TRANS
@app.route('/Loan_approval_system',methods = ['POST','GET'])
def loan_approval_prediction():
    global data 
    data = request.get_json()
    print()
    print('data is :',data)
    print()
    APPLICATION_ID = data['APPLICATION_ID']
    print(APPLICATION_ID)
    QUEUE_ID= data['QUEUE_ID']
    print(QUEUE_ID)
    CURRENT_STAGE= data['CURRENT_STAGE']
    print(CURRENT_STAGE)
    MARITAL_STATUS= data['MARITAL_STATUS']
    print(MARITAL_STATUS)
    GENDER= data['GENDER']
    print(GENDER)
    AGE= data['AGE']
    print(AGE)
    EDUCATION= data['EDUCATION']
    print(EDUCATION)
    RESIDENCE_TYPE= data['RESIDENCE_TYPE']
    print(RESIDENCE_TYPE)
    EMPLOY_CONSTITUTION= data['EMPLOY_CONSTITUTION']
    print(EMPLOY_CONSTITUTION)
    PAN_STATUS= data['PAN_STATUS']
    print(PAN_STATUS)
    CIBIL_SCORE= data['CIBIL_SCORE']
    print(CIBIL_SCORE)
    APPLICATION_SCORE= data['APPLICATION_SCORE']
    print(APPLICATION_SCORE)
    RESIDENTIAL_ADDRESS_SCORE= data['RESIDENTIAL_ADDRESS_SCORE']
    print(RESIDENTIAL_ADDRESS_SCORE)
    OFFICE_ADDRESS_SCORE= data['OFFICE_ADDRESS_SCORE']
    print(OFFICE_ADDRESS_SCORE)
    LOAN_TENOR= data['LOAN_TENOR']
    print(LOAN_TENOR)
    PRIMARY_ASSET_CTG= data['PRIMARY_ASSET_CTG']
    print(PRIMARY_ASSET_CTG)
    VOTER_ID= data['VOTER_ID']
    print(VOTER_ID)
    DRIVING_LICENSE= data['DRIVING_LICENSE']
    print(DRIVING_LICENSE)
    AADHAAR= data['AADHAAR']
    print(AADHAAR)
    PAN= data['PAN']
    print(PAN)
    BANK_PASSBOOK= data['BANK_PASSBOOK']
    print(BANK_PASSBOOK)
    APPLIED_AMOUNT_TRANS= data['APPLIED_AMOUNT_TRANS']
    print(APPLIED_AMOUNT_TRANS)
    
    print()

    str1 = 'DATA SUCCESSFULLY FETCHED'
    print(str1.center(100,'*'))

    list1 = list(data.keys())
    dict2={}
    c = 0
    for i in data.values():
        print(i)
        dict2[list1[c]]=np.array(list(data.values())[c],ndmin=1)
        c=c+1

    print(dict2)


    print('UPTO Dict2')


    input = pd.DataFrame(dict2).drop('APPLICATION_ID',axis = 1)
    print('Test point created'.center(100,'*'),end='\n')

    prediction = DT_model.predict(input)
    print('MODEL RESULT'.center(100,'*'))
    print()

    print(f'LOAN STATUS for {APPLICATION_ID} IS :',prediction[0])

    print()

    print('MODEL RAN SUCCESSFULLY'.center(100,'*'))

    insert_query = ("""INSERT INTO datalab_bank.latest_lending_data_2023(APPLICATION_ID,
    QUEUE_ID,
    CURRENT_STAGE,
    MARITAL_STATUS,
    GENDER,
    AGE,
    EDUCATION,
    RESIDENCE_TYPE,
    EMPLOY_CONSTITUTION,
    PAN_STATUS,
    CIBIL_SCORE,
    APPLICATION_SCORE,
    RESIDENTIAL_ADDRESS_SCORE,
    OFFICE_ADDRESS_SCORE,
    LOAN_TENOR,
    PRIMARY_ASSET_CTG,
    VOTER_ID,
    DRIVING_LICENSE,
    AADHAAR,
    PAN,
    BANK_PASSBOOK,
    APPLIED_AMOUNT_TRANS
    )

    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            
    )

    data1 = (APPLICATION_ID,
    QUEUE_ID,
    CURRENT_STAGE,
    MARITAL_STATUS,
    GENDER,
    AGE,
    EDUCATION,
    RESIDENCE_TYPE,
    EMPLOY_CONSTITUTION,
    PAN_STATUS,
    CIBIL_SCORE,
    APPLICATION_SCORE,
    RESIDENTIAL_ADDRESS_SCORE,
    OFFICE_ADDRESS_SCORE,
    LOAN_TENOR,
    PRIMARY_ASSET_CTG,
    VOTER_ID,
    DRIVING_LICENSE,
    AADHAAR,
    PAN,
    BANK_PASSBOOK,
    APPLIED_AMOUNT_TRANS)

    try:
        mycursor.execute(insert_query,data1)
        mydb.commit()
        print('we are in try block')
        print('Data entered successfully into the Database'.center(100,'*'))

        
    except:
        mydb.rollback()
        print('we are in except block')
        print('Data did not enter successfully into the Database'.center(100,'*'))


    print()

    return jsonify({'APPROVAL STATUS :':prediction[0]})

print('API IS SUCCESSFULLY EXECUTED')

if __name__ == '__main__':
    app.run(debug=True)