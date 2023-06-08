from graphql import GraphQLError

from api.models import Book, Author, Category


def sync_book_delete(book_id):
    try:
        deleted = Book.objects.get(pk=book_id).delete()
        return deleted
    except Exception as e:
        raise GraphQLError(f'Could not delete book: {str(e)}')


def sync_book_create(volume_info, source_id):
    # check if authors exist in database, otherwise create them
    google_authors = volume_info.get('authors', [])
    local_authors = []
    for author in google_authors:
        local_author, _ = Author.objects.get_or_create(name=author)
        local_authors.append(local_author)

    # check if categories exist in database, otherwise create them
    google_categories = volume_info.get('categories', [])
    local_categories = []
    for category in google_categories:
        local_category, _ = Category.objects.get_or_create(title=category)
        local_categories.append(local_category)

    # create Book
    try:
        import pdb
        params = {
            'title': volume_info.get('title', ''),
            'subtitle': volume_info.get('subtitle', ''),
            'published_date': volume_info.get('publishedDate', ''),
            'editor': volume_info.get('editor', ''),
            'description': volume_info.get('description', ''),
            'image': volume_info.get('imageLinks', {}).get('thumbnail', '')
        }
        book_exists = Book.objects.filter(original_source='google', original_source_id=source_id).exists()
        if not book_exists:
            params['original_source'] = 'google'
            params['original_source_id'] = source_id
            book = Book.objects.create(**params)
            for author in local_authors:
                book.authors.add(author.id)
            for category in local_categories:
                book.categories.add(category.id)
            return book
        else:
            raise GraphQLError(f'Book already exists')
    except Exception as e:
        raise GraphQLError(f'Could not create book: {str(e)}')
