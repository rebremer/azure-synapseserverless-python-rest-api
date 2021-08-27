import sys
import os
import json
import pyodbc
import socket
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from threading import Lock
from tenacity import *
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler
import logging
import struct

# Initialize Flask
app = Flask(__name__)

# Setup Azure Monitor
if 'APPINSIGHTS_KEY' in os.environ:
    middleware = FlaskMiddleware(
        app,
        exporter=AzureExporter(connection_string="InstrumentationKey={0}".format(os.environ['APPINSIGHTS_KEY'])),
        sampler=ProbabilitySampler(rate=1.0),
    )

# Setup Flask Restful framework
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('total_amount')

# Implement singleton to avoid global objects
class ConnectionManager(object):    
    __instance = None
    __connection = None
    __lock = Lock()

    def __new__(cls):
        if ConnectionManager.__instance is None:
            ConnectionManager.__instance = object.__new__(cls)        
        return ConnectionManager.__instance       
    
    def __getConnection(self):
        if (self.__connection == None):

            flask_env_setting = os.getenv('FLASK_ENV', 'webapp')
            if flask_env_setting == 'development':
                # az account get-access-token --resource=https://database.windows.net/ --query accessToken
                #
                token = os.environ['TOKEN']
                token= token.replace('"','') # Make sure that unnecessary quotes are removed
                accessToken = bytes(token, 'utf-8')
                exptoken = b""
                for i in accessToken:
                    exptoken += bytes({i})
                    exptoken += bytes(1)
                    tokenstruct = struct.pack("=i", len(exptoken)) + exptoken

                connstr = os.environ['SQLAZURECONNSTR_TAXI']
                self.__connection = pyodbc.connect(connstr, attrs_before = { 1256:tokenstruct })
            else:
                connstr = os.environ['SQLAZURECONNSTR_TAXI'] + ';Authentication=ActiveDirectoryMsi'
                self.__connection = pyodbc.connect(connstr)

        return self.__connection

    def __removeConnection(self):
        self.__connection = None

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(10), retry=retry_if_exception_type(pyodbc.OperationalError), after=after_log(app.logger, logging.DEBUG))
    def executeQueryJSON(self, procedure, payload=None):
        result = {}  

        #return {"rene":"test"}

        try:
            conn = self.__getConnection()

            cursor = conn.cursor()
            
            if payload:
                #total_amount = {}
                #total_amount["total_amount"] = 14
                cursor.execute(f"EXEC get_taxidataAmount ?", json.dumps(payload))
            else:
                cursor.execute(f"EXEC get_taxidata")

            result = cursor.fetchall()

            if result:
                #result = json.loads(result[0])
                result = json.loads(''.join([row[0] for row in result]))                         
            else:
                result = {}

            cursor.commit()    
        #except pyodbc.OperationalError as e:            
        #    app.logger.error(f"{e.args[1]}")
        #    if e.args[0] == "08S01":
        #        # If there is a "Communication Link Failure" error, 
        #        # then connection must be removed
        #        # as it will be in an invalid state
        #        self.__removeConnection() 
        #        raise 
        except Exception as e:
            result = {"rene":e.args[1]}                 
        #finally:
        #    cursor.close()
                         
        return result

class Queryable(Resource):
    def executeQueryJson(self, verb, payload=None):
        result = {}  
        entity = type(self).__name__.lower()
        procedure = f"dbo.get_taxidata"
        result = ConnectionManager().executeQueryJSON(procedure, payload)
        return result

# Customer Class
class TaxiData(Queryable):
    def get(self, total_amount):     
        total_amount_json = {}
        total_amount_json["total_amount"] = total_amount
        result = self.executeQueryJson("dbo.get_taxidataAmount", total_amount_json)   
        return result, 200
    
# Customers Class
class TaxiDataall(Queryable):
    def get(self):     
        result = self.executeQueryJson("dbo.get_taxidata")   
        return result, 200
    
# Create API routes
api.add_resource(TaxiData, '/taxidataprice', '/taxidataprice/<total_amount>')
api.add_resource(TaxiDataall, '/taxidataall')
