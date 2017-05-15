from GenericClientABC import GenericClientABC
import urllib3
import json
import yaml
from urllib.parse import urlencode, quote
from jsonpath_rw import jsonpath, parse
import base64
import pandas as pd
import os

#httpconnpool = urllib3.PoolManager(num_pools=10, maxsize=30, block=True, timeout = 20.0)
httpconnpool = urllib3.ProxyManager('http://proxy-idp01.ind.hp.com:8080', num_pools=10, maxsize=30, block=True, timeout = 20.0)

class GenericWSClient(metaclass=GenericClientABC):
    """Paramter driven REST client implementation"""
    def __init__(self, settingsdata, params=None):
        if os.path.isfile(settingsdata) == True:
            with open(settingsdata) as settingsfile:
                settings = yaml.safe_load(settingsfile)
        else:
            settings = yaml.safe_load(settingsdata)
        self.settings = settings
        self.params = params
        #validate settings
        if settings['endpoint']['url'] == None or len(settings['endpoint']['url']) == 0:
            raise Exception('Invalid end point URL')
        if settings['endpoint']['method'] not in ['get', 'post', 'put','head', 'delete', 'options']:
            raise Exception('Invalid http method')

    def processrequest(self, inputcontext):
        outputcontext = {}
        try:
            #process input paramteters
            #query string first
            querystring = {}
            headers = {}
            jsondictbody = {}
            url = self.settings['endpoint']['url']
            if 'inputmap' in self.settings:
                for input in self.settings['inputmap']:
                    #check if input value is present
                    defaultinputvalue = None
                    if 'default' in self.settings['inputmap'][input]:
                        defaultinputvalue = self.settings['inputmap'][input]['default']

                    if (input not in inputcontext or inputcontext[input] == None) and defaultinputvalue == None:
                        raise Exception('Input not provided for {} input'.format(input))
                    if input in inputcontext and inputcontext[input] != None:
                        inputvalue = inputcontext[input]
                    else:
                        inputvalue = defaultinputvalue
                    if 'encode' in self.settings['inputmap'][input]:
                        if str(self.settings['inputmap'][input]['encode']).lower() == 'true':
                            #switch on encoding scheme
                            if str(self.settings['inputmap'][input]['encodingscheme']).lower() == 'base64':
                                inputvalue = base64.b64encode(inputcontext[input].encode()).decode('ascii')
                            elif str(self.settings['inputmap'][input]['encodingscheme']).lower() == 'urlencode':
                                if str(self.settings['inputmap'][input]['target']).lower() != 'querystring':
                                    inputvalue = quote(inputcontext[input])
                            else:
                                raise Exception('Unknown encoding scheme for {} input'.format(input))
                        elif str(self.settings['inputmap'][input]['encode']).lower() == 'false':
                            pass
                        else:
                            raise Exception('Unknown encoding switch for {} input'.format(input))

                    if str(self.settings['inputmap'][input]['target']).lower() == 'querystring':
                        querystring[self.settings['inputmap'][input]['querystring']] = inputvalue
                    elif str(self.settings['inputmap'][input]['target']).lower() == 'header':
                        headers[self.settings['inputmap'][input]['headername']] = inputvalue
                    elif str(self.settings['inputmap'][input]['target']).lower() == 'body':
                        if str(self.settings['inputmap'][input]['format']).lower() == 'jsondict':
                            jsondictbody[self.settings['inputmap'][input]['key']] = inputvalue
                        else:
                            raise Exception('Unknown encoding switch for {} input --> body'.format(input))
                    elif str(self.settings['inputmap'][input]['target']).lower() == 'url':
                        url = url.replace(self.settings['inputmap'][input]['urlpart'] , inputvalue)

                    else:
                        raise Exception('Unknown target for inputmap') 


            #process authentication scheme
            apikey = None
            if str(self.settings['authenticationscheme']).lower() == 'apikey':
                #just loop through all keys and assign them to targets
                for key in self.settings['authentication']['keys']:
                    apikeykeyinparams = self.settings['authentication']['keys'][key]['source']
                #check if we need to encode
                    if str(self.settings['authentication']['keys'][key]['encode']).lower() == 'true':
                        #switch on encoding scheme
                        if str(self.settings['authentication']['keys'][key]['encodingscheme']).lower() == 'base64':
                            apikey = base64.b64encode(self.params[apikeykeyinparams].encode()).decode('ascii')
                        elif str(self.settings['authentication']['keys'][key]['encodingscheme']).lower() == 'urlencode':
                            apikey = quote(self.params[apikeykeyinparams])
                        else:
                            raise Exception('Unknown encoding scheme for APIKEY')
                    elif str(self.settings['authentication']['keys'][key]['encode']).lower() == 'false':
                        apikey = self.params[apikeykeyinparams]
                    else:
                        raise Exception('Unknown encoding swtich for APIKEY')

            
                    if str(self.settings['authentication']['keys'][key]['target']).lower() == 'querystring':
                        querystring[self.settings['authentication']['keys'][key]['querystring']] = str(self.settings['authentication']['keys'][key]['value']).format(apikey)
                    elif str(self.settings['authentication']['keys'][key]['target']).lower() == 'header':
                        headers[self.settings['authentication']['keys'][key]['header']] = str(self.settings['authentication']['keys'][key]['value']).format(apikey)
                    else:
                        raise Exception('Unknown target for APIKEY')

            encodedquerystring = ''
            if len(querystring) > 0:
                encodedquerystring = urlencode(querystring)
                if '?' not in url:
                    url = url + '?' + encodedquerystring
                else:
                    url = url + '&' + encodedquerystring
            body=None
            if len(jsondictbody) > 0:
                body = json.dumps(jsondictbody)

            #add heades
            if 'headers' in self.settings['endpoint']:
                for header in self.settings['endpoint']['headers']:
                    headers[header] = self.settings['endpoint']['headers'][header]

            response = httpconnpool.urlopen(self.settings['endpoint']['method'].upper(), url, headers=headers, body=body)
            if response.status < 200 or response.status > 299:
                return outputcontext

            #extract items from outputcontext which can be directly extracted
            if 'outputmap' in self.settings:
                for output in self.settings['outputmap']:
                    data = None
                    if str(self.settings['outputmap'][output]['source']).lower() == 'body':
                        data = response.data
                    elif str(self.settings['outputmap'][output]['source']).lower() == 'header':
                        data = response.headers[self.settings['outputmap']['direct'][output]['header']]
                    else:
                        raise Exception('Unsupported output source')

                    if str(self.settings['outputmap'][output]['transform']).lower() == 'none':
                        if str(self.settings['outputmap'][output]['type']).lower() == 'json':
                            outputcontext[output] = [match.value for match in parse(self.settings['outputmap'][output]['value']).find(json.loads(data.decode('utf-8')))]
                        elif self.settings['outputmap'][output]['type'] == 'xml':
                            raise Exception('XML support not implemented yet')
                        else:
                            raise Exception('Unsupported output type')
                    elif str(self.settings['outputmap'][output]['transform']).lower() == 'strfmt':
                        if str(self.settings['outputmap'][output]['type']).lower() == 'json':
                            formatargs = []
                            for formatargquery in self.settings['outputmap'][output]['value']:
                                formatargs.append([match.value for match in parse(formatargquery).find(json.loads(data.decode('utf-8')))])
                            outputcontext[output] = []
                            for x in zip(*formatargs):
                                outputcontext[output].append(self.settings['outputmap'][output]['format'].format(*x))
                        elif self.settings['outputmap'][output]['type'] == 'xml':
                            raise Exception('XML support not implemented yet')
                        else:
                            raise Exception('Unsupported output type')
                    else:
                        raise Exception('Unsupported transform type')
                    #map to single value 
                    if len(outputcontext[output]) == 1:
                        outputcontext[output] = outputcontext[output][0]
            return outputcontext
        except Exception as e:
            return outputcontext


    def getinputs(self):
        inputs = {}
        try:
            for inputparam in self.settings['inputmap']:
                if 'default' not in self.settings['inputmap'][inputparam]:
                    defaultvalue = None
                else:
                    defaultvalue = self.settings['inputmap'][inputparam]['default']
                inputs[inputparam] = {'description': self.settings['inputmap'][inputparam]['description'] if 'description' in self.settings['inputmap'][inputparam] else None, 'default': defaultvalue}
        except Exception as e:
            pass
        return inputs

    def getoutputs(self):
        outputs = {}
        try:
            for outputparam in self.settings['outputmap']:
                outputs[outputparam] = {'description': self.settings['outputmap'][outputparam]['description'] if 'description' in self.settings['outputmap'][outputparam] else None}
        except Exception as e:
            pass
        return outputs


    def getparams(self):
        params = {}
        try:
            for apiparam in self.settings['params']:
                params[apiparam] = {'description': self.settings['params'][apiparam]['description'] if 'description' in self.settings['params'][apiparam] else None}
        except Exception as e:
            pass
        return params

    def setparams(self, params):
        self.params = params

    def getservicedesription(self):
        description = ''
        try:
            description = self.settings['description'] if 'description' in self.settings else None
        except Exception as e:
            pass
        return description

