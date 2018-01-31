############################################################
##### Title: Bulk Check and Rent Numbers               #####
##### Author: Olivier Salmon                           #####
##### Date: 24 March 2017                              #####
##### Updated: 9 September 2017                        #####
##### Compatibility: Python 3                          #####
############################################################

import requests
import csv, sys, getopt, datetime, time, math, os



############
# SETTINGS #
############

### API KEY ###
params_keys = {
    'api_key': os.getenv('nexmo_api_key'),
    'api_secret': os.getenv('nexmo_api_secret')
}
#}

### GLOBAL PARAMETERS ###

numberOfWantedNumbers = 10000
amountOfSequentialsNumbers = 28

params_global = {
    'country': 'GB',
    # Possible values for features: SMS - VOICE - VOICE,SMS
    'features': 'VOICE,SMS',
}

numberList = []

###########
# CODE    #
###########

def roundup(x):
    #return int(math.ceil(x / 10.0)) * 10
    return int(math.ceil(x))

def getNumbers(maxPageSize,idx):
    new_params = {
        'size': maxPageSize,
        'index':idx
    }

    #print(idx)

    params = dict(params_keys.items() | new_params.items() | params_global.items())

    try:
        response = requests.get(base_url + action, params=params)
        virtual_numbers = response.json()
        #print(virtual_numbers)
        for number in virtual_numbers['numbers']:
            #print(number)
            #print(number['msisdn'])
            numberList.append(number['msisdn'])
            if len(numberList) > 1 and len(numberList) < amountOfSequentialsNumbers:
                beforeLastNum = int(numberList[-2])
                lastNum = int(number['msisdn'])
                seqNum = lastNum - beforeLastNum
                #print(idx," ",beforeLastNum, " " , lastNum, " " , seqNum )
                if seqNum != 1:
                    numberList.clear()
            if len(numberList) == amountOfSequentialsNumbers:
                print(numberList)
                print(len(numberList))
                break
            country = number['country']
            msisdn = number['msisdn']
            #buyNumbers(country,msisdn)

    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)



def buyNumbers(country,msisdn):
    action = '/number/buy?'

    new_params_buy = {
        'country': country,
        'msisdn': msisdn
    }

    params_buy = dict(params_keys.items() | new_params_buy.items())

    try:
        print (base_url + action + str(dict(params_buy)))
        #response = requests.post(base_url + action, params=params_buy)
        decoded_response = response.json()
        if decoded_response['error-code'] == '200':
            print(msisdn + ' has been rented successfully')

    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

bigLoop = roundup (numberOfWantedNumbers/100)
smallLoop = numberOfWantedNumbers - ((bigLoop - 1) * 100)
#print(bigLoop)
#print(smallLoop)

base_url = 'https://rest.nexmo.com'
version = ''
action = '/number/search?'

if ((bigLoop-1) == 0):
    getNumbers(smallLoop)
else:
    for x in range(1, bigLoop):
        getNumbers(100,x)
    getNumbers(smallLoop)
