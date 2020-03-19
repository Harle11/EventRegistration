from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')  #mongodb url
db = client["EventRegistration"]    #Using EventRegistration DB

def acceptRegistration():  #only for testing purpose without GUI
    name = input('Enter name: ')
    USN = input('Enter USN: ')
    mobile = input('Enter Mobile number: ')
    email = input('Enter email ID: ')
    college = input('Enter college initials: ')
    reg = [name,mobile,email,college,USN]
    return reg

def addRegistration(lst,event):
    '''
    Inserts a document containing registration details into a collection.
    Parameters accepted:
        1. List -> A list containing registration details and
        2. String -> The name of the event i.e. the collection name
    '''
    global db
    coll = db[event]
    docID = getLastID(event)+1
    doc = {'_id':str(docID),'name':lst[0],'contact':[lst[1],lst[2]],'college':lst[3],'USN':lst[4],'paid':False,'ack':'none'}
    coll.insert_one(doc)

def getLastID(event):
    '''
    Gets the _id of the last document in the collection.
    Parameters accepted:
        1. String -> The name of the event i.e. the collection name.
        returns ID as integer object
    '''
    global db
    coll = db[event]
    result = coll.find({},{'_id':1}).sort("_id",-1).limit(1)
    docID = 0
    for x in result:
        docID = int(x['_id'])
    return docID

def findRegistration(event,usn):
    '''
    Searches for a document containing registration details in a collection based on a USN.
    Parameters accepted:
        1. String -> The name of the event i.e. the collection name.
        2. String -> The USN of a registered student.
    '''
    global db
    coll = db[event]
    result = coll.find_one({'USN':usn},{'_id':0,'ack':0})
    try:
        contact = [result['contact'][0],result['contact'][1]]
        print("Name: {}\nUSN: {}\nMobile: {}\nEmail: {}\nCollege: {}\nPaid: {}".format(result['name'],result['USN'],contact[0],contact[1],result['college'],result['paid']))
    except:
        print("USN does not match any registered student")

def markAsPaid(event,usn):
    '''
    Searches for a document containing registration details in a collection based on a USN and marks them as paid.
    Parameters accepted:
        1. String -> The name of the event i.e. the collection name.
        2. String -> The USN of a registered student.
    '''
    global db
    coll = db[event]
    result = coll.find_one({'USN':usn},{'_id':0,'ack':0})
    if result is not None:
        coll.update_one({'USN':usn},{'$set':{'paid':True}})
    else:
        print("USN does not match any registered student")

def showRegistrations(event):
    '''
    Shows all documents containing registration details in a collection.
    Parameters accepted:
        1. String -> The name of the event i.e. the collection name
    '''
    global db
    coll = db[event]
    allreg = coll.find({},{'_id':0,'ack':0})
    for result in allreg:
        contact = [result['contact'][0],result['contact'][1]]
        print("Name: {}\nUSN: {}\nMobile: {}\nEmail: {}\nCollege: {}\nPaid: {}".format(result['name'],result['USN'],contact[0],contact[1],result['college'],result['paid']))

def acceptEvent(): #only for testing purpose without GUI
    name = input('Enter event name: ')
    etype = input('Enter event type: ')
    fee = input('Enter registration fees: ')
    size = input('Enter team size: ')
    date = input('Enter event date: ')
    time = input('Enter event time: ')
    venue = input('Enter event venue: ')
    prizes = input('Enter event 1st, 2nd and 3rd prizes separated by a space: ').split()
    desc = input('Enter event description: ')
    rules = input('Enter event rules(each rule separated by "#"): ').split('#')
    cords = input('Enter event coordinators names and numbers(all separated by "#"): ').split('#')
    event = [name,etype,fee,size,date,time,venue,prizes,desc,rules,cords]
    return event

def addEvent(lst):
    '''
    Inserts a document containing event details into a collection.
    Parameters accepted:
        1. List -> A list containing event details
    '''
    global db
    coll = db['eventList']
    doc = {'name':lst[0],'type':lst[1],'regFees':lst[2],'teamSize':lst[3],'date':lst[4],'time':lst[5],'venue':lst[6],'prizes':lst[7],'desc':lst[8],'rules':lst[9],'coordinators':lst[10]}
    coll.insert_one(doc)

def editEvent(event):
    '''
    Edits event details
    Parameters accepted: 
        1. String -> Name of event
    '''
    global db
    coll = db['eventList']
    check = coll.find_one({'name':event})
    if check is not None:
        lst = acceptEvent() #Change once GUI comes
        doc = {'name':lst[0],'type':lst[1],'regFees':lst[2],'teamSize':lst[3],'date':lst[4],'time':lst[5],'venue':lst[6],'prizes':lst[7],'desc':lst[8],'rules':lst[9],'coordinators':lst[10]}
        coll.update_one({'name':event},{'$set':doc})
        print('Successfully updated')
    else:
        print('No such event Exists')

def eventList():
    '''
    Displays all events
    '''
    global db
    coll = db['eventList']
    allevents = coll.find({},{'_id':0})
    for event in allevents:
        rule = []
        coordinators = []
        for r in event['rules']:
            rule.append(r)
        for c in event['coordinators']:
            coordinators.append(c)
        print('Event name: {}\nEvent type: {}\nEvent desc: {}\nEvent rules:'.format(event['name'],event['type'],event['desc']))
        for i in range(len(rule)):
            print('{}. {}'.format(i+1,rule[i]))
        print('Size of team: {}\nRegistration Fees: {}\nPrizes: '.format(event['teamSize'],event['regFees']),end='')
        for prize in event['prizes']:
            print(prize,end=' ')
        print('\nEvent date: {}\nEvent time: {}\nEvent venue: {}\nEvent Coordinators:'.format(event['date'],event['time'],event['venue']))
        for i in range(0,len(coordinators),2):
            print('Name: {}\tNumber: {}'.format(coordinators[i],coordinators[i+1]))
        print()

def eventDetails(event):
    '''
    Displays all details w.r.t an event
    Parameters accepted: 
        1. String -> Name of event
    '''
    global db
    coll = db['eventList']
    event = coll.find_one({'name':event},{'_id':0})
    if event is not None:
        rule = []
        coordinators = []
        for r in event['rules']:
            rule.append(r)
        for c in event['coordinators']:
            coordinators.append(c)
        print('Event name: {}\nEvent type: {}\nEvent desc: {}\nEvent rules:'.format(event['name'],event['type'],event['desc']))
        for i in range(len(rule)):
            print('{}. {}'.format(i+1,rule[i]))
        print('Size of team: {}\nRegistration Fees: {}\nPrizes: '.format(event['teamSize'],event['regFees']),end='')
        for prize in event['prizes']:
            print(prize,end=' ')
        print('\nEvent date: {}\nEvent time: {}\nEvent venue: {}\nEvent Coordinators:'.format(event['date'],event['time'],event['venue']))
        for i in range(0,len(coordinators),2):
            print('Name: {}\tNumber: {}'.format(coordinators[i],coordinators[i+1]))
    else:
        print('No such event Exists')
