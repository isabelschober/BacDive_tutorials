1. [The Bac*Dive* API](#the-bacdive-api)                 
        1.1. [APIs](#apis)              
        1.2. [The Bac*Dive* API](#the-bacdive-api-1)              
        1.3. [Endpoints](#endpoints)            
        
2. [The Bac*Dive* R Package](#the-bacdive-r-package)                   
        2.1. [Installation](#installation)               
        2.2. [Initialization](#initialization)              
        2.3. [R functions](#r-functions)


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

When data for a large number of strains is delivered, the results are paginated at 100 strains per page (JSON file).

### Endpoints

The Bac*Dive* API has five different endpoints (network locations) that can be used to send requests and receive data.

The endpoints can be tested in the browser by adding the name of the desired endpoint to the Bac*Dive* API URL and then specifying the query.

#### fetch

API requests to this endpoint are made by Bac*Dive* ID and return all Bac*Dive* information on the strain(s). All other endpoints return Bac*Dive* IDs that can then in turn be searched using fetch.

Browser example:     
https://api.bacdive.dsmz.de/fetch/5621

A detailed explanation of the data fields in the delivered JSON file can be found [here](https://api.bacdive.dsmz.de/strain_fields_information).

Data for several Bac*Dive* strains can be requested at the same time when their IDs are delimited by semicolons. There is a limit of 100 IDs per call.

Browser example:      
https://api.bacdive.dsmz.de/fetch/5621;139709

#### culturecollectionno

API requests to this endpoint are made by culture collection number and return Bac*Dive* IDs.

Browser example:     
[https://api.bacdive.dsmz.de/culturecollectionno/DSM 2801](https://api.bacdive.dsmz.de/culturecollectionno/DSM%202801)

#### taxon

API requests to this endpoint are made by genus, species or subspecies name and return the Bac*Dive* IDs of all strains present for that taxon in the Bac*Dive* database.

Browser example for a genus name:      
https://api.bacdive.dsmz.de/taxon/Myroides

Browser example for a species name:      
https://api.bacdive.dsmz.de/taxon/Myroides/odoratus

Browser example for a subspecies name:   
https://api.bacdive.dsmz.de/taxon/Myroides/odoratimimus/xuanwuensis

#### sequence_16s

API requests to this endpoint are made by 16S rRNA gene nucleotide accession numbers and return Bac*Dive* IDs.

Browser example:        
https://api.bacdive.dsmz.de/sequence_16s/M58777

#### sequence_genome

API requests to this endpoint are made by genome assembly accession numbers and return Bac*Dive* IDs.

Browser example:        
https://api.bacdive.dsmz.de/sequence_genome/GCA_000243275



## The Bac*Dive* R Package 

### Installation

The Bac*Dive* R Package  can be found at https://r-forge.r-project.org/R/?group_id=1573.

It can be installed within an R session using the install.packages() function.

```R
install.packages("BacDive", repos="http://R-Forge.R-project.org")
```
### Initialization

The Bac*Dive* client is initialized using the open_bacdive() function with your login data.

```R
bacdive <- open_bacdive("test@test.de", "password")
```
### R functions

#### fetch()

The fetch() function implements a request to the fetch endpoint of the API.

As parameters, the fetch() function takes the client object, initialized earlier, and one or more Bac*Dive* IDs.

```R
one_strain <- fetch(object = bacdive, ids = 5621)
```
```R
two_strains <- fetch(object = bacdive, ids = 5621, 139709)
```

The returned strain information is stored in the $results field.
```R
one_strain$results
```

For easier handling, the output can be transformed to a data frame.
```R
two_strains_df <- as.data.frame(two_strains)
```
The main strain data categories are then stored in different columns of the data frame, the searched strains are represented by different rows.

#### request()

The request() function implements requests to the four other endpoints of the BacDive API.

As parameters, the request() function takes the client object, a query and a search parameter specifying the queried endpoint.

A request to the culturecollectionno ("deposit") endpoint:
```R
id <- request(object = bacdive, query = "DSM 2801", search = "deposit")
```

The returned Bac*Dive* ID can be found in the $results field
```R
id$results
```
A request to the sequence_16s ("16S") endpoint:
```R
id <- request(object = bacdive, query = "M58777", search = "16S")
id$results
```

A request to the sequence_genome ("genome") endpoint:
```R
id <- request(object = bacdive, query = "GCA_006094295", search = "genome")
id$results
```

#### retrieve()
