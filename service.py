import urllib2
import json
import sys
#from pprint import pprint
query = "http://52.200.214.141:8080/fhir/baseDstu3/" #API link
encounter = [] #holds Encounter data
encounter.append([])
condition = [] 
patient = [] # holds patients data
'''
API connectivity tester
'''
def callAPI(firstName,lastName):
    #get Named response
    name = lastName
    if name == None:
        name = firstName
    if name == None:
        name = ""
        return 0 #empty name is invalid query so exit abruptly
    patient = getNameResponse("Patient?name="+name)
    print(patient)# get encounter details
    returnVal=[]
    encounter = []
    if patient != 0 :
        print(len(patient))
        print(patient[0])
        for i in range(0, len(patient)-1):
            if name == patient[i][5] and firstName == patient[i][6]:
                encounter = getEncounter("Encounter?patient:reference=Patient/"+patient[i][0])
                print(encounter)# call Encounter API
                if encounter !=0 :
                    returnVal.append(patient[i])
                    returnVal.append(encounter)
                    break #we found patient we are looking for
            else:
                continue
        if encounter==[]:
            return 0 # no records found		
        #returnVal.append(patient[i])
        #returnVal.append(encounter)
        print(len(encounter[0])-1)
        for i in range(0, len(encounter[0])-1,5):
            if(i+5<=len(encounter[0])-1):
                if i == 0 :
                    con = getCondition("Condition?patient:reference=Patient/"+returnVal[0][0]+"&encounter:reference=Encounter/"+encounter[0][4])
                else:
                    con = getCondition("Condition?patient:reference=Patient/"+returnVal[0][0]+"&encounter:reference=Encounter/"+encounter[0][i+4])				
                print(con)
                if con != 0:
		           condition.append(con)
                else:
                   condition.append("No issue")
        print(condition)
        print(returnVal)
        returnVal.append(condition)
        print(returnVal)
        return returnVal
    else:
        return 0
'''
Call NJII API to get Patient record for Patient which is refered using name
'''
def getNameResponse(name):
    # call API for name
    response=[]
    data=[]
    try :
        response = urllib2.urlopen(query+name)
    except:
        print("url error")
        return 0 #Url is closed so close the APP 
	# save Address
    # identifier
    try : 
        data = json.load(response)
    except AttributeError:
        print("Attribute Error")
        return 0
    patient = []
    #print(data)
    if data != [] : 
        try:
            x = []
#            print(data["entry"])
            print(data["entry"][5]["resource"]["id"])
            print(data["entry"][5]["resource"]["telecom"][0]["value"])
            print(data["entry"][5]["resource"]["gender"])
            print(data["entry"][5]["resource"]["birthDate"])
            print(data["entry"][5]["resource"]["address"][0]["line"][0]+ ", "+data["entry"][0]["resource"]["address"][0]["city"] +data["entry"][0]["resource"]["address"][0]["state"] +", "+data["entry"][0]["resource"]["address"][0]["postalCode"])
            print(data["entry"][0]["resource"]["name"][0]["family"]) # family name
            print(data["entry"][0]["resource"]["name"][0]["given"][0]) #first Name
            for i in range(0, len(data["entry"] )-1):
                x = []
                x.append(data["entry"][i]["resource"]["id"])
                x.append(data["entry"][i]["resource"]["telecom"][0]["value"])
                x.append(data["entry"][i]["resource"]["gender"])
                x.append(data["entry"][i]["resource"]["birthDate"])
                x.append(data["entry"][i]["resource"]["address"][0]["line"][0]+ ", "+data["entry"][i]["resource"]["address"][0]["city"] +data["entry"][i]["resource"]["address"][0]["state"] +", "+data["entry"][i]["resource"]["address"][0]["postalCode"])
                x.append(data["entry"][i]["resource"]["name"][0]["family"]) # family name
                x.append(data["entry"][i]["resource"]["name"][0]["given"][0]) #first Name
                print("----------------------------------------------")
                print(len(x))
                print("----------------------------------------------")
                patient.append(x)
                print(patient)
            return patient
        except :
            return 0
    return 0
'''
Call NJII API to get Encounter record for Patient which is refered using referenceID
'''
def getEncounter(referenceID):
    #call API for encounter
    response = []
    data = []
    try :
        response = urllib2.urlopen(query+referenceID)
    except:
        print("URl error")
        print(sys.exc_info()[0])
        return 0 #Url is closed so close the APP 
    # save Address
    # identifier
    try : 
        data = json.load(response)
    except AttributeError:
        print("response is empty")	
        return 0
    print(data)
    if data != [] :
        encounter = []
        encounter.append([])
        try:
            for i in  range(0,len(data["entry"])):
                encounter[0].append(data["entry"][i]["resource"]["type"][0]["coding"][0]["display"]) #reason of visit
                encounter[0].append(data["entry"][i]["resource"]["participant"][0]["period"]["start"]) #date of visit
                encounter[0].append(data["entry"][i]["resource"]["participant"][0]["individual"]["display"]) #doctor
                encounter[0].append(data["entry"][i]["resource"]["serviceProvider"]["display"]) # service provider
                encounter[0].append(data["entry"][i]["resource"]["id"]) # service provider			
        #print(encounter)
            return encounter
        except:
            return 0 #No data available for that person  
    return 0

'''
Call NJII API to get Condition record for Patient which is refered using referenceID, encounter ID
'''	
def getCondition(ID):
    #call API for encounter
    response = []
    data = []
    print(ID)
    try :
        response = urllib2.urlopen(query+ID)
    except:
        print("URl error")
        print(sys.exc_info()[0])
        return 0 #Url is closed so close the APP 
    # save Address
    # identifier
    try : 
        data = json.load(response)
    except AttributeError:
        print("response is empty")	
        return 0

    if data != [] :
        
        #for i in  range(0,len(data["entry"])):
        try:
            return data["entry"][0]["resource"]["code"]["coding"][0]["display"] #condition of patient
        except:
            return "No issues"
        #print(encounter)
        
    return 0

	
def getDiet(conditions):
    opening = "Your Diet Should include"
    str = ""
    condition = list(set(conditions))
    for i in range(0, len(condition)):
        if "diabetes" in condition[i].lower():
            str += "Diabetes : Lite bite, Salads, leafy Vegetables. \nAvoid To much sweet, soda, alcohol, starchy and oily food\n"
        if "sinusitis" in condition[i].lower():
            str += "Sinusitis : Foods rich in Vitamin C, Spinach, beets, rich in Vitamin A, like Carrots, purslane, pumpkin\nRich in Vitamin B, E like Rice, Wheat, oats, Olive oil sunflower seeds for Vitamin E.\n"
        if "pharyngitis" in condition[i].lower():
            str += "Pharyngitis : Drinking large amounts of fluid is recommended. No specific dietary restrictions are needed. Soft, cold foods (eg, ice cream, popsicles) are more easily tolerated. \n"
        if "allergic" in condition[i].lower():
            str += "Allergies : Avoid food that causes allergies, everything else you can consume. \n"
        if "burn" in condition[i].lower():
            str += "Burn : Avoid Eating salty Food.\n"
        if "laceration " in condition[i].lower():
            str +="Laceration : Continue consuming the food which you regulary consume.\n"
        if "heart" in condition[i].lower():
            str +="Heart Issues : Avoid oily, spicy and fatty food. Consume green vegetables is good for you, Decrease amount meat per meal. It is good habit to eat oats in heart issues\n"
        if "cold" in condition[i].lower():
            str +="Cold, Fever, Cough: Drink soups, tea or coffee. It'll keep you relaxed. Drink lot of fluid. Avoid Cold milk, Yogurt and Banana.\n"
        if "strain" in condition[i].lower():
            str +="Muscle Strain, Stress :Drink lot of fluids, other than this you can enjoy everything you like\n"
    if str == "":
        opening = "\n"
        str = "You seem absolutely healthy, you don't have to worry about diet!!\n Eat fresh and stay healthy!"
    str = opening + str
    return str        			
	
'''
This method generates out put string which will be printed on html response page
'''
def generateString(response):
    strin = ""
    if response == []:
        return "Empty"
    else:
        print(len(response))
        print(response)
        strin = "PatientID : " + str(response[0][0]) + "\nDate of Birth : "+ str(response[0][3]) + "\nGender : "+ str(response[0] [2])+"\nAddress : "+str(response[0][4])+"\nContact : "+str(response[0][1])+"\n"
        print(strin)
        for i in range(0, len(response[1][0]),5):
            strin += "Reason for Visit : "+str(response[1][0][i])+"\n"
            strin += "Date of Visit : "+str(response[1][0][i+1])+"\n"
            strin += "Doctor : "+str(response[1][0][i+2])+"\n"
            strin += "Service Provider : "+str(response[1][0][i+3])+"\n"
        strin +=getDiet(response[2])
        return strin

'''
this method identifies that API calls are successful or not
If successful store response and pass to caller 
'''
		
def identify(firstName,lastName):
    response = callAPI(firstName,lastName)
    #response = []
    if  response == 0 :
        return 0
    else:
        # create proper response
        print(response)
        for i in range(0, len(response[0])):     		
            response.append(response[0][i])
        #print("printing response which includes patient's info")
        #print(response)
        try:
            for i in range(0, len(encounter[0])-1):
                response.append(encounter[0][i])
        except:
		    print(sys.exc_info()[0])
        response.append(response[2])
        return response

'''
This method is called by server and this acts as caller and service provider for server
calls identify to check API are responding and then genrate Response
'''
def generateResponse(firstName,lastName):
    response = identify(firstName,lastName)
    print(response)
    if response == 0:
        # general response
        return "Record Not Found"
    else:
        return generateString(response)
'''
If ran as standalone then check API connectivity by calling callAPI
'''
if __name__ == "__main__":
	callAPI("Jude","Law")