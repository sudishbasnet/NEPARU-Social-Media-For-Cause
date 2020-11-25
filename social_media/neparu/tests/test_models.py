from django.test import TestCase
from neparu import models


class UserTestCase(TestCase):
    def test_string_representation(self):
        entry = models.User(username='sudish1',
          first_name = 'sudish',
          last_name = 'basnet',
          email='author@test.com',
          account_type = 'private',
          password = 'Blabitw1234',)
        self.assertEqual(str(entry), entry.username)



class PostTestCase(TestCase):
    def test_string_representation(self):
        entry = models.Post(title='Hello')
        self.assertEqual(str(entry), entry.title)




class CommentTestCase(TestCase):
    def test_string_representation(self):
        entry = models.Comment(content='Hello')
        self.assertEqual(str(entry), entry.content)


class InboxTestCase(TestCase):
    def test_string_representation(self):
        user = models.User(username='sudish1',)
        user1 = models.User(username='sudish',)
        entry = models.Inbox(sender=user,message='hy',receiver=user1)
        self.assertEqual(str(entry), entry.sender.username)



class RentalTestCase(TestCase):
    def test_string_representation(self):
        entry = models.Rental(title='Hello')
        self.assertEqual(str(entry), entry.title)


class NotificationTestCase(TestCase):
    def test_string_representation(self):
        entry = models.Notification(content='Liked photo',action=='Like')
        self.assertEqual(str(entry), entry.action)