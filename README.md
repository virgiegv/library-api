# library-api

## Installation

After cloning repository, go to library-api/library

Create a virtual environment:
```bash
pip install virtualenv
virtualenv <env_name>
source <env_name>/bin/activate
```

Install requirements:
```bash
pip install -r requirements.txt
```

Install PostgreSQL as required for your distro, then create the database:
```bash
sudo -iu postgres
initdb --locale $LANG -E UTF8 -D '/var/lib/postgres/data/'
exit
sudo systemctl enable --now postgresql.service
```

The project is not yet in production, so the following names of databases and users are just an example to set up the database locally. 

```bash
sudo su - postgres
psql
CREATE DATABASE library;
CREATE USER library WITH PASSWORD 'library';
GRANT ALL PRIVILEGES ON DATABASE library TO library;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO library;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO library;
ALTER USER library CREATEDB;
\q
exit 
```

Create a .env file with the following env vars. Their values are based simply on how we've set up our local database so far, production values don't exist for the project.
```bash
DB_ENGINE=django.db.backends.postgresql
DB_PORT=5432
DB_HOST=localhost
DB_NAME=library
DB_USERNAME=library
DB_PASSWORD=library
```

Run migrations:
```bash
python manage.py migrate
```

Run server:
```bash
uvicorn library.asgi:fastapp --host=0.0.0.0 --reload
```

Run tests:
```bash
pytest --cov --ds=library.settings api/tests.py
```
## How to use:

This is a GraphQL API. There are three functionalities available: 
1. Search for a book in the local database, if there are no results then search in Google Books
2. Use the id of a Google Books result to add the same book to the local database
3. Delete a book from the local database using the local id of the book 

Integrating a second external API as a source for new books has currently fallen out of the scope for this project for time contraints, although it can soon be integrated. 

Once running locally, you can access the GraphQL endpoint at: 127.0.0.1:8000/graphql

### 1. Searching for a book:
Query:
```bash
query search(
    $title: String, $subtitle: String, $authors: String, 
    $categories: String, $editor: String, $publishedDate:String, 
    $bookDescription: String ) {
        search (title: $title, subtitle: $subtitle, authors: $authors, 
        categories: $categories, editor: $editor, publishedDate: $publishedDate, bookDescription: $bookDescription) {
            results {
                source
                bookId
                title
                subtitle
                editor
                publishedDate
                image
                authors
                categories
            }
        }
    }
 ```   
Variables:
```bash
{
    "title": "example",
    "subtitle": ...,
    "authors": "example name",
    "categories": "fiction",
    "editor": ...,
    "publishedDate": ...,
    "bookDescription":...,   
}
```
Only send the variables that you actually want to query by. Any variable you don't wish to use, simply remove from the json. 

You can also use the following cURL to import into Postman as an example:
```bash
curl --location --request POST '127.0.0.1:8000/graphql' \
--header 'Content-Type: application/json' \
--data-raw '{"query":"query search(\n    $title: String, $subtitle: String, $authors: String, \n    $categories: String, $editor: String, $publishedDate:String, \n    $bookDescription: String ) {\n        search (title: $title, subtitle: $subtitle, authors: $authors, \n        categories: $categories, editor: $editor, publishedDate: $publishedDate, bookDescription: $bookDescription) {\n            results {\n                source\n                bookId\n                title\n                subtitle\n                editor\n                publishedDate\n                image\n                authors\n                categories\n            }\n        }\n    }","variables":{"title":"example"}}'
```

### 2. Add Book using Google Books ID:
If you use the previous query, most likely the database will be empty, so the results will come from Google Books, as denoted by the field 'source' in the response. There we can also find 'bookId', which we can use paired with the source to identify a single book and add it to our local database. 

Query:
```bash
mutation createBook ($bookId: String!, $source: String! ) {
   createBook(bookId: $bookId, source: $source) {
     ok
     title
     bookId
   }
}
```

Variables:
```bash
{
    "bookId": "3txgDQAAQBAJ",
    "source": "google"
}
```

Example cURL:
```bash
curl --location --request POST '127.0.0.1:8000/graphql' \
--header 'Content-Type: application/json' \
--data-raw '{"query":"mutation createBook ($bookId: String!, $source: String! ) {\n   createBook(bookId: $bookId, source: $source) {\n     ok\n     title\n     bookId\n   }\n}","variables":{"bookId":"3txgDQAAQBAJ","source":"google"}}'
```

### 3. Delete Book from local db:
Any book that has been created using the previous mutation can be eliminated using the bookId provided in the response. If we use the first query and the results come from our local database, that response's bookId will be the same. 

Query:
```bash
 mutation deleteBook ($bookId: ID!) {
  deleteBook(bookId: $bookId){
    deleted
  }
}
```

Variables:
```bash
{
    "bookId": 6
}
```

Example cURL:
```bash
curl --location --request POST '127.0.0.1:8000/graphql' \
--header 'Content-Type: application/json' \
--data-raw '{"query":" mutation deleteBook ($bookId: ID!) {\n  deleteBook(bookId: $bookId){\n    deleted\n  }\n}","variables":{"bookId":6}}'
```
