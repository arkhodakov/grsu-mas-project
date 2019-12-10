# MAS System - Course Work Makarova - GRSU 2019

## Setup instructions

Perform next steps:
1. In _root_ directory. Install npm packages: ```npm install```
2. Install Python packages:
    * __osBrain__ -> ```pip install osbrain```
    * __Flask__ -> ```pip install flask```
    * __Google Search Result__ -> ```pip install google-search-results```

## Launch instructions

### Production

Perform next steps:
1. In _'mas'_ directory. Run Python webserver: ```python ./run.py```
2. In _'mas-server-agents'_ directory. Run Python osBrain server: ```python ./server.py```


### Development

This way you'll be able to edit code on fly. All changes made with project files will automatically invoke project build.

Perform next steps:

1. In _'mas/static'_ directory. Run webpack server builder: ```npm run watch```
1. In _'mas'_ directory. Run Python webserver: ```python ./run.py```
2. In _'mas-server-agents'_ directory. Run Python osBrain server: ```python ./server.py```
