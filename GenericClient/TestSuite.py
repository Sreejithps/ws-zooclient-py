import sys
import yaml
from RESTClient import RESTClient
import json
import os
import uuid

def main():

    #regression suite

    #foursquare
    #FourSquare-VenueSearch
    CLIENT_ID = 'BEK1M1DDQREKZZPIG3MJLCEUFDX3XO5E2MU2E1F1MMVOOOWG'
    CLIENT_SECRET = 'NFT5QFWMX1RULZGVWQONA0XJMQOEF4XTTVCANHDLMLFPM0QF'
    inputcontext = {}
    inputcontext['locationname'] = 'Trivandrum'
    inputlen = len(inputcontext)
    params = {}
    params['clientid']= CLIENT_ID
    params['clientsecret'] = CLIENT_SECRET
    restClient = RESTClient('testconfigurations\\FourSquare-VenueSearch.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= inputlen:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))


    #google books
    #GoogleBooks-GenericQuery
    inputcontext = {}
    inputcontext['query'] = 'hellen keller'
    inputlen = len(inputcontext)
    params = {}
    params['apikey'] = 'AIzaSyB4xSa6S92WOlxMACXphGUXpPrcrhi09RM'
    restClient = RESTClient('testconfigurations\\GoogleBooks-GenericQuery.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= inputlen:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))
    #GooglePlus-PublicProfileQuery
    inputcontext = {}
    inputcontext['query'] = 'sreejith p s'
    params = {}
    params['apikey'] = 'AIzaSyB4xSa6S92WOlxMACXphGUXpPrcrhi09RM'
    inputlen = len(inputcontext)
    restClient = RESTClient('testconfigurations\\GooglePlus-PublicProfileQuery.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= inputlen:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))

    #OpenWeathermapbyCityName - sreejithsreedharanp@gmail.com:Dogbert$123
    inputcontext = {}
    inputcontext['city'] = 'bangalore'
    params = {}
    params['apikey'] = '67884a44bf38278c68df212b44381216'
    inputlen = len(inputcontext)
    restClient = RESTClient('testconfigurations\\OpenWeathermapbyCityName.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= inputlen:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))

    #Flowdoc-GetFlows
    inputcontext = {}
    params = {}
    params['apikey'] = 'a70a802bce0d8346f2b246f27f6b0c09'
    inputlen = len(inputcontext)
    restClient = RESTClient('testconfigurations\\Flowdoc-GetFlows.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= inputlen:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))

    #Flowdoc-GetOrganizations
    inputcontext = {}
    params = {}
    params['apikey'] = 'a70a802bce0d8346f2b246f27f6b0c09'
    inputlen = len(inputcontext)
    restClient = RESTClient('testconfigurations\\Flowdoc-GetOrganizations.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= inputlen:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))


    #Flowdoc-GetFlowsbyID
    inputcontext = {}
    params = {}
    params['apikey'] = 'a70a802bce0d8346f2b246f27f6b0c09'
    inputcontext['flowid'] = '998ec352-33ba-479c-8d29-8f733dd081bb'
    inputlen = len(inputcontext)
    restClient = RESTClient('testconfigurations\\Flowdoc-GetFlowsbyID.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= inputlen:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))

    #Flowdoc-CreateFlow
    flowname = ''
    inputcontext = {}
    params = {}
    params['apikey'] = 'a70a802bce0d8346f2b246f27f6b0c09'
    inputcontext['organization'] = 'sreejith-sreedharan'
    inputcontext['flowname'] = str(uuid.uuid4())
    flowname = inputcontext['flowname']
    inputlen = len(inputcontext)
    restClient = RESTClient('testconfigurations\\Flowdoc-CreateFlow.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= inputlen:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))

    #Flowdoc-UpdateFlow
    inputcontext = {}
    params = {}
    params['apikey'] = 'a70a802bce0d8346f2b246f27f6b0c09'
    inputcontext['organization'] = 'sreejith-sreedharan'
    inputcontext['oldflowname'] = flowname
    inputcontext['newflowname'] = 'new' + flowname
    inputcontext['disabled'] = False
    inputcontext['open'] = False
    inputcontext['access_mode'] = 'organization'
    inputlen = len(inputcontext)
    restClient = RESTClient('testconfigurations\\Flowdoc-UpdateFlow.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= inputlen:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))

    #Flowdoc-SendMessage
    inputcontext = {}
    params = {}
    params['apikey'] = 'a70a802bce0d8346f2b246f27f6b0c09'
    inputcontext['organization'] = 'sreejith-sreedharan'
    inputcontext['flowname'] = flowname
    inputcontext['event'] = 'message'
    inputcontext['content'] = str(uuid.uuid4())
    inputlen = len(inputcontext)
    restClient = RESTClient('testconfigurations\\Flowdoc-SendMessage.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= inputlen:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))

    #Flowdoc-GetLatestMessage
    inputcontext = {}
    params = {}
    params['apikey'] = 'a70a802bce0d8346f2b246f27f6b0c09'
    inputcontext['organization'] = 'sreejith-sreedharan'
    inputcontext['flowname'] = flowname
    inputlen = len(inputcontext)
    restClient = RESTClient('testconfigurations\\Flowdoc-GetLatestMessage.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= inputlen:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))


    
    pass
    

if __name__ == "__main__":
    sys.exit(int(main() or 0))