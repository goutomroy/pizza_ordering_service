#### Description
Implement the following logic using the Django REST framework. 
Imagine a pizza ordering services with the following functionality:

	• Order pizzas:
		• It should be possible to specify the desired flavors of pizza, the number of pizzas and their size.
		• An order should contain information regarding the customer.
		• It should be possible to track the status of delivery.
		• It should be possible to order the same flavor of pizza but with different sizes multiple times
	• Update an order:
		• It should be possible to update the details — flavours, count, sizes — of an order
		• It should not be possible to update an order for some statutes of delivery (e.g. delivered).
		• It should be possible to change the status of delivery.
	• Remove an order.
	• Retrieve an order:
		• It should be possible to retrieve the order by its identifier.
	• List orders:
		• It should be possible to retrieve all the orders at once.
		• Allow filtering by status / customer.
		
#### Setup  & Run
* This project was developed in Ubuntu 18.04.  
* This project was developed using Python3.7, Django 2.2.6 and PostgreSQL.   
* Install PostgreSQL database and Redis server.  
* Create a virtual environment and do git clone this repository.  

* Create a new PostgreSQL database  in postgres server

      'NAME': 'pizza_ordering_service',
      'USER': 'postgres',
      'PASSWORD': 'postgres',  

* Install required packages

      pip install -r requirements.txt
    
    
* Migrate the database before the first run:

      python manage.py migrate

* Running the application

      python manage.py runserver

* Load initial data for projects:

      python manage.py loaddata initial.json


* Enter to admin with already created admin user:  

      Username : andre  Password : 123456  

* Run test

      python manage.py test
      
#### Api Documentation  
Check `API_DOC.md`    
		


