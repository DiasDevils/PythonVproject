# PythonVproject PP3

PythonVproject is a Flu Vaccine Stock Tracking System designed to run on the render platform. This system is aimed at helping any medical practice that deals with vaccines to track their stock.

[Visit My Website](https://pythonvproject.onrender.com/)

## Disclaimer:
1. This project used the Code Institute student template for deploying my third portfolio project using Python command-line. The last update to the template file was: **May 14, 2024**.
2. This application is not all comprehensive. There is more development to be done. Due to the scope of this project and time constraints I am satisfied with the current development and features which satisfy the project goals.

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

-------------------------------------------------------------------------
## Purpose
 This Flu Vaccine Stock Tracking (FVST) System is aimed at helping any medical practice that deals with vaccines to track their stock. The users can see their stock, record the deliveries and usage and know how much stock they have in date or expired. This system is aimed to help manage/trace orders and usage for reporting purposes like for example statistics to the health department. These type of systems are invaluable to organisations like the HSE in the world. Current systems in place may lack important validation rules and therefore rendering statistical data of vaccinations incorrect.

## User Experience
As the creator of the application and user I needed and wanted to make sure of the following:
* the user to find the system easy to navidate and easy to understand
* the user to have instructions and limitation information where necessary
* the user to be aware of steps and validation steps for when incorrect data was entered
* maintain the user informed along every step
* for data to be visible when it was requested
* ability to exit the application
* easy to navigate menu

The user of this application will be a person in the medical sphere that must record deliveries and usage of vaccines. This way at the end of the month they have information that could be passed to a main institution and statistical information pulled from the data available. The application is to be very easy to use and not tedious. Steps to be skipped if necessary.

## Code logic
![Coding Logic](logicexcel.png)
First I had to understand what a user would need and how it would actually work to calculate a stock.
For this I used a google sheet that was to collect the deliveries and usages and then these data points would be used to calculate the stock. This google sheet was paramount to the design of how the application would work and the logic from how it should operate in a manual setting was applied/transferred to the application. This step was crucial in the design.

## Flow chart
![Vacstock Logic and User charts.](vacstock.drawio.png)
I drew this chart to understand and clarify how the program was going to work. This design on flow chart helped ne comprehend and guide me to bring the application to fruition. A clearly defined flow helped code and have the correct flow.
Both the google sheet flow calculation and the flow chart design paved the way for the application to function correctly.
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

#### Development 
The code was going from simple step to step to more complex logic. It started simple and then I came across many bugs as stated above. These bugs were only visible after user testing and requesting individuals to play with the application and think of possibilities that I did not think about. Even with these bugs there is at least one bug that I have thought about but do not have the time frame to cover in this project. The delivery date and expiration date is far more complex than just added 30 days to the delivery. In fact, my logic adds 30 days to the last delivery but it does not account for the old delivery to be sure out of date and therefore expired. More testing and more development is required to perfect this application and more complex logic is required to cover these refined detail on expiration.


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

