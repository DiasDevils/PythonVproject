# PythonVproject PP3

PythonVproject is a Flu Vaccine Stock Tracking System designed to run on the render platform. This system is aimed at helping any medical practice that deals with vaccines to track their stock. The users can see their stock, record the deliveries and usage and know how much stock they have in date or expired. This system is aimed to help manage/trace orders and usage for reporting purposes like for example statistics to the health department.

[Visit My Website](https://pythonvproject.onrender.com/)

## Disclaimer:
This project used the Code Institute student template for deploying my third portfolio project using Python command-line. The last update to the template file was: **May 14, 2024**.

## Content 
* Purpose
* User Experience
* Code logic
* Flow chart
* Data storage
* Features 
* Future features
* Technologies used 
* Python Packages used
* Testing
* Deployment and Development( cloning repository / APiS)
* Credits
* Acknowledgements 


# ORDER
## Purpose
## User Experience
## Code logic
![Flow Chart ](VacStock.drawio.png)
Used google sheet to calculate how it would work and applied that to the logic.
## Flow chart
## Data storage
## Features 
## Future features
## Technologies used 
## Python Packages used
## Testing 
![CodeTest](<python authenticator pep8ci.png>)
Received a couple of white space errors such as W291(trailing whitespace), W293 (blank line contains white space).
Received E501 error (line too long).
Received E302 error (expecting white line but 0 found).

### User Testing 
Requested several people to try the application. Several bugs in the logic were discovered.
- usage could exceed delivery - bug fixed
- dates could be in the past - bug fixed
- dates could be in the future - bug fixed
- quantities could be a minus number - bug fixed
- the main menu was tedious as one had to go through entire process and could not skip steps - bug fixed
- batch number could be a negative number - bug fixed 
- quantity allowed to order was missing - bug fixed

## Deployment and Development( cloning repository / APiS)
#### Guidelines followed:
- Code placed in the `run.py` file
- Dependencies placed in the `requirements.txt` file
- Added to the `requirements.txt` file as required per project
- Did not edit any other files or code may not have deploy properly
- Edited coe to deploy on render
- Ignored too long error E501 as deployed on Render not Hiroku
#### Creating the Render app
Created Environment variables in Render in Settings
1. 'Port' 8000
2. 'nodejs`
3. 'credentials'
4. 'something else'
Had credentials `CREDS` and paste the JSON into the value field.
Connect your GitHub repository and deploy as normal.
#### Issues on deployment 
Encountered many issues on the render app but was able to figure it out eventually.
Used the document given by student services but not all the inforamtion was in the instructions.
Figured out other environmental varaibles had to be introduced.
#### Connecting GCP/API


## Credits
Code Institute code template.
Code Institute student support.
Google and Open AI for problem resolution.

## Acknowledgements 
My mentor Richard Wells and the student support staff for render help.





## Constraints

