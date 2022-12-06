# Bac*Dive* Tutorials

## The Bac*Dive* API

### APIs

An API (Application Programming Interface) is a set of procedures that allows two applications to communicate with each other. These procedures can be used to write code that communicates with another application, like a software or a website like Bac*Dive*. Through API procedures, requests to websites can be automated.

### The Bac*Dive* API

The Bac*Dive* API can be found at https://api.bacdive.dsmz.de/ or by clicking on the 'Web services' tab on the [Bac*Dive* website](https://bacdive.dsmz.de).

[Registration/Login](https://sso.dsmz.de/auth/realms/DSMZ/protocol/openid-connect/auth?response_type=code&redirect_uri=https%3A%2F%2Fapi.bacdive.dsmz.de%2Flogin&client_id=api.bacdive&nonce=d8f6663726e72d881a22d672e7a56109&state=770e6085fc26b50e2535e193b49dfa8c&scope=openid) is required to use the API, but is fast and easily accomplished.

For all requests, the requested data is returned in JSON format with the following fields:

* **count** - Number of entries retrieved
* **next** - URL to next page if results are paginated, otherwise 'null'
* **previous** - URL to previous page if results are paginated, otherwise 'null'
* **results** - Requested data


#### Endpoints

The Bac*Dive* API has five different endpoints (network locations) that can be used to send requests and receive data.

The endpoints can be tested in the browser by adding the name of the desired endpoint to the Bac*Dive* API URL and then specifying the query.

##### fetch

API requests to this endpoint are made by Bac*Dive* ID and return all Bac*Dive* information on the strain(s). All other endpoints return Bac*Dive* IDs that can then in turn be searched using fetch.

Browser example:     
https://api.bacdive.dsmz.de/fetch/5621

Several IDs can be looked up at the same time when delimited by semicolon. There is a limit of 100 IDs per call.

--------------------------





