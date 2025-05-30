from django.test import TestCase
from django.contrib.auth.models import User
from .models import Thread, Message

# Create your tests here.
class ThreadTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('user1', None, 'test1234')
        self.user2 = User.objects.create_user('user2', None, 'test1234')
        self.user3 = User.objects.create_user('user3', None, 'test1234')

        self.thread = Thread.objects.create()

    def test_add_user_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        self.assertEqual(len(self.thread.users.all()), 2)
    
    def test_filter_threads_by_users(self):
        self.thread.users.add(self.user1, self.user2)
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(self.thread, threads[0])

    def test_filter_non_existing_thread(self):
        threads = Thread.objects.filter(users=self.user1).filter(users=self.user2)
        self.assertEqual(len(threads), 0)

    def test_add_message_to_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content='Hola Como estas?')
        message2 = Message.objects.create(user=self.user2, content='Buen dia, bien y tu?')
        self.thread.messages.add(message1, message2)
        self.assertEqual(len(self.thread.messages.all()), 2)
        
        for message in self.thread.messages.all():
            print (f"({message.user}) : {message.content}")
    
    def test_add_message_from_user_not_in_thread(self):
        self.thread.users.add(self.user1, self.user2)
        message1 = Message.objects.create(user=self.user1, content='Hola Como estas?')
        message2 = Message.objects.create(user=self.user2, content='Buen dia, bien y tu?')
        message3 = Message.objects.create(user=self.user3, content='A mi nadie me llamo pero aqui estoy')
        self.thread.messages.add(message1, message2, message3)
        self.assertEqual(len(self.thread.messages.all()), 2)
    

    def test_find_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find(self.user1, self.user2)
        self.assertEqual(self.thread, thread)

    def test_find_or_created_thread_with_custom_manager(self):
        self.thread.users.add(self.user1, self.user2)
        thread = Thread.objects.find_or_created(self.user1, self.user2)
        self.assertEqual(self.thread, thread)
        thread = Thread.objects.find_or_created(self.user1, self.user3)
        self.assertIsNotNone(thread)
