# CSULB Classroom Finder 
__***Brief description of the program:***__
 - There are two web crawlers to build the database:
   -  The first scrapes the data needed such as class start time, class end time, location for all the classes offered during a given semester from the school's schedule website and store them in a database. 
	 - The second finds all the rooms and buildings in the university and stores them in the database. 
 - Django app that helps students to find a classroom/lab to study at the time and location of their convince across the campus using the data from the database.

__***TODO:***__
- **Clean up the code** (as this is a temporary branch and doesn't have the final code)
- Add hitcounter 
- ~~Host the website on Ubuntu server and use nginx as a web server. Replace DDNS with DNS domain 
- Add all possible locations available for students to study and get help such as tutoring and student support locations. 
- Integrate the scraper with an admin panel to update the database every semester
- Add user feedback page 
- Ultimately support more schools 
