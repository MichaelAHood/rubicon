#!/usr/bin/env bash

wget https://chromedriver.storage.googleapis.com/100.0.4896.60/chromedriver_mac64.zip -O chromedriver.zip

unzip chromedriver.zip
chmod 755 chromedriver
mv chromedriver /usr/local/bin
rm chromedriver.zip