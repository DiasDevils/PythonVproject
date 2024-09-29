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
![Coding Logic](logicexcel.png)
First I had to understand what a user would need and how it would actually work to calculate a stock.
For this I used google sheet that was to collect the deliveries and usages and then these data points would be used to calculate the stock. This google sheet was paramount to the design of how the application would work and the logic from how it should operate in a manual setting was applied or transferred to the application.
## Flow chart
![Vacstock Logic and User charts.](vacstock.drawio.png)
I drew this chart to understand and clarify how the program was going to work. This design on flow chart helped ne comprehend and guide me to bring the application to fruition. A clearly defined flow helped code and have the correct flow.
Both the google sheet flow calculation and the flow design paved the way for the application to work.
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

