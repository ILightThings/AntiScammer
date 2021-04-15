import requests
import json
import random
import string

def randomNum():
    return str(random.randint(100000000,999999999))

def randomSession():
    return ''.join(random.choice(string.ascii_letters) for i in range(60))

attempt = 0
while True:
    print(f'Attempt Number: {attempt}')
    cc = '5100000010001004'
    ss = randomNum()
    url = "&pageID="+randomSession() # Generate fake pageID - backend does not check for validity
    newPerson = json.loads(requests.get('https://randomuser.me/api/?nat=ca&inc=person,name,location,phone,dob').text) #Get fake person data via api
    middlename = json.loads(requests.get('https://randomuser.me/api/?nat=ca&inc=name').text)['results'][0]['name']['last'] # Get a fake middle name
    persondata = newPerson['results'][0]
    
    
    postPerson = {
        'ship_date':'0',
        'fn':f"{persondata['name']['first']} {persondata['name']['last']}",
        'add':f"{persondata['location']['street']['number']} {persondata['location']['street']['name']}",
        'cty':persondata['location']['city'],
        'prv':f"{persondata['location']['state']}",
        'postcode':persondata['location']['postcode'],
        'mnum':persondata['phone'],
        'db3':persondata['dob']['date'][0:4],
        'db2':persondata['dob']['date'][5:7],
        'db1':persondata['dob']['date'][8:10],
        'ssn':ss
                   }
    
    postCard = {
        'ship_date':'0',
        'fn':f"{persondata['name']['first']} {persondata['name']['last']}",
        'cnm':cc,
        'ce1':str(random.randint(1,12)).zfill(2),
        'ce2':str(random.randint(2022,2028)),
        'scv':str(random.randint(0,999)).zfill(3),
        'mnm':middlename,
        'bill_same':'on',
        'fn':'',
        'add':'',
        'add2':'',
        'cty':'',
        'prv':'',
        'post':'',
        'mnum':''
    }
    print(f'Person Data:')
    for x in postPerson:
        print(x,postPerson[x])

    s = requests.session()
    rz = s.get('http://officecanadapostaccess.aaadvworkshop.com/') # Get x-ref header from this site to bypass first check, site will redirect.
    print(rz.url)
    print(rz.text)
    print('END\n\n\n')
    
    r0 = s.get('http://www.badsite.notreal/index.php/'+url) # Get PHP Session cookie, bypassing second check.
    print(f"Sending {persondata['name']['first']} {persondata['name']['last']} from {persondata['location']['street']['number']} {persondata['location']['street']['name']} ")
    

    r1 = s.post('http://www.badsite.notreal/Addressupdate/'+url,data=postPerson)
    print(f'Request 1 Status {r1.status_code} ')

    r2 = s.post('http://www.badsite.notreal/Payment/'+url,data=postCard,timeout=2)
    
    print(f'Request 2 Status {r2.status_code} ')
    attempt += 1


