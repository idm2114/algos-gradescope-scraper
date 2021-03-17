# Algos Web Scraper

### Setup

In order to set up this project, you need to install chromedriver to your local path.
You should also install all required python packages.
Then, all you have to do is input your gradescope username and password
into the global variables at the top and you should be good to go!

### Notes on this script

Currently, this script is designed to run forever (i.e. it will sleep when
not checking for a quiz and run indefinitely). In order to set this up
semi-gracefully, I recommend using nohup and calling the script at the 
command line as follows:

nohup python3 -u gradescope-py &

This command will allow it to run in background. You could also set this 
up however you want (whatever works for you!). Just keep in mind that since
this script is very clunky with a hardcoded NUMQUIZ variable, if you interrupt
or abort the script at any point, that value will be reset to the original 
hardcoded value (currently 11). I am working to fix the script in general so 
that this is not the case in the future.
