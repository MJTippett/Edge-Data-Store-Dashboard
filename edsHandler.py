'''
Implements some simple classes (stream and EDS) to interact with EDS
'''

import json
import requests

import edsEnums


class edsBase(object):
    def __init__(self,edsParams):
        self.edsParams = edsParams

    # Helper method used to make GET requests
    def get(self,endpoint,queryParams=None):
        response = requests.get(endpoint, params = queryParams)
        
        if response.status_code >= 200 and response.status_code < 300:
            return response.json()
        else:
            print(response.status_code)
            print(response.json())
            return None


class eds(edsBase):
    def __init__(self, edsParams):
        super().__init__(edsParams)

    def __str__(self):
        obj = {
            'Endpoint': self.edsParams['endpoint']
        }
        return str(obj)


    # Returns a list of streams matching a given query string
    def get_streams(self,query,namespace='default'):
        returnValue = []

        # Check that a valid namespace was entered
        if(namespace.lower() not in edsEnums.namespaces.__members__):
            namespace = 'default'
        
        endpoint = '{}/api/v1/Tenants/default/Namespaces/{}/Streams'.format(self.edsParams['endpoint'],namespace)

        response = self.get(endpoint,query)
        # If the response is empty
        if(response is None):
            return returnValue
        else:
            for stream in response:
                stream = edsStream(stream, self.edsParams, namespace)
                returnValue.append(stream)
            
            return returnValue
    
    # Returns all streams in a namespace
    def get_all_streams(self,namespace='default'):
        return self.get_streams('query=name:*', namespace)


class edsStream(edsBase):
    def __init__(self, properties, edsParams, namespace):
        super().__init__(edsParams)

        self.typeId = properties['TypeId']
        self.Id = properties['Id']
        self.name = properties['Name']
        self.description = properties['Description']
        self.InterpolationMode = properties['InterpolationMode']
        self.extrapolationMode = properties['ExtrapolationMode']

        self.namespace = namespace
    
    def __str__(self):
        obj = {
            'typeId': self.typeId,
            'Id': self.Id,
            'name': self.name,
            'description': self.description,
            'InterpolationMode': self.InterpolationMode,
            'extrapolationMode': self.extrapolationMode,
            'namespace': self.namespace
        }
        return str(obj)

    # Returns the last value of a stream
    def get_last_value(self):
        endpoint = '{}/api/v1/Tenants/default/Namespaces/{}/Streams/{}/Data/Last'.format(self.edsParams['endpoint'], self.namespace, self.Id)

        response = self.get(endpoint)
        return response
    
    # Returns the first value of a stream
    def get_first_value(self):
        endpoint = '{}/api/v1/Tenants/default/Namespaces/{}/Streams/{}/Data/First'.format(self.edsParams['endpoint'], self.namespace, self.Id)

        response = self.get(endpoint)
        return response

    # Returns a value at a certain index
    def get_distinct_value(self, index, searchMode = edsEnums.sdsSearchMode.exact):
        endpoint = '{}/api/v1/Tenants/default/Namespaces/{}/Streams/{}/Data'.format(self.edsParams['endpoint'], self.namespace, self.Id)
        
        query = 'index={}&searchMode={}'.format(index, searchMode.name)

        response = self.get(endpoint,query)
        return response

    # Returns range values for a stream based on a index value and maximum count
    def get_range_values(self, startIndex, count = 10, reverse = False, boundaryType = edsEnums.sdsBoundaryType.inside):
        endpoint = '{}/api/v1/Tenants/default/Namespaces/{}/Streams/{}/Data'.format(self.edsParams['endpoint'], self.namespace, self.Id)
        
        query = 'startIndex={}&count={}&reversed={}&boundaryType={}'.format(startIndex,count,reverse,boundaryType.name)

        response = self.get(endpoint,query)
        return response

    # Returns windows vlaues for a stream based on start and end indices
    def get_window_values(self, startIndex, endIndex, boundaryType = edsEnums.sdsBoundaryType.inside):
        endpoint = '{}/api/v1/Tenants/default/Namespaces/{}/Streams/{}/Data'.format(self.edsParams['endpoint'], self.namespace, self.Id)
        
        query = 'startIndex={}&endIndex={}&boundaryType={}'.format(startIndex, endIndex, boundaryType.name)

        response = self.get(endpoint,query)
        return response

    # Returns summary data for a stream
    def get_summary_data(self, startIndex, endIndex, intervals):
        endpoint = '{}/api/v1/Tenants/default/Namespaces/{}/Streams/{}/Data/Summaries'.format(self.edsParams['endpoint'], self.namespace, self.Id)
        
        query = 'startIndex={}&endIndex={}&count={}'.format(startIndex, endIndex, intervals)

        response = self.get(endpoint,query)
        return response



        


