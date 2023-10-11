### StrainInfo

# load requests package to make API requests
import requests

# Example strain Prevotella bivia 653C
designation="653C"

# make API request to search cultures connected with the designation
# using the requests.get() method and
# saving the response to a variable called 'response'
response=requests.get("https://api.straininfo.dsmz.de/v1/search/culture/str_des/"+designation)

# print 'response' using the json decoder from the requests package
print(response.json())

# store the first culture ID of the list
si_cu=response.json()[0]
print(si_cu)

# make API request to search information on the culture with the SI-CU
response=requests.get("https://api.straininfo.dsmz.de/v1/data/culture/max/"+str(si_cu))
print(response.json())

# store the strain ID (SI-ID) of the strain
si_id=response.json()[0]["strain"]["id"]
print(si_id)

# print designation of current culture
print(response.json()[0]["culture"]["strain_number"])
# print other designations of the strain
print(response.json()[0]["culture"]["relation"])

# store the BacDive ID of the strain
bd_id=response.json()[0]["strain"]["bacdive"]
print(bd_id)

### BacDive

# load bacdive package
import bacdive

# initialize BacDive client with email and password
client = bacdive.BacdiveClient('isabel.schober@dsmz.de', 'password')

# use the bacdive search method with a BacDive ID
client.search(id=bd_id)

# retrieve the searched data
for strain in client.retrieve():
    # print everything
    print(strain)
    
# turn on inclusion of predictions
client.includePredictions()

# retrieve the searched data
for strain in client.retrieve():
    # print only predictions
    print(strain["Genome-based predictions"])
    
# turn off inclusion of predictions
client.excludePredictions()

# retrieve the searched data
for strain in client.retrieve(["species","keywords","culture medium"]):
    # print keywords
    print(strain)
    # store the species name
    species=strain[str(bd_id)][1]["species"]
    
# print the stored species name
print(species)

# search BacDive for all strains of the species -> search with taxonomy
client.search(taxonomy=species)

# retrieve the searched data - with filter -> only retrieve BD-ID
for strain in client.retrieve("BacDive-ID"):
    print(strain)
    
### MediaDive
    
# requests package to make API requests is still loaded

# make API request with the stored BacDive ID to search media for the strain
# using the requests.get() method and
# saving the response to a variable called 'response'
response=requests.get("https://mediadive.dsmz.de/rest/strain/bacdive/"+str(bd_id))

# print 'response' using the json decoder from the requests package
print(response.json())

# store the MD-ID of the first medium in the list 
md_id=response.json()["data"]["media"][0]["medium_id"]
print(md_id)

# make API request with MediaDive ID to get full medium recipe
response=requests.get("https://mediadive.dsmz.de/rest/medium/"+str(md_id))
print(response.json())

# make API request with MediaDive ID to get list of strains connected to this medium
response=requests.get("https://mediadive.dsmz.de/rest/medium-strains/"+str(md_id))
print(response.json())










### Example using all three APIs

# load API request packages
import requests
import bacdive

# initialize BacDive client with email and password
client = bacdive.BacdiveClient('isabel.schober@dsmz.de', 'password')

# use the Bacdive search method with a species name
client.search(taxonomy="Prevotella bivia")

# use the Bacdive retrieve method to retrieve data on the strains
for strain in client.retrieve():
    
    # store part of the strain description
    desc=strain["General"]["description"].split(" is")[0]
    
    # store the BacDive ID of the strain
    bd_id=str(strain["General"]["BacDive-ID"])
    # store the first culture collection number of the strain
    ccno=strain["External links"]["culture collection no."].split(", ")[0]
    # store the isolation country if present
    if "country" in strain["Isolation, sampling and environmental information"]["isolation"]:
        country=strain["Isolation, sampling and environmental information"]["isolation"]["country"]
    else: 
        country="NA"
    # store the sampling date if present
    if "sampling date" in strain["Isolation, sampling and environmental information"]["isolation"]:
        date=strain["Isolation, sampling and environmental information"]["isolation"]["sampling date"].split("-")[0]
    else:
        date="NA"

    # use the StrainInfo API to store the StrainInfo culture ID for the culture
    response=requests.get("https://api.straininfo.dsmz.de/v1/search/culture/str_no/"+ccno)
    si_cu=response.json()[0]
    
    # use the StrainInfo API to store other designations for the strain listed in StrainInfo, if any are present
    response=requests.get("https://api.straininfo.dsmz.de/v1/data/culture/max/"+str(si_cu))
    if "relation" in response.json()[0]["culture"]:
        other_des=response.json()[0]["culture"]["relation"]
    else:
        other_des=""
    
    # use the MediaDive API to store a Medium ID of a medium for the strain, if present in MediaDive (unfortunately most are not in this case)
    response=requests.get("https://mediadive.dsmz.de/rest/strain/bacdive/"+str(bd_id))
    if response.json()["status"]==200:
        md_id=str(response.json()["data"]["media"][0]["medium_id"])
    else: 
        md_id="NA"

    # print everything
    print("\n"+desc)
    print("Strain: "+ccno,end="")
    if len("other_des")>1:
        print(" ("+", ".join(other_des)+")")
    else:
        print()
    print("BacDive-ID: "+bd_id)
    print("Isolation: "+country+", "+date)
    print("Medium: "+md_id)
