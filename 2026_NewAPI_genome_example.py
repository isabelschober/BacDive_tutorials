#!/usr/bin/env python

import math
import requests

# Example query for the new BacDive API beta version (2026-11-17)
# For all strains that have linked INSDC genomes
# get the genome accession(s) of the best scoring genome

def main():	

    # Initialize output file
    out = open("best_genomes.csv","w")
    out.write("BacDive-ID,Species,Designation,CCNos,sequence_accession\n")

    # Define query
    filters = {
        "sequence_genomes": {
            "ID_sequence": {
                "exists": True
            }
        }
    }

    # Define output
    fields = [
        "strains.species",
        "strains.strain_number",
        "strains.designation",
        "sequence_genomes.insdc_acc",
        "sequence_genomes.bvbrc_acc",
        "sequence_genomes.img_acc",
        "sequence_genomes.score"
    ]

    # First request to get the count of strains
    results = requests.post("https://beta.bacdive.dsmz.de/search",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        },
        json={
            "filters": filters,
            "fields": fields,
            "limit": 1,
            "page": 0
        }
    ).json()
    count = results["count"]

    # Iterate through result pages (100 strains per page)
    for i in range(0,int(math.ceil(count/100))):
        # Request results
        results = requests.post("https://beta.bacdive.dsmz.de/search",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                json={
                    "filters": filters,
                    "fields": fields,
                    "limit": 100,
                    "page": i
                }
            ).json()

        # Parse results
        for strain in results["results"]:
            bd_id = str(strain["_id"])
            species = strain["strains"][0]["species"]
            if "designation" in strain["strains"][0]:
                des = strain["strains"][0]["designation"].replace(",",";")
            else:
                des = ""
            if "strain_number" in strain["strains"][0]:
                ccno = strain["strains"][0]["strain_number"].replace(",",";")
            else:
                ccno = ""        
            genome = max(strain["sequence_genomes"], key=lambda x: x['score'])
            if "insdc_acc" in genome:
                acc = genome["insdc_acc"]
            elif "bvbrc_acc" in genome:
                acc = genome["bvbrc_acc"]
            else:
                acc = genome["img_acc"]

            # Write results to output file
            out.write(bd_id + "," + species + "," + des + "," + ccno + "," + acc + "\n")

    out.close()

if __name__ == "__main__":
   main()
