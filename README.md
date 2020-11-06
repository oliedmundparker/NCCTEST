# Ncc Test

## requirements
Requirements can be found in requirements.txt

## Instructions

First run
``python3 manage.py makemigrations``
``python3 manage.py migrate``

This will apply all needed DB set up (using sqlite). Then run
``python3 manage.py runserver``
This will start a development server.

## Endpoints
Each object has its own end point at the following addresses:

User:  /user 

Asset: /asset

Scan: /scan

Vulnerability: /vulnerability

These endpoints can handle `GET` and `POST` requests. Additionally, each endpoint has a detail view for accessing individual elements. 

eg.

/scan/1 makes requests against the scan with pk=1. This can handle `GET`, `PUT`, and `DELETE` requests.

## Explanation

I implemented each object as a Django model to start with. This was a minimum requirement. Looking at the data, we had some additional parts that, for flexibility, I also decided to implement as a model. This includes:
1. Scanners. I believe that it makes sense to wrap the scanners in an object so tht they are stored in the DB, have some verification against them, and can be easily added as fields to new models. They are implemented as Many To Many relationships within other objects.
2. Severity Count. Due to this being returned as a dictionary, I figured I either needed to mess with the way the object would be represented in the request, which could create some problems, or encapsulated the severity count in its own model and set up a 1-1 relationship with a scan so that we can treat each separately. I chose to do the later. This also gives us the flexibility to add new tiers of severity down the line and have old scans be supported.

Everything else is, in my view, regular django. I had to override the create/update functions in the serializers for Scan + Vulnerability in order to make sure we dealt with the Many to Many / One to One relationships properly.

## Extensions
There are some other things I would have liked to have done but I feel fell outside the scope of the task.
1. Authentication. In a real world application most of these end points would be authenticated. Scans/Vulnerabilities would only be able to be read by the user who requested the scan & administrators. Additionally we'd also want to ensure only an admin could do put/delete requests.
2. Verification. I would have liked to have added some verification on many elements in the code. E.G, an asset listed in a vulnerability should have to be in the scan the vulnerability is part of. And Start/End times should have some verification to ensure they make sense.

## Update

After I submitted the test I went back to check my code properly and discovered some problems that I should have spotted. You can see from the commit what they were, but to summarise:
1. I assumed the references was always a URL but upon inspection it isn't (its multiple). I decided to change the field to a text field.
2. Some char fields were clearly not long enough. I made these bigger.
3. I had been adding scanners in the admin for my tests but disocvered there was no way to add these through the API. I have added this capbility through the /scanner endpoint.
4. The scanner object was also looking for pk's rather than names. I resolved this, and made their name unique so no error could occur.
5. Choices tuples where the wrong way round, reversed this error.
6. Some field names were incorret from the sample jsons. Corrected.