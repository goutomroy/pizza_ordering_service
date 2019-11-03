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

#### Tasks
	1. Design the model / database structure, use PostgreSQL for a backend with Django.
	2. Design and implement an API with the Django REST framework for the web service described above.
	3. Write test(s) for at least one of the API endpoints that you implemented.
	4. Write a brief README with instructions on how to get your code from Git clone to up and  running on macOS and/or Linux hosts

#### Please note!
	• Use Docker, Python 3.6+ and the latest releases of Django, Django REST framework etc.
	• You don't have to take care of authentication etc, we are just interested in structure and data modeling.
	• You don't have to implement any frontend UI, just the API endpoints.
	• Use viewsets where possible.
	• Keep your endpoints as RESTful as possible.
