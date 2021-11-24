#!/usr/bin/env python3
import os
import json
import csv
import argparse
import requests
import urllib

#URI = "https://dlib2.biblhertz.it/iiif/3/bncrges1323"
#CSV="https://docs.google.com/spreadsheets/d/e/2PACX-1vTfa4Q-66Qa_CdNISFBswzZF4Io3uFOI4nG-05tkac1sru3L69bfUZoJC8Rp3lyfmpdzYIzHWPkFJ2B/pub?gid=0&single=true&output=csv"
def addmeta():
    arg_parser = argparse.ArgumentParser(description='Process some integers.')
    arg_parser.add_argument('-u', '--uri', dest='URI', required=True)
    arg_parser.add_argument('-i', '--input', dest='inputfile', required=True)
    arg_parser.add_argument('-c', '--csv', dest='csvfile', required=True)
    arg_parser.add_argument('-o', '--output', dest='outputfile')
    args = arg_parser.parse_args()
    manifest_string = urllib.request.urlopen(args.inputfile).read().decode('utf-8')
#    manifest_file = open(args.inputfile, "r", encoding='utf-8')
#    manifest_string = manifest_file.read()
#    manifest_file.close()
    manifest = json.loads(manifest_string)

    # replace or add structures to manifest
    del manifest["structures"]
    manifest["structures"] = [{
        "id": f"{args.URI}/ranges",
        "type": "Range",
        "label": {
            "en": ["Table of Contents"]
        }
    }]
    with open(args.csvfile, encoding='utf-8') as metadata_file:
        metadata_reader = csv.reader(metadata_file)
        # Skip first line (header)
        next(metadata_reader, None)
        accumulator = []
        items = []
        for i, metadata in enumerate(metadata_reader):
            page = metadata[0]
            canvas = metadata[1]
            label = metadata[2]
            level = metadata[3]

            # Add a range if there's a label and a level
            if label != "" and level != "":
                item = {
                    "id": f"{args.URI}/ranges/{i+1}",
                    "type": "Range",
                    "label": {
                        "en": [label]
                    },
                    "items": [{
                        "id": f"{args.URI}/canvas/{page}",
                        "type": "Canvas"
                    }]
                }
                # recursivley add ranges based on level.
                def storeAtLevel(lv, obj):
                    if (lv == 0):
                        obj.append(item)
                        return obj
                    for n in range(lv+1):
                        # if not isinstance(obj["items"], list):
                        #     obj["items"] = []
                        return storeAtLevel(lv-1, obj[-1]["items"])
                items.append(storeAtLevel(int(level), accumulator))
            manifest["structures"][0]["items"] = items[0]

            # Adjust Canvas label
            for item in manifest["items"]:
                if item["type"] == "Canvas":
                    if item["id"] == f"{args.URI}/canvas/{page}":
                        item["label"] = {
                            "none": [canvas]
                        }
    outputfile = args.outputfile
    if not outputfile:
        manifest_base = os.path.basename(args.inputfile)
        manifest_filename = os.path.splitext(manifest_base)[0]
        outputfile = f"{manifest_filename}_metadata.json"
        print(f'Wrote {outputfile}')
    with open(outputfile, 'w', encoding='utf-8') as outfile:
        json.dump(manifest, outfile, indent=2, ensure_ascii=False)
if __name__ == "__main__":
    addmeta()