# wikisearch_api

#### Repository Name: wikisearch_api


## Installation and Configuration

Before you begin, ensure you have met the following requirements:

- Python (version 10)

### Step 1: Clone the Repository
git clone https://github.com/mehrangeeky/wikisearch_api.git
### Step 2: Create a Virtual Environment
python3 -m venv venv

### Step 3: Activate the Virtual Environment (Windows)
venv\Scripts\activate

### Step 3: Activate the Virtual Environment (macOS and Linux)
source venv/bin/activate

### Step 4: Install Dependencies
pip install -r requirements.txt


#### Debug mode (Set to True for development, False for production)

DEBUG=True


### Step 5: Apply Database Migrations
python manage.py makemigrations

python manage.py migrate

### Step 7: Start the Server
python manage.py runserver

## Usage

- Create a superuser and login
    
    `python manage.py createsuperuser`

- enter username and password.
    
    **`Start the development server`**
        
        python manage.py runserver


# Endpoints

## Word Frequency Endpoint

### URL

`POST search/word-frequency/`

### Request Body

- **title** (string): Title of the Wikipedia article.
- **num_words** (integer): Number of most common words to retrieve.

#### Example

```json
{
  "title": "Python (programming language)",
  "num_words": 5
}
```

### Response
```json
{
  "most_common_words": {
    "Python": 10,
    "Django": 8,
    "API": 5,
    "Framework": 3,
    "Programming": 2
  }
}
```

## Search History Endpoint

### URL

`GET search/history/`

### Response
```json
[
  {
    "id": 1,
    "user": "john_doe",
    "article": "Python (programming language)",
    "word_count": 5,
    "word_frequency": {
      "Python": 10,
      "Django": 8,
      "API": 5
    },
    "created_at": "2024-02-06"
  },
  {
    "id": 2,
    "user": "jane_smith",
    "article": "Machine Learning",
    "word_count": 7,
    "word_frequency": {
      "Machine": 12,
      "Learning": 10,
      "Algorithm": 8
    },
    "created_at": "2024-02-05"
  }
]
```
