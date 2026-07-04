#!/bin/bash

mkdir -p ~/.streamlit/

echo "
[streamlit]
headless = true
port = \$PORT
enableCORS = false
" > ~/.streamlit/config.toml
