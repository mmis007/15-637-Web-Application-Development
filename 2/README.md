To turn in homework 2, create files (and subdirectories if needed) in
this directory, add and commit those files to your cloned repository,
and push your commit to your bare repository on GitHub.

Add any general notes or instructions for the TAs to this README file.
The TAs will read this file before evaluating your work.


explain why your app generates either GET or POST requests. Also cite any external resources used and any additional notes you would like to convey to your grader.


The reason I'm using POST rather than GET:
1. the POST requests have no restrictions on data length, while GET requests have. So by using POST, I can send more data

2. the query string is sent in the HTTP message body of a POST request, while the GET is in the url. Using POST is safer, since people cannot get form information from the url. 

3. by using the POST request, the url of the webpage will not change when we sending requests, which makes the webpage cleaner



external resources:
http://www.w3schools.com/

http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000

https://www.djangoproject.com/



explaination of solving invalid input:

1. when user attempts to divide by 0 or send malformed input, the calculator will display an error message until the next button is clicked.

2. when there is an error message displayed, if the user click on digit buttons, the calculator will be restarted; if the user click on the equals button, the screen will be reset to zero; if the user click on operator buttons, the screen will still display error message

3. when the user click several operator buttons, the calculator will only take the last one for calculation;
if the user click equals button right after operator buttons, the calculator will ignore the equals action and wait for the next digit or operator.





