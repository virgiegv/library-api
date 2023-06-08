from fastapi.testclient import TestClient

from api.models import Book
from library.asgi import fastapp as app

DEFAULT_GRAPHQL_URL = "/graphql/"


class GrapheneTestClientMixin(object):
    client = TestClient(app)

    async def graphql_query(
            self,
            query,
            operation_name=None,
            input_data=None,
            variables=None,
            headers=None,
            client=None,
            graphql_url=DEFAULT_GRAPHQL_URL,
    ):
        if client is None:
            client = self.client

        body = {'query': query}
        if operation_name:
            body['operationName'] = operation_name
        if variables:
            body['variables'] = variables
        if input_data:
            if 'variables' in body:
                body['variables']['input'] = input_data
            else:
                body["variables"] = {"input": input_data}
        if headers:
            resp = client.post(graphql_url, json=body, headers=headers)
        else:
            resp = client.post(graphql_url, json=body)
        return resp

    async def search_query(
            self,
            title=None,
            subtitle=None,
            authors=None,
            categories=None,
            editor=None,
            published_date=None,
            book_description=None
    ):
        variables = {
            'title': title,
            'subtitle': subtitle,
            'publishedDate': published_date,
            'editor': editor,
            'bookDescription': book_description,
            'authors': authors,
            'categories': categories
        }
        query = '''
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
        '''

        response = await self.graphql_query(query, variables=variables)
        return response

    async def create_book_mutation(self, book_id, source):
        variables = {
            "bookId": book_id,
            "source": source
        }
        query = '''
            mutation createBook ($bookId: String!, $source: String! ) {
                createBook(bookId: $bookId, source: $source) {
                    ok
                    title
                    bookId
                }
            }
        '''
        response = await self.graphql_query(query, variables=variables)
        return response

    async def delete_book_mutation(self, book_id):
        variables = {
            "bookId": book_id,
        }
        query = '''
            mutation deleteBook ($bookId: ID!) {
                deleteBook(bookId: $bookId) {
                    deleted
                }
            }
        '''
        response = await self.graphql_query(query, variables=variables)
        return response

    def get_first_book(self):
        book_ids = list(Book.objects.all().values_list('id', flat=True))
        return min(book_ids)
