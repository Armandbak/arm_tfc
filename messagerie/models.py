
# models.py dans votre application de messagerie (par exemple, 'messaging')

from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    pass

class ConversationUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    read_at = models.DateTimeField(null=True, blank=True)

class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


''' from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    pass

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class ConversationUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    read_at = models.DateTimeField(null=True, blank=True)
'''