# Creating a REST API with Python on Synapse Serverless pools using external tables

![License](https://img.shields.io/badge/license-MIT-green.svg)

<!-- 
Guidelines on README format: https://review.docs.microsoft.com/help/onboard/admin/samples/concepts/readme-template?branch=master

Guidance on onboarding samples to docs.microsoft.com/samples: https://review.docs.microsoft.com/help/onboard/admin/samples/process/onboarding?branch=master

Taxonomies for products and languages: https://review.docs.microsoft.com/new-hope/information-architecture/metadata/taxonomies?branch=master
-->
Based on work by Davide Mauri, see [blogpost here](https://techcommunity.microsoft.com/t5/azure-sql/building-rest-api-with-python-flask-and-azure-sql/ba-p/1056637) and [gitrep here](https://github.com/Azure-Samples/azure-sql-db-python-rest-api)

Thanks to native JSON support, creating a REST API with Azure Synapse external tables and Python is really a matter of a few lines of code. Take a look at `app.py` to easy it is!

Wondering what's the magic behind? The sample uses the well known [Flask](https://flask.palletsprojects.com/en/1.1.x/) micro-framework and the [flask-restful](https://flask-restful.readthedocs.io/en/latest/) package to easily implement REST APIs. Beside that the [native JSON support that Azure SQL provides](https://docs.microsoft.com/en-us/azure/sql-database/sql-database-json-features) does all the heavy lifting so sending data back and forth to the database is as easy as sending a JSON message.

## Install Synapse 

In order to run this sample, an Azure Synapse Workspace is needed:

[Create Synapse workspace](https://docs.microsoft.com/en-us/azure/synapse-analytics/quickstart-create-workspace)

## Add data to Synapse primarey storage account

Create a FileSystem named `taxidata` and add the data files 

`./data/part-00005-tid-8364420724365899593-b5fafbac-8fd5-4869-a6b6-e607867d9673-6-1-c000.snappy.parquet` 

from this git repo to this repository

## Run SQL scripts

Once the Synapse Workspace has been established database has been installed, you need to add create external tables and stored procedures that will be called from Python. The SQL code is available here:

```
./sql/1_create_external_table.sql
./sql/2_stored_procedures.sql
```

If you need any help in executing the SQL script, you can find a Quickstart here: [Quickstart: Use Azure Data Studio to connect and query Azure SQL database](https://docs.microsoft.com/en-us/sql/azure-data-studio/quickstart-sql-database)

## Run sample locally

Make sure you have Python 3.7 installed on your machine. Clone this repo in a directory on our computer and then create a [virtual environment](https://www.youtube.com/watch?v=_eczHOiFMZA&list=PLlrxD0HtieHhS8VzuMCfQD4uJ9yne1mE6&index=34). For example:

```bash
virtualenv venv --python C:\Python37\
```

then activate the created virtual environment. For example, on Windows:

```powershell
.\venv\Scripts\activate
```

and then install all the required packages:

```bash
pip install -r requirements
```

The connections string is not saved in the python code for security reasons, so you need to assign it to an environment variable in order to run the sample successfully. You also want to enable [development environment](https://flask.palletsprojects.com/en/1.1.x/config/#environment-and-debug-features) for Flask:

Linux:

```bash
export FLASK_ENV="development"
export SQLAZURECONNSTR_TAXI="<your-connection-string>"
# Bearer token from user that has contributor rights on Azure Synapse workspace, can be generated using Azure CLI as follows
export TOKEN=$(az account get-access-token --resource=https://database.windows.net/ --query accessToken)
```

Windows:

```powershell
$Env:FLASK_ENV="development"
$Env:SQLAZURECONNSTR_TAXI="<your-connection-string>"
# Bearer token from user that has contributor rights on Azure Synapse workspace, can be generated using Azure CLI as follows
$Env:TOKEN=az account get-access-token --resource=https://database.windows.net/ --query accessToken
```

Your connection string is something like:

```
DRIVER={ODBC Driver 17 for SQL Server};SERVER=<your-server-name>-ondemand.sql.azuresynapse.net;DATABASE=<your-database-name>
```

Just replace `<your-server-name>` and `<your-database-name>` with the correct values for your environment.

To run and test the Python REST API local, just run

```bash
flask run
```

Python will start the HTTP server and when everything is up and running you'll see something like

```text
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Using a REST Client (like [Insomnia](https://insomnia.rest/), [Postman](https://www.getpostman.com/) or curl), you can now call your API, for example:

```bash
curl -X GET localhost:5000/taxidataall
curl -X GET localhost:5000/taxidateprice/20
```

In the latter, you'll get info on total_amount 20:

```json
[
    {
        "VendorID": 1,
        "tpep_pickup_datetime": "2019-01-31T13:34:15",
        "tpep_dropoff_datetime": "2019-01-31T13:55:37",
        "passenger_count": 1,
        "trip_distance": 3.2,
        "RatecodeID": 1,
        "store_and_fwd_flag": false,
        "PULocationID": 236,
        "DOLocationID": 263,
        "payment_type": 1,
        "fare_amount": 15.5,
        "extra": 0.0,
        "mta_tax": 0.5,
        "tip_amount": 3.7,
        "tolls_amount": 0.0,
        "improvement_surcharge": 0.3,
        "total_amount": 20.0,
        "congestion_surcharge": 0.0
    }
]
```

## Debug from Visual Studio Code

Debugging from Visual Studio Code is fully supported. Make sure you create an `.env` file the look like the following one (making sure you add your connection string)

```
FLASK_ENV="development"
SQLAZURECONNSTR_TAXI=""
```

and you'll be good to go.

## Deploy to Azure

Now that your REST API solution is ready, it's time to deploy it on Azure so that anyone can take advantage of it. This can be done using the following simple command using the Azure CLI, see also [here](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=bash&pivots=python-framework-flask#deploy-the-sample):

```bash
appName="<<your app name>>"
resourceGroup="<<your resource group>>"
az webapp up --sku B1 --name appName
```

Two more things you have do in addition to what explained in the above articles:

### 1. Add connection string

Connection string needs to be added to the Azure Web App configuration. Using AZ CLI, for example:

```bash
appName="your-app-name"
resourceGroup="my-resource-group"

az webapp config connection-string set \
    -g $resourceGroup \
    -n $appName \
    --settings TAXI=$SQLAZURECONNSTR_TAXI \
    --connection-string-type=SQLAzure
```

Just make sure you correctly set `$appName` and `$resourceGroup` to match your environment and also that the variable `$SQLAZURECONNSTR_WWIF` as also been set, as mentioned in section "Run sample locally". An example of a full script that deploy the REST API is available here: `azure-deploy.sh`.

Please note that connection string are accessible as environment variables from Python when running on Azure, *but they are prefixed* as documented here:

https://docs.microsoft.com/en-us/azure/app-service/configure-common#connection-strings

That's why the Python code in the sample look for `SQLAZURECONNSTR_TAXI` but the Shell script write the `TAXI` connection string name.

### 2. Assign Managed Identity to web app and grant rights to Synapse Serverless and underlying storage account

First, enable managed Identity of web app, this can be done using following Azure CLI command:

```bash
az webapp identity assign -g $resourceGroup -n $appName
```

Then grant the Managed Identity ```Storage Blob Data Reader ``` rights to storage account where taxi data is stored. The name of the function app ```$appName``` can be used for as user that shall be granted rights, see [here](https://docs.microsoft.com/en-us/azure/storage/blobs/assign-azure-role-data-access?tabs=portal#assign-an-azure-role)

Finally, run the web app managed identity shall also be granded righs to read data from the Synapse serverless pools and be able to execute the stored procedure.

The SQL code is available here:

`./sql/3_grant_WebApp_database_rights.sql`


## Connection Resiliency

As per best practices, code implement a retry logic to make sure connections to Azure SQL are resilient and che nicely handle those cases in which the database may not be available. One of these case is when database is being scale up or down. This is usually a pretty fast operation (with Azure SQL Hyperscale it happens in something around 10 seconds), but still graceful management of connection is needed. 

The sample uses the [Tenacity](https://tenacity.readthedocs.io/en/latest/) library to implement a simple retry-logic in case the error "Communication link failure" happens (see [ODBC Error Codes](https://docs.microsoft.com/en-us/sql/odbc/reference/appendixes/appendix-a-odbc-error-codes)).

If you need more details aside the general error generated by the ODBC call, you can take a look at the detailed errors that Azure SQL will return here: [Troubleshooting connectivity issues and other errors with Microsoft Azure SQL Database](https://docs.microsoft.com/en-us/azure/sql-database/troubleshoot-connectivity-issues-microsoft-azure-sql-database)

To test connection resiliency you can using testing tools like [Locust.io](https://locust.io/), [K6](https://k6.io/) or [Apache JMeter](https://jmeter.apache.org/). IF you want something really simple to try right away, a while loop will do. For example:

```bash
while :; do curl -s -X GET http://localhost:5000/customer/$((RANDOM % 1000)); sleep 1; done
```

## PyODBC, Linux and Connection Pooling

To get the best performances, Connection Pooling should be used so that each time the code tries to open and close a connection, it can just take an existing connection from the pool, reset it, and use that one. Using a connection from the pool is way less expensive than creating a new connection, so by using connection pooling performance can be greatly improved.

Unfortunately as of today (March 2020) ODBC connection pooling in Linux does work as expected to due an issue in unixODBC library. To work around that, I had to implement a manual technique to pool connection, that you can find in the `ConnectionManager` class.

Once the issue will be fixed, or if you are using Windows, you can completely remove that part of the code, and just open and close the connection as you would do normally, as connection pooling will be used automatically behind the scenes.

## Learn more

If you're new to Python and want to learn more, there is a full free Python curse here:

- [Python for Beginners - Videos](https://aka.ms/python-for-beginners)
- [Python for Beginners - GitHub Repo](https://github.com/microsoft/c9-python-getting-started)

It will teach you not only how to use Python, but also how to take advantage the a great editor like Visual Studio Code.

Flask is a very common (and amazing!) framework. Learn how to use it right from Visual Studio Code with this tutorial:

[Flask Tutorial in Visual Studio Code](https://code.visualstudio.com/docs/python/tutorial-flask)

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.