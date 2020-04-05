# Trivia API

## Introduction

Get access to trivia questions sorted by categories for your app with this API. This API conforms to the REST architectural style. It returns JSON-encoded responses and uses standard HTTP response codes.

## Getting Started

#### 1. Initialize and activate a virtual environment:
Run this in the terminal:
```bash
cd YOUR_PROJECT_DIRECTORY_PATH/
virtualenv --no-site-packages env OR virtualenv env
source env/bin/activate (MacOS/Linux) OR source env/Scripts/activate (Windows)
```

Additional instructions can be found [here](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### 2. Install the dependencies:
In the backend folder directory, run the following:
```bash
pip install -r requirements.txt OR pip3 install -r requirements.txt
```

#### 3. Set up database:
Restore a database using the trivia.psql file provided. In the terminal, connect to psql and create a database called trivia. Then, while in the backend folder directory, run the following:
```bash
psql trivia < trivia.psql OR psql -d trivia -U [username] -f trivia.psql
```
*where [username] is your username

#### 4. Run the server
Still in the backend folder directory, run the following:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

#### 5. Run the app
Navigate to the frontend folder directory and run the following:

```bash
npm start
```

This will automatically launch the app in the web browser with http://localhost:3000 as the address.

## HTTP Status Codes

200 - OK (The request has succeeded)

400 - Bad Request (The server cannot process the request due to a client error)

404 - Not Found	(The requested resource doesn't exist)

422 - Unprocessable Entity (The server was unable to process the request)

## API Endpoints

#### Base URL
> http://localhost:5000

#### Get Trivia Categories (GET Method)
> http://localhost:5000/categories

#### Get Trivia Questions (GET Method)

> http://localhost:5000/questions?category=[CATEGORY_ID]

Returned questions are paginaged, up to 10 per page. The default page number is 1. You can specify the page number like so:

> http://localhost:5000/questions?category=[CATEGORY_ID]&page=[PAGE_NUMBER]

#### Get Trivia Questions By Category (GET Method)

> http://localhost:5000/categories/[CATEGORY_ID]/questions

#### Add Trivia Question (POST Method)
> http://localhost:5000/questions

>Request JSON:  
> {  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'question' : '[QUESTION]',  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'answer' : '[ANSWER]',  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'difficulty' : '[DIFFICULTY]',  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'category' : '[CATEGORY_CODE]',  
> }

#### Search Trivia Question (POST Method)
> http://localhost:5000/questions

>Request JSON:  
> {  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'searchTerm' : '[SEARCH_TERM]'  
> }

Optional - to narrow down by category:

> http://localhost:5000/questions?category_id=[CATEGORY_ID]


#### Delete Trivia Question (DELETE Method)

> http://localhost:5000/questions/[QUESTION_ID]

#### Get Trivia Questions for Quiz (POST Method)

> http://localhost:5000/quizzes

> Request JSON:  
> {  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'previous_questions' : '[IDS_OF_PREVIOUS_QUESTIONS]',  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'quiz_category' : '[CATEGORY_ID]'  
> }

This will randomly select a question from the pool, by category if applicable.

## Author

This documentation was created by Joshua Kagawa