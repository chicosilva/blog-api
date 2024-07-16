from django.test import TestCase
from django.utils.text import slugify
from .models import Post, CustomUser


class PostModelTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.post = Post.objects.create(
            title='Test Post',
            slug=slugify('Test Post'),
            author=self.user,
            text='This is a test post.',
            status=0
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.slug, 'test-post')
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.text, 'This is a test post.')
        self.assertEqual(self.post.status, 0)

    def test_post_str(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_slug_unique(self):
        with self.assertRaises(Exception):
            Post.objects.create(
                title='Test Post',
                slug=self.post.slug,
                author=self.user,
                text='This is another test post.',
                status=0
            )

    def test_post_update(self):
        self.post.title = 'Updated Post'
        self.post.save()
        self.assertEqual(self.post.title, 'Updated Post')

    def test_post_delete(self):
        self.post.delete()
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=self.post.id)
