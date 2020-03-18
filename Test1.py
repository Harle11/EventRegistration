from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')  #mongodb url
db = client["EventRegistration"]    #Using EventRegistration DB

def addRegistration(lst,event):
    '''
    Inserts a document containing registration details into a collection.
    Parameters accepted:
        1. List -> A list containing registration details and
        2. String -> The name of the event i.e. the collection name
    '''
    coll = db[event]
    docID = getLastID(event)+1
    doc = {'_id':str(docID),'name':lst[0],'contact':[lst[1],lst[2]],'college':lst[3],'USN':lst[4],'paid':False,'ack':'none'}
    coll.insert_one(doc)

def showRegistrations(event):
    '''
    Shows all documents containing registration details in a collection.
    Parameters accepted:
        1. String -> The name of the event i.e. the collection name
    '''
    coll = db[event]
    allreg = coll.find({},{'_id':0,'ack':0,'paid':0})
    for result in allreg:
        contact = [result['contact'][0],result['contact'][1]]
        print("Name: {}\nUSN: {}\nMobile: {}\nEmail: {}\nCollege: {}\n".format(result['name'],result['USN'],contact[0],contact[1],result['college']))

def findRegistration(event,usn):
    '''
    Searches for a document containing registration details in a collection based on a USN.
    Parameters accepted:
        1. String -> The name of the event i.e. the collection name.
        2. String -> The USN of a registered student.
    '''
    coll = db[event]
    result = coll.find_one({'USN':usn},{'_id':0,'ack':0})
    try:
        contact = [result['contact'][0],result['contact'][1]]
        print("Name: {}\nUSN: {}\nMobile: {}\nEmail: {}\nCollege: {}\nPaid: {}".format(result['name'],result['USN'],contact[0],contact[1],result['college'],result['paid']))
    except:
        print("USN does not match any registered student")

def acceptInput():  #only for testing purpose without GUI
    name = input('Enter name: ')
    USN = input('Enter USN: ')
    mobile = input('Enter Mobile number: ')
    email = input('Enter email ID: ')
    college = input('Enter college initials: ')
    reg = [name,mobile,email,college,USN]
    return reg

def getLastID(event):
    '''
    Gets the _id of the last document in the collection.
    Parameters accepted:
        1. String -> The name of the event i.e. the collection name.
        returns ID as integer object
    '''
    coll = db[event]
    result = coll.find({},{'_id':1}).sort("_id",-1).limit(1)
    docID = 0
    for x in result:
        docID = int(x['_id'])
    return docID