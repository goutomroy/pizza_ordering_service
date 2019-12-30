#### Description
Implement the following logic using the Django REST framework. 
#### Database Model Structure  
*   Pizza : id, flavour, description.
*   Order : id, user, status, created, updated.
*   Order Items : id, order, pizza, size, quantity.
*   User Profile : id, user, address, created, updated.  

Imagine a pizza ordering services with the following functionality:

	• Order pizzas:
		• It should be possible to specify the desired flavors of pizza, the number of pizzas and their size.
		• An order should contain information regarding the customer.
		• It should be possible to track the status of delivery.
		• It should be possible to order the same flavor of pizza but with different sizes multiple times.
	• Update an order:
		• It should be possible to update the details — flavours, count, sizes — of an order
		• It should not be possible to update an order for some statutes of delivery (e.g. delivered).
		• It should be possible to change the status of delivery.

	• Order:
	    * Create :
	        * Any authenticated user can create.
	    * Get -> get single order :
	        * Only the owner of an order can get specified order.
        * List -> get list of orders :
	        * Any authenticated user can get only his list of orders.
        * Update -> update single order :
	        * Admin, staff can update any order.
	        * Authenticated(not admin or staff) user can update only his order.
        * Partial update -> update single order :
	        * Admin, staff can update any order.
	        * Authenticated(not admin or staff) user can update only his order.
	        
	    * Only order owner, admin,staff can update/delete order.
	    * While updating an order status check status update constrains :
	        * if order status is IN_PRODUCTION then can't be changedd to TRAVELLING, DELIVERED, CANCELED.

    
    
	    * Create order with just user, use retrieved order id to create/update/delete order items.
		• Retrieve an order by its identifier or retrieve all the orders at once.
		• Filter orders by status / customer.
		* Remove order by its identifier, then delete all its order items.

		
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
		


