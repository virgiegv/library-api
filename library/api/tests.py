from asgiref.sync import sync_to_async

import pytest

from api.external_api_utils import GOOGLE_BOOKS_SOURCE, LOCAL_DB_SOURCE
from api.models import Author, Category, Book
from api.test_utils import GrapheneTestClientMixin

pytestmark = pytest.mark.django_db(
    databases=['default'], transaction=True
)


@pytest.fixture
def load_test_data():
    homer = Author.objects.create(name='Homer')
    descartes = Author.objects.create(name='Descartes')
    rowling = Author.objects.create(name='JK Rowling')

    philosophy = Category.objects.create(title='Philosophy')
    history = Category.objects.create(title='History')
    fantasy = Category.objects.create(title='Fantasy')
    adventure = Category.objects.create(title='Adventure')

    illyad = Book.objects.create(
        title='Illiad',
        subtitle='The war',
        published_date='unknown',
        editor='unknown',
        description='The Trojan war',
        image='www.images.com/illiad.jpg'
    )
    illyad.authors.add(homer)
    illyad.categories.add(history)
    illyad.categories.add(fantasy)
    illyad.save()

    method = Book.objects.create(
        title='Discourse on the Method',
        subtitle='of Rightly Conducting Ones Reason and of Seeking Truth in the Sciences',
        published_date='1637',
        editor='unknown',
        description='One of the most influential works in the history of modern philosophy',
        image='www.images.com/rene.jpg'
    )
    method.authors.add(descartes)
    method.categories.add(history)
    method.categories.add(philosophy)
    method.save()

    hp = Book.objects.create(
        title='Harry Potter and the Philosophers Stone',
        subtitle='',
        published_date='1997-06-26',
        editor='Bloomsbury',
        description='Harry Potter, a young wizard who discovers his magical heritage on his eleventh birthday, '
                    'when he receives a letter of acceptance to Hogwarts School of Witchcraft and Wizardry.',
        image='www.images.com/hp.jpg'
    )
    hp.authors.add(rowling)
    hp.categories.add(fantasy)
    hp.categories.add(adventure)
    hp.save()


class TestSearchBooks(GrapheneTestClientMixin):
    @pytest.mark.asyncio
    async def test_search_existing_book(self, load_test_data):
        response = await self.search_query(
            title='harry',
            published_date='1997',
            book_description='wizard'
        )

        data = response.json().get('data')

        assert len(data['search']['results']) > 0
        hp_source = data['search']['results'][0]['source']
        assert hp_source == LOCAL_DB_SOURCE

    @pytest.mark.asyncio
    async def test_search_google_books(self, load_test_data):
        response = await self.search_query(
            title='test book',
        )
        data = response.json().get('data')

        assert len(data['search']['results']) > 0
        hp_source = data['search']['results'][0]['source']
        assert hp_source == GOOGLE_BOOKS_SOURCE

    @pytest.mark.asyncio
    async def test_add_book(self):
        test_google_id = 'lciEAAAAQBAJ'

        response = await self.create_book_mutation(test_google_id, GOOGLE_BOOKS_SOURCE)
        data = response.json().get('data')

        assert data['createBook']['ok']

    @pytest.mark.asyncio
    async def test_add_repeated_book_fail(self):
        test_google_id = 'lciEAAAAQBAJ'

        response = await self.create_book_mutation(test_google_id, GOOGLE_BOOKS_SOURCE)
        data = response.json().get('data')
        assert data['createBook']['ok']

        response = await self.create_book_mutation(test_google_id, GOOGLE_BOOKS_SOURCE)
        data = response.json().get('data')
        assert data['createBook'] is None

    @pytest.mark.asyncio
    async def test_delete_book(self, load_test_data):
        book_id = await sync_to_async(self.get_first_book)()

        response = await self.delete_book_mutation(book_id)

        data = response.json().get('data')
        assert data['deleteBook']['deleted']

    @pytest.mark.asyncio
    async def test_delete_fake_book_fail(self):
        response = await self.delete_book_mutation(99999)
        data = response.json().get('data')
        assert data['deleteBook'] is None
