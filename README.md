1. [The Bac*Dive* API](#the-bacdive-api)                 
        1.1. [APIs](#apis)              
        1.2. [The Bac*Dive* API](#the-bacdive-api-1)              
        1.3. [Endpoints](#endpoints)            
        
2. [The Bac*Dive* R Package](#the-bacdive-r-package)                   
        2.1. [Installation](#installation)               
        2.2. [Initialization](#initialization)              
        2.3. [R functions](#r-functions)         
        2.4. [Examples](#examples)

3. [The Bac*Dive* Python Package](#the-bacdive-python-package)               
        3.1. [Installation](#installation-1)           
        3.2. [Initialization](#initialization-1)           
        3.3. [Python Methods: Search and Retrieve](python-methods-search-and-retrieve)                      
        3.4. [Examples](#examples-1)
            

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
library(BacDive)

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

The taxon endpoint differs from the culturecollectionno and sequence endpoints as a request usually returns not just one, but several Bac*Dive* IDs.

In the following example request to the taxon ("taxon") endpoint using the species name *Myroides odoratus*, the count field of the output shows that 19 strains of this species are present in the database. The results field contains all 19 Bac*Dive* IDs.
```R
ids <- request(object = bacdive, query = "Myroides odoratus", search = "taxon")
ids
ids$results
```
In another example using the genus name *Myroides*, the count field correctly notes 106 strains for this genus in Bac*Dive*, but the results field does not contain all their Bac*Dive* IDs. **The request() function cannot return more than 100 Bac*Dive* IDs.** This is due to the pagination of the API, which limits output JSON files to 100 IDs per page. The request() function only returns the results from teh first page.
```R
ids <- request(object = bacdive, query = "Myroides", search = "taxon")
ids
ids$results
```
The request() function is useful in cases in which you want to receive only Bac*Dive* IDs and no further information on the strains and in which you know that your request will not return more than 100 IDs at a time.

In other cases, the retrieve() function should be used.

#### retrieve()

The retrieve() function can retrieve data directly using non BacDive IDs and taxon names. It can retrieve data for any number of strains without the limitation of the request() function. 

As parameters, the retrieve() function takes the client object, a query and a search parameter specifying the queried endpoint.     
Here the taxon enpoint is again queried for the genus *Myroides*.
```R
strains <- retrieve(object = bacdive, query = "Myroides", search = "taxon")
strains
```
Data for all 106 strains is retrieved and can now be transformed into a data frame with one row for each strain.
```R
strains_df <- as.data.frame(strains)
nrow(strains_df)
```

### Examples

With the available data on all *Myroides* strains now stored in a data frame, specific data fields can be looked up.

In this example, the number of *Myroides* strains, which are type strains for their species is counted, by iterating through the rows of the data frame and asking whether the type strain field is filled with a 'yes'.

```R
#strains <- retrieve(object = bacdive, query = "Myroides", search = "taxon")
#strains_df <- as.data.frame(strains)

# initialization of numerator
num_type=0
# loop through all rows of data frame containing data on all Myroides strains
for (i in 1:nrow(strains_df)){
  # check if 'type strain' field is 'yes' > if it is add +1 to numerator
  if (strains_df[["Name and taxonomic classification"]][i][[1]][["type strain"]]=="yes"){
    num_type=num_type+1
  }
}
num_type
```

In a second example the Bac*Dive* IDs of a number of DSM strains are looked up, in this case the strains DSM 1 to DSM 20.       
After the initialization of an output data frame, a for-loop goes through the numbers 1 to 20. The prefix "DSM" is added to each number to make the DSM indentifier , which is then used as query in a request to the culturecollectionno endpoint. If the DSM strain is present in Bac*Dive*, the count field of the received output says '1' and the BacDive ID is saved to the data frame. Otherwise, an 'NA' is put into the respective field.

```R
# initialization of output data frame
DSM_BacDive <- data.frame(matrix(ncol=2,nrow=20))
colnames(DSM_BacDive) <- c("DSM Number","BacDive ID")

# loop through numbers 1 to 20
for (i in 1:20){
  # addition of prefix DSM to number
  DSM_num <- paste("DSM", i, sep = " ")
  # request to BaDive API
  ret <- request(object = bacdive, query = DSM_num, search = "deposit")
  # addition DSM identifier to output data frame
  DSM_BacDive[i,1] <- DSM_num
  # if the API request returned a result > addition of BacDive ID to output data frame
  if (ret$count==1){
    DSM_BacDive[i,2] <- ret$results[1]
  }
  # if no result was returned > addition of NA to output data frame
  else{
    DSM_BacDive[i,2] <- NA
  }
}

DSM_BacDive
```

## The Bac*Dive* Python package

### Installation 

The Bac*Dive* Python package is available in the Python Package Index (PyPI): https://pypi.org/project/bacdive/.            

It can be installed in a UNIX terminal using the pip installer.

```bash
pip install bacdive
```

### Initialization

The Bac*Dive* client needs to be initialized with your login data.

```Python
import bacdive

client = bacdive.BacdiveClient('test@test.de', 'password')
```

### Python methods: search and retrieve

The 'search' method takes BacDive IDs, other IDs or taxon names and fetches and stores all BacDive IDs that are found for this query.

This is an example for a search with a Bac*Dive* ID using the 'id' parameter:
```Python
client.search(id="5621")
```
The function returns a '1', showing that it stored one Bac*Dive* ID.

The actual data for the strains whose IDs were stored with the 'search' method can then be retrieved using the 'retrieve' method.

```Python
for strain in client.retrieve():
    print(strain)
```

The method returns a nested dictionary that contains all the information on the strains that are in Bac*Dive* and that you could also see on the Bac*Dive* website if you would search for the strain there.

This also works with more than one Bac*Dive* ID.

Example using two Bac*Dive* IDs and printing out only the general information on the strains when using the 'retrieve' method:
```Python
client.search(id="5621;138170")

for strain in client.retrieve():
    print(strain["General"])
```
For API requests with taxon names, the 'taxonomy'parameter is used in the 'search' method.

Example with a genus name:
```Python
client.search(taxonomy="Myroides")
```
All the BacDive IDs for the genus *Myroides* strains that are present in the BacDive database are stored.

Example with a species name:
```Python
client.search(taxonomy="Myroides odoratus")
```

Again all the BacDive IDs of strains of this species that are present in the BacDive database are stored.

Instead of retrieving the complete data on the strains and then using only a small part of it, as in the previous example, the 'retrieve' function can also be used with filters by specifying which information shall be retrieved.

For this, a list of keys specifying the data fields to be retrieved is added to the 'retrieve' function as parameter.

In this example only the culture collection numbers of the previously searched *Myroides odoratus* strains are retrieved:
```Python
for strain in client.retrieve(["culture collection no."]):
    print(strain)
```
Of course this can also be done the other way round. This example shows a search with a culture collection number. In this case, another filter is given in the 'retrieve' method: the taxonomic family information.

```Python
client.search(culturecolno="DSM 100861")

for strain in client.retrieve(["family"]):
    print(strain)
```
The DSM strain belongs to the family *Flavobacteriaceae*.

Information on the same strains can again be retrieved with other filters.

In this example, a list of two filters is given in the 'retrieve' function, they are the full scientific name field and the information that the stored in the culture medium field.

```Python
for strain in client.retrieve(["full scientific name","culture medium"]):
    print(strain)
```

### Example

Again, the BacDive IDs of a number of DSM strains 1 to 20 are looked up.

```Python
# loop through the numbers 1 to 20
for i in range(1,21):
    # addition of prefix DSM to number
    DSM_num="DSM "+str(i)
    # print out of the DSM identifier
    print(DSM_num, end="\t")
    # API request
    result=client.search(culturecolno=DSM_num)
    # if the request returned a result > print out the BacDive ID
    if result:
        for strain in client.retrieve(["BacDive-ID"]):
            print(list(strain)[0])
```


In the second example, all the strains of the genus *Myroides* are again searched. Then, I want to now which species these strains belong to.

```Python
# API search for all Myroides strains
client.search(taxonomy="Myroides")
# initialization of output list
species=[]
# for each Myroides strain, the species information is retrieved and appended to the output list
for strain in client.retrieve(["species"]):
    species.append(strain[list(strain)[0]][0]["species"])
# the Counter function from the collection package is imported and used to count the number of instances of each species name in the output list 
from collections import Counter
print(Counter(species))
```
