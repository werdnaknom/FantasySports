from requests import post, get
from random import randint, seed
import forgery_py
from collections import namedtuple

def checkResponse(resp):
    print(resp.status_code, resp.json())

def getFromServer(url):
    r = get(url=url)
    checkResponse(r)
    return r.json()

def postToServer(url, json_data):
    r = post(url=url, json=json_data)
    checkResponse(r)
    return r.json()

def getSample(baseurl, id):
    final_url = "{}api/sample/{}".format(baseurl, id)
    dataDict = getFromServer(final_url)
    return dataDict['id']

def getHwRev(baseurl, id):
    final_url = "{}api/hardwarerevision/{}".format(baseurl, id)
    dataDict = getFromServer(final_url)
    return dataDict['id']

def getTest(url, id):
    final_url = "{}api/test/{}".format(baseurl, id)
    dataDict = getFromServer(final_url)
    return dataDict['id']

def postTestID(url, test_id, hwrev_id, sample_id):
    final_url = "{}api/testid".format(baseurl)
    json_data = {
        'test_id' : test_id,
        'hardware_revision_id' : hwrev_id,
        'sample_id' : sample_id
    }
    dataDict = postToServer(final_url, json_data)
    return dataDict

def postTestRow(url, testid_id):
    final_url = "{}api/testrow".format(baseurl)
    json_data = {
        'test_id' : test_id,
    }
    dataDict = postToServer(final_url, json_data)
    return dataDict

def postTestData(url, testrow_id, value, attribute, datatype):
    final_url = "{}api/testdata".format(baseurl)
    json_data = {
        'testrow_id' : test_id,
        'value' : value,
        'attribute' : attribute,
        'datatype' : datatype
    }
    dataDict = postToServer(final_url, json_data)
    return dataDict

def create_sample(url, product_id, serial, hardware_revision_id):
    final_url = "{}api/sample/".format(url)
    json_data = {
        "product_id" : product_id,
        "serial" : serial,
        "hardware_revision_id" : hardware_revision_id,
    }
    dataDict = postToServer(final_url, json_data)
    return dataDict


if __name__ == "__main__":
    seed()
    #Grab a product
    #p = Product.query.first()

    #Create a sample
    sample_json = create_sample(baseurl, product_id = 1,
                                serial = "12345",
                                hardware_revision_id = 3)

    test_id = getTest(baseurl, 10)

    testid = postTestID(url=baseurl, test_id=test_id,
                        hwrev_id = hwrev_id,
                        sample_id = sample_id)
    testid_id = testid['id']

    testrow_id = postTestRow(url=baseurl, testid_id = testid_id)






    '''
    baseurl = "http://127.0.0.1:5000/"
    #Get Sample from server
    sample_id = getSample(baseurl, 101)

    test_id = getTest(baseurl, 10)

    testid = postTestID(url=baseurl, test_id=test_id,
                        hwrev_id = hwrev_id,
                        sample_id = sample_id)
    testid_id = testid['id']

    attributes = []
    for _ in range(0,50):
        attributes.append(forgery_py.address.street_name())

    seed()
    for row in range(0,randint(0,1000)):
        testrow_id = postTestRow(url=baseurl, testid_id = testid_id)
        row_id = testrow_id['id']
        for i in range(0, 50):
            value = randint(0,100000)
            attribute = attributes[i]
            datatype = type(value).__name__
            testdata = postTestData(url = baseurl,
                                    testrow_id = testrow_id,
                                    value = value,
                                    attribute = attribute,
                                    datatype = datatype)
    '''














