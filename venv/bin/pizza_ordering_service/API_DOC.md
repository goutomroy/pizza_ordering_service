### Base Uri
`http://127.0.0.1:8000/api`

### 1. Initial data  

* Endpoint : `/utils/initials/`
* Method : `GET`
* Optional url Parameter :
	- last_synced_at : `String` (Don't add this first time)

* Success response:
  
```json
{
    "order_status_choices": [
        [
            1,
            "Submitted"
        ],
        [
            2,
            "In Production"
        ],
        [
            3,
            "Travelling"
        ],
        [
            4,
            "Delivered"
        ],
        [
            5,
            "Cancelled"
        ]
    ],
    "pizza_size_choices": [
        [
            30,
            "30cm"
        ],
        [
            60,
            "60cm"
        ],
        [
            100,
            "100cm"
        ]
    ],
    "last_synced_at": 1573033466.124189,
    "pizza_choices": [
        {
            "id": 1,
            "flavor": "Berry"
        },
        {
            "id": 2,
            "flavor": "Orange"
        }
    ]
}

```
* Error response   
Http 304(Not Modified) or 500(Internal server error)
```json
    {
        "detail": "message"
    }
```

### 2. Create order
Create an order including pizzas(flavour, size, quantity).

* Method : `POST`  

* Api Endpoint : `/v1/order/`   

* Json Payload Format :  
```json
{
    "user": 1,
    "order_pizza": [
        {
            "pizza": 1,
            "size": 30,
            "quantity": 2
        }
    ]
}
```

* Success Response :  
```json
{
    "id": 23,
    "user": 1,
    "status": 1,
    "order_pizza": [
        {
            "id": 48,
            "pizza": 1,
            "size": 30,
            "quantity": 2
        }
    ]
}
```

### 3. Add or update pizza of an order 
Add new pizza or update existing pizza 
properties(flavour, size, quantity) of an order. Do not include `status` in payload.

* Method : `PUT`  

* Api Endpoint : `/v1/order/7/`   

* Json Payload Format for adding new pizza :  
```json
{
    "user": 1,
    "order_pizza": [
        {
            "pizza": 1,
            "size": 30,
            "quantity": 2
        }
    ]
}
```

* Json Payload Format for updating existing pizza :    
```json
{
    "user": 1,
    "order_pizza": [
        {
            "id" : 15,
            "pizza": 1,
            "size": 30,
            "quantity": 2
        }
    ]
}
```
* Success Response :  
```json
{
    "id": 23,
    "user": 1,
    "status": 1,
    "order_pizza": [
        {
            "id": 48,
            "pizza": 1,
            "size": 30,
            "quantity": 2
        }
    ]
}
```

### 4. Retrieve/List/Filter orders
Retrieve all the orders at once and filter by status/customer.  

* Method : `GET`  
* Api Endpoint :   
`/v1/order/`  
`/v1/order/7/`  
`/v1/order/?user=1`  
`/v1/order/?status=4`  
`/v1/order/?user=1&status=1` 

* Optional url Parameter :
	- user : `int`  
	- status : `int`  

* Success Response :   
```json
[
    {
        "id": 23,
        "user": 1,
        "status": 1,
        "order_pizza": [
            {
                "id": 48,
                "pizza": 1,
                "size": 30,
                "quantity": 2
            }
        ]
    },
    {
        "id": 22,
        "user": 1,
        "status": 1,
        "order_pizza": [
            {
                "id": 44,
                "pizza": 1,
                "size": 30,
                "quantity": 2
            }
        ]
    }
]
```

### 5. Change order status  
This api basically would be used by admin users and customer(to cancel order).  
You will get http 400 either status is cancelled or delivered or if you try to downgrade status or if its in process but you want to cancel it.
* Method : `PATCH`  

* Api Endpoint : `/v1/order/7/`

* Json Payload Format :   
```json
{
    "status": 2
}
```

* Success Response :  
```json
{
    "id": 23,
    "user": 1,
    "status": 1,
    "order_pizza": [
        {
            "id": 48,
            "pizza": 1,
            "size": 30,
            "quantity": 2
        }
    ]
}
```

* Error Response :  
Http 400 - bad request  
```json
[
    "Status can't be downgraded."
]
```

### 6. Delete an order  

* Method : `DELETE`  

* Api Endpoint : `/v1/order/7/`

* Success Response :  
Status Code : 204 - No Content
