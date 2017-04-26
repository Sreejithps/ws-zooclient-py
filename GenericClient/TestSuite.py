import sys
import yaml
from RESTClient import RESTClient
import json
import os
import uuid

def main():

    #inputcontext = {}
    #inputcontext['city'] = 'bangalore'
    #params = {}
    #params['apikey'] = 'a70a802bce0d8346f2b246f27f6b0c09'
    ##invoke rest client
    #restClient = RESTClient('testconfigurations\\OpenWeathermapbyCityName.yaml', params)
    #inputcontext = {}
    #for inputparam in restClient.GetInputs():
    #    print('{}:'.format(inputparam))
    #    inputcontext[inputparam] = input()
    #res = restClient.ProcessRequest(inputcontext)
    #print(json.dumps(res, indent=4, sort_keys=True))

    #regression suite
    #OpenWeathermapbyCityName - sreejithsreedharanp@gmail.com:Dogbert$123
    inputcontext = {}
    inputcontext['city'] = 'bangalore'
    params = {}
    params['apikey'] = '67884a44bf38278c68df212b44381216'
    restClient = RESTClient('testconfigurations\\OpenWeathermapbyCityName.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= 1:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))

    #Flowdoc-GetFlows
    inputcontext = {}
    params = {}
    params['apikey'] = 'a70a802bce0d8346f2b246f27f6b0c09'
    restClient = RESTClient('testconfigurations\\Flowdoc-GetFlows.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= 0:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))

    #Flowdoc-GetOrganizations
    inputcontext = {}
    params = {}
    params['apikey'] = 'a70a802bce0d8346f2b246f27f6b0c09'
    restClient = RESTClient('testconfigurations\\Flowdoc-GetOrganizations.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= 0:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))


    #Flowdoc-GetFlowsbyID
    inputcontext = {}
    params = {}
    params['apikey'] = 'a70a802bce0d8346f2b246f27f6b0c09'
    inputcontext['flowid'] = '998ec352-33ba-479c-8d29-8f733dd081bb'
    restClient = RESTClient('testconfigurations\\Flowdoc-GetFlowsbyID.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= 1:
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
    restClient = RESTClient('testconfigurations\\Flowdoc-CreateFlow.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= 1:
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

    restClient = RESTClient('testconfigurations\\Flowdoc-UpdateFlow.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= 1:
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

    restClient = RESTClient('testconfigurations\\Flowdoc-SendMessage.yaml', params)
    res = restClient.ProcessRequest(inputcontext)
    if len(res) <= 1:
        print("Failed")
    else:
        print(json.dumps(res, indent=4, sort_keys=True))

    
    pass
    

if __name__ == "__main__":
    sys.exit(int(main() or 0))