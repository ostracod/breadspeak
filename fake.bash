#!/bin/bash

echo "Faking..."

echo "Converting dictionary to JSON..."
./entryDigest.py getJson

echo "Creating documentation file..."
node ./createDoc.js

echo "Creating word table file..."
node ./createWordTable.js

echo "Creating cheat sheet file..."
node ./createCheatSheet.js

echo "Finished faking."


