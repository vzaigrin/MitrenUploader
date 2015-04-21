# MitrenUploader
This is a script on Python3 for creating an assessment and uploading data to Mitrend.com

This script take an options:
- -v -- verbose output
- -c inifile -- initialization file with description of an assessment

Inifile should has sections:
- user -- description a user of Mitrend: username and password
- assessment -- description an assessment: name, company, city, country
- files -- description of file to upload: device type and filename
 
Filename should have a path to file where script can read it.
