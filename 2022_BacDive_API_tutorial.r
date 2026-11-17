
## load library
library(BacDive)

## initialize BacDive client
bacdive <- open_bacdive("test@test.de", "password")

## fetch strain data with a BacDive ID
one_strain <- fetch(object = bacdive, ids = 5621)
one_strain
## received strain information is stored in one_strain$results
one_strain$results

## fetch strain data for more than one strain with BacDive IDs
two_strains <- fetch(object = bacdive, ids = 5621, 139709)

## the output can be stored in a data frame for easier handling
two_strains_df <- as.data.frame(two_strains)
## the main strain data categories are the different columns of the data frame
## the rows are the two strains
colnames(two_strains_df)
head(two_strains_df)

## request BacDive ID in search with culture collection number
id <- request(object = bacdive, query = "DSM 2801", search = "deposit")
## the received BacDive ID is in id$result
id$results

## request BacDive ID in search with 16S gene accession number
id <- request(object = bacdive, query = "M58777", search = "16S")
id$results

## request BacDive IDs in search with taxon name
ids <- request(object = bacdive, query = "Myroides odoratus", search = "taxon")
ids
ids$results

## Maximum 100 entries are stored in ids$results!!!
## The total number of entries can be see in bac1$count.
ids <- request(object = bacdive, query = "Myroides", search = "taxon")
ids
ids$results

## Retrieve strain information directly from non-BacDive IDs or taxon names
strains <- retrieve(object = bacdive, query = "Myroides", search = "taxon")
strains

## the output can be stored in a data frame like the output of fetch()
strains_df <- as.data.frame(strains)
nrow(strains_df)


## Check how many of the Myroides strains are type strains
num_type=0
for (i in 1:nrow(strains_df)){
  if (strains_df[["Name and taxonomic classification"]][i][[1]][["type strain"]]=="yes"){
    num_type=num_type+1
  }
}
num_type

## Go through DSM numbers and find the respective BacDive IDs.
DSM_BacDive <- data.frame(matrix(ncol=2,nrow=20))
colnames(DSM_BacDive) <- c("DSM Number","BacDive ID")

for (i in 1:20){
  DSM_num <- paste("DSM", i, sep = " ")
  ret <- request(object = bacdive, query = DSM_num, search = "deposit")
  DSM_BacDive[i,1] <- DSM_num
  if (ret$count==1){
    DSM_BacDive[i,2] <- ret$results[1]
  }
  else{
    DSM_BacDive[i,2] <- NA
  }
}

DSM_BacDive


