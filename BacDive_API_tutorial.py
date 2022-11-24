## import package
import bacdive

## initialize BacDive client 
client = bacdive.BacdiveClient('test@test.de', 'password')

## search with a BacDive ID
client.search(id="5621")

## retrieval of data for the strain previously searched
for strain in client.retrieve():
    print(strain)
    
## search with more than one BacDive ID
client.search(id="5621;138170")

## retrieval of data for the strains previously searched 
## (print only general information)
for strain in client.retrieve():
    print(strain["General"])
    
## search with a genus name
client.search(taxonomy="Myroides")

## search with a species name
client.search(taxonomy="Myroides odoratus")

## retrieval of data for the strains previously searched 
## with filter -> retrieve only the data for culture collection no.
for strain in client.retrieve(["culture collection no."]):
    print(strain)
    
## search with culture collection number
client.search(culturecolno="DSM 100861")

## retrieval of data for the strain previously searched
## with filter -> retrieve only the data for "family"
for strain in client.retrieve(["family"]):
    print(strain)
    
## retrieval of data for the strain previously searched
## with filter -> retrieve only the data for "full scientific name" and "culture medium"
for strain in client.retrieve(["full scientific name","culture medium"]):
    print(strain)
    
## Go through DSM numbers and find the respective BacDive IDs.
for i in range(1,21):
    DSM_num="DSM "+str(i)
    print(DSM_num, end="\t")
    result=client.search(culturecolno=DSM_num)
    if result:
        for strain in client.retrieve(["BacDive-ID"]):
            print(list(strain)[0])
            
## To which species do the BacDive strains of the genus Myroides belong?
client.search(taxonomy="Myroides")
species=[]
for strain in client.retrieve(["species"]):
    species.append(strain[list(strain)[0]][0]["species"])
from collections import Counter
print(Counter(species))
