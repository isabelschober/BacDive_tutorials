#!/usr/bin/env python
import requests

# Example query for the new BacDive API beta version (2026-11-17)

def main():	

  # Define query
  # growth at lower than 10°C + origin human + complete genome sequence
  filters = {
      "culture_temp": {
          "test_type": {
              "eq": "growth"
          },
          "temp": {
              "lt": 10
          },
          "ability": {
              "eq": "positive"
          }
      },
      "origin": {
          "sample_type": {
              "contains": "human"
          }
      },
      "sequence_genomes": {
          "assembly_lvl": {
              "eq": "complete"
          }
      }
  }

  # Define output
  fields = [
      "strains.species",
      "strains.strain_number",
      "origin.sample_type",
      "sequence_genomes"
  ]

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
              "page": 0
          }
      ).json()
  
  # Parse and printresults
  print(results["count"])
  for strain in results["results"]:
      print()
      print(strain)


if __name__ == "__main__":
   main()
