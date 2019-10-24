#!/bin/bash

if [ ! -d "$(pwd)/output" ]; then
  mkdir $(pwd)/output
fi

if [ ! -d "$(pwd)/output/$1" ]; then
  mkdir $(pwd)/output/$1
fi

python3 -c "import api_download; api_download.download(\"/Backup/$1$2\",\"$(pwd)/output/$1$3\")"
