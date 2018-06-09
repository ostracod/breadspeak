#!/bin/bash

echo "Faking..."

echo "Converting dictionary to JSON..."
./entryDigest.py getJson

echo "Creating documentation file..."
node ./createDoc.js

echo "Finished faking."


