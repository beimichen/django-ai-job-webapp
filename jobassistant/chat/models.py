# from django.contrib.postgres.fields import JSONField
# from django.db import models
# import uuid
#
#
# class SenderUUIDManager(models.Manager):
#
#     def create_sender_id(self, sender_id):
#         id = self.create(sender_id=sender_id)
#         return id
#
#     class Meta:
#         managed = True
#         app_label = 'chat'
#
#
# class SenderUUID(models.Model):
#     # sender_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # TODO: change this to charfield with 120 max length
#     sender_id = models.CharField(max_length=100, null=True)
#     objects = SenderUUIDManager()
#
#     def __str__(self):
#         return str(self.sender_id)
#
#     class Meta:
#         managed = True
#         app_label = 'chat'
#
#
# class ChatPartOneManager(models.Manager):
#
#     def create_chat_data(self, data, sender):
#         chat = self.create(data=data, sender=sender)
#         return chat
#
#     class Meta:
#         managed = True
#         app_label = 'chat'
#
#
# class ChatPartOne(models.Model):
#     sender = models.ForeignKey(
#         SenderUUID,
#         on_delete=models.CASCADE,
#     )
#     data = JSONField(blank=True, null=True)
#     objects = ChatPartOneManager()
#
#     def __str__(self):
#         return str(self.sender)
#
#     class Meta:
#         managed = True
#         app_label = 'chat'
#
#
# class ChatPartOneTrackerManager(models.Manager):
#
#     def create_chat_tracker_data(self, data, sender):
#         chat = self.create(data=data, sender=sender)
#         return chat
#
#     class Meta:
#         managed = True
#         app_label = 'chat'
#
#
# class ChatPartOneTracker(models.Model):
#     sender = models.ForeignKey(
#         SenderUUID,
#         on_delete=models.CASCADE,
#     )
#     data = JSONField(blank=True, null=True)
#     objects = ChatPartOneTrackerManager()
#
#     def __str__(self):
#         return str(self.sender)
#
#     class Meta:
#         managed = True
#         app_label = 'chat'
#
#
# class ChatFullTrackerManager(models.Manager):
#
#     def create_chat_tracker_data(self, data, sender):
#         chat = self.create(data=data, sender=sender)
#         return chat
#
#     def get_chat_data(self, sender):
#         return self.filter(sender=sender)
#
#     class Meta:
#         managed = True
#         app_label = 'chat'
#
#
# class ChatFullTracker(models.Model):
#     sender = models.CharField(max_length=120, null=True)
#     data = JSONField(blank=True, null=True)
#     objects = ChatFullTrackerManager()
#
#     def __str__(self):
#         return str(self.sender)
#
#     class Meta:
#         managed = True
#         app_label = 'chat'
#
#
# class ChatPartTwoManager(models.Manager):
#
#     def create_chat_data(self, data, sender):
#         message = self.create(data=data, sender=sender)
#         return message
#
#     class Meta:
#         managed = True
#         app_label = 'chat'
#
#
# class ChatPartTwo(models.Model):
#     sender = models.ForeignKey(
#         SenderUUID,
#         on_delete=models.CASCADE,
#     )
#     data = JSONField(blank=True, null=True)
#     objects = ChatPartTwoManager()
#
#     def __str__(self):
#         return str(self.sender)
#
#     class Meta:
#         managed = True
#         app_label = 'chat'
