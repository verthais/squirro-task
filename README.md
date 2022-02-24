# Squirro text project

## Api

Application exposes three endpoints

Request:
```
GET /text/{id}
```
Response:
```
{
    "text_id": string,
    "text": string,
}
```

Request:
```
POST /text {'text': 'content'}
```
Response:
```
{
    "text_id": string,
}
```

Request:
```
GET /summary/{text_id}
```
Response:
```
{
    "id": string,
    "summary": string,
    "text_id": string,
}
```

## Setup

### Download

clone the repository from github

```
git clone TODO: setup github rep
```

### Environment

```
python -m virtualenv env-squirro
```

then activate virtual environment

#### Windows

```
env-squirro\Scripts\activate
```

#### Linux

````
. env-squirro/bin/activate
````

#### Dependencies

Upgrade pip just in case

```
python -m pip install --upgrade pip
```

then install all the dependencies

```
python -m pip -r requirements.txt
```

### Launch the tests

Run in the main folder

```
python -m pytest
```

### Launch the flask server

```
python ./app.py
```

