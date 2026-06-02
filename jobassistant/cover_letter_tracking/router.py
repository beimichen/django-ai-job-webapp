# class DatabaseAppsRouter(object):
#     """
#     A router to control all database operations on models in the
#     user application.
#     """
#     def db_for_read(self, model, **hints):
#         """
#         Attempts to read user models go to chat_data.
#         """
#         if model._meta.app_label == 'cover_letter_tracking':
#             return 'chatdb'
#         return None
#
#     def db_for_write(self, model, **hints):
#         """
#         Attempts to write user models go to chat_data.
#         """
#         if model._meta.app_label == 'cover_letter_tracking':
#             return 'chatdb'
#         return None
#
#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Allow relations if a model in the chat app is involved.
#         """
#         if obj1._meta.app_label == 'cover_letter_tracking' or \
#            obj2._meta.app_label == 'cover_letter_tracking':
#             return True
#         return None
#
#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """
#         Make sure the chat app only appears in the 'chatdb'
#         database.
#         """
#         if app_label == 'cover_letter_tracking':
#             return db == 'chatdb'
#         return None
#
#     #grant all privileges on database jobbdb to admin;
