# Project setup instructions.
 - Create Django Project by using command: django-admin startproject project .
 - Create Django Apps: python manage.py startapp patient, registered_users
 - Registered Apps in INSTALLED_APPS list settings.py file which is in project directory
 - Create Database Models
 - To run server: python manage.py runserver
 - To Create REST API: Models are serialized(python object to JSON object) and using those serializers CRUD Operation logics are written in API View.

# Challenges you faced and how you overcame them.
 - Since most of the features I have used in this project was already implemented by me so to be honest I didn't face much challenges.

# Any additional features or improvements you added.
 - Used JWT Tokens for user Authentication.
 - Implemented Logger to keep track of code in case of some errors occurred.
 - Containerized the application using docker.
 - Used CI/CD for continues deployment.
 - Implemented Pagination in List View.

# Explain in your own words how would the process of deployment to AWS look like?
 - So far I have used EC2 and S3 buckets services of AWS.
 - To deploy this project in EC2 first of all we have to launch EC2 instance and select instance type like nano, micro according to the size of 
   application.
 - Then we have to create key, pair which is used for authentication. (.pem file is created for linux users)
 - Then in Network Setting, we have to add Security Group Rule like Port Range - 8500
 - Next Step is to Configure Storage (Elastic Box Storage)
 - Then Launch Instance.
 - Copy .pem file.
 - Copy ssh file
 - Clone Git Repository.
 - Then install requirements.txt
 - Run application by using command: python manage.py runserver
 - For Permanent Deploy: nohup python manage.py runserver
 - To Stop Application: kill PID