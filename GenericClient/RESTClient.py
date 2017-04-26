from GenericClientABC import GenericClientABC
import urllib3
import json
import yaml
from urllib.parse import urlencode, quote
from jsonpath_rw import jsonpath, parse
import base64
import pandas as pd

#httpconnpool = urllib3.PoolManager(num_pools=10, maxsize=30, block=True, timeout = 20.0)
httpconnpool = urllib3.ProxyManager('http://proxy-idp01.ind.hp.com:8080', num_pools=10, maxsize=30, block=True, timeout = 20.0)

class RESTClient(metaclass=GenericClientABC):
    """Paramter driven REST client implementation"""
    def __init__(self, settingsfile, params):
        with open(settingsfile) as settingsfile:
            settings = yaml.safe_load(settingsfile)
        self.settings = settings
        self.params = params
        #validate settings
        if settings['endpoint']['url'] == None or len(settings['endpoint']['url']) == 0:
            raise Exception('Invalid end point URL')
        if settings['endpoint']['method'] not in ['get', 'post', 'put']:
            raise Exception('Invalid http method')
        #validate parameters
        #start with 
        if self.settings['authenticationscheme'] == 'apikey' and self.params['apikey'] == None:
            raise Exception('API Key not provided') 
        #TODO validate other authentication schemes


    def ProcessRequest(self, inputcontext):
        outputcontext = {}
        #copy input context to output context
        outputcontext = inputcontext.copy()

        try:
            #process input paramteters
            #query string first
            querystring = {}
            headers = {}
            jsondictbody = {}
            url = self.settings['endpoint']['url']
            if 'inputmap' in self.settings:
                for input in self.settings['inputmap']:
                    inputvalue = inputcontext[input]
                    if 'encode' in self.settings['inputmap'][input]:
                        if str(self.settings['inputmap'][input]['encode']).lower() == 'true':
                            #switch on encoding scheme
                            if str(self.settings['inputmap'][input]['encodingscheme']).lower() == 'base64':
                                inputvalue = base64.b64encode(inputcontext[input].encode()).decode('ascii')
                            elif str(self.settings['inputmap'][input]['encodingscheme']).lower() == 'urlencode':
                                inputvalue = quote(inputcontext[input])
                            else:
                                raise Exception('Unknown encoding scheme for {} input'.format(input))
                        elif str(self.settings['authentication']['apikey']['encode']).lower() == 'false':
                            inputvalue = inputcontext[input]
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
                #check if we need to encode
                if str(self.settings['authentication']['apikey']['encode']).lower() == 'true':
                    #switch on encoding scheme
                    if str(self.settings['authentication']['apikey']['encodingscheme']).lower() == 'base64':
                        apikey = base64.b64encode(self.params['apikey'].encode()).decode('ascii')
                    elif str(self.settings['authentication']['apikey']['encodingscheme']).lower() == 'urlencode':
                        apikey = quote(self.params['apikey'])
                    else:
                        raise Exception('Unknown encoding scheme for APIKEY')
                elif str(self.settings['authentication']['apikey']['encode']).lower() == 'false':
                    apikey = self.params['apikey']
                else:
                    raise Exception('Unknown encoding swtich for APIKEY')

            
                if str(self.settings['authentication']['apikey']['target']).lower() == 'querystring':
                    querystring[self.settings['authentication']['apikey']['querystring']] = str(self.settings['authentication']['apikey']['value']).format(apikey)
                elif str(self.settings['authentication']['apikey']['target']).lower() == 'header':
                    headers[self.settings['authentication']['apikey']['header']] = str(self.settings['authentication']['apikey']['value']).format(apikey)
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
            if 'headers' in self.settings:
                for header in self.settings['headers']:
                    headers[header] = self.settings['headers'][header]

            response = httpconnpool.urlopen(self.settings['endpoint']['method'].upper(),  url, headers=headers, body=body)
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


    def GetInputs(self):
        inputs = {}
        try:
            inputs = self.settings['inputmap'].keys()            
        except Exception as e:
            pass
        return inputs

    def GetParams(self):
        params = {}
        try:
            params = self.settings['params'].keys()
        except Exception as e:
            pass
        return params
