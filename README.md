Flask API CRUD Phone book
-----

Installation
--

Clone the repository into a new folder and switch to project root :   
```
git clone https://github.com/MargaritaPopova/phone-book.git
cd phone-book
```

Create virtualenv and activate it
```
# by virtualenv
python3 -m venv <your-venv-name>
source <your-venv-name>/bin/activate
```

Install requirements
```
pip install -r requirements.txt
```

run script to create & fill database:
``` 
python build_database.py
```

run app:
```
python app.py
```

Usage
---
Go to http://0.0.0.0:5000/ for browsable API 

### Making requests


URL: http://0.0.0.0:5000/api/phones  


```GET``` request to get list of phones   
```POST``` request with json data to create new phone number

URL: http://0.0.0.0:5000/api/phones/<int:phone_id>  


```GET``` request to get one number  
```PUT``` request with json data to update a number  
```DELETE``` request to delete a number

#### Examples

**READ**  
```
curl http://localhost:5000/api/phones

# returns:
[
  {
    "first_name": "Lesley",
    "last_name": "Doe",
    "number": "87867675655",
    "phone_id": 2
  },
  {
    "first_name": "Doug",
    "last_name": "Farrell",
    "number": "32497238473",
    "phone_id": 1
  },
  {
    "first_name": "John",
    "last_name": "Link",
    "number": "76353344333",
    "phone_id": 4
  },
  {
    "first_name": "Minnie",
    "last_name": "Marshall",
    "number": "97654333567",
    "phone_id": 3
  }
]


```  
```
curl http://localhost:5000/api/phones/1

# returns:
{
  "first_name": "Doug",
  "last_name": "Farrell",
  "number": "32497238473",
  "phone_id": 1
}

```

**CREATE**  
```
curl --header "Content-Type: application/json" --request POST --data '{"first_name":"Molly","last_name":"Burke","number":"3493855858"}' http://localhost:5000/api/phones

# returns:
{
  "first_name": "Molly",
  "last_name": "Burke",
  "number": "3493855858",
  "phone_id": 5
}

```   

**UPDATE**  
```
curl --header "Content-Type: application/json" --request PUT --data '{"last_name":"Linkoln"}' http://localhost:5000/api/phones/4

# returns:
{
  "first_name": "John",
  "last_name": "Linkoln",
  "number": "76353344333",
  "phone_id": 4
}

```

**DELETE**  
```
curl --request DELETE http://localhost:5000/api/phones/4

# returns:
Phone 76353344333 deleted
```

