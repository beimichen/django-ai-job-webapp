# # Model related imports
# import uuid
# from django.db import models
# from django.contrib.postgres.fields import JSONField
#
#
# class RawJobTitle(models.Model):
#     raw_job_title = models.CharField(max_length=100, null=True)
#     reconciled_position = models.CharField(max_length=100, null=True)
#
#     class Meta:
#         managed = True
#         app_label = 'cover_letter_tracking'
#         verbose_name_plural = "raw job titles"
#
#
#     def __str__(self):
#         position = str(self.raw_job_title)
#         return position
#
#
# class JobTitle(models.Model):
#     job_title = models.CharField(max_length=100, null=True)
#     reconciled_position = models.CharField(max_length=100, null=True)
#
#     class Meta:
#         managed = True
#         app_label = 'cover_letter_tracking'
#         verbose_name_plural = "job titles"
#
#     def __str__(self):
#         return str(self.job_title)
#
#
# class RawCompany(models.Model):
#     raw_company = models.CharField(max_length=100, null=True)
#
#     class Meta:
#         managed = True
#         app_label = 'cover_letter_tracking'
#         verbose_name_plural = "raw companies"
#
#     def __str__(self):
#         company = str(self.raw_company)
#         return company
#
#
# class Company(models.Model):
#     company = models.CharField(max_length=100, null=True)
#
#     class Meta:
#         managed = True
#         app_label = 'cover_letter_tracking'
#         verbose_name_plural = "companies"
#
#     def __str__(self):
#         company = str(self.company)
#         return company
#
#
# class PersonName(models.Model):
#     name = models.CharField(max_length=100, null=True)
#
#     class Meta:
#         managed = True
#         app_label = 'cover_letter_tracking'
#         verbose_name_plural = "names"
#
#     def __str__(self):
#         return str(self.name)
#
#
# class RawPersonName(models.Model):
#     name = models.CharField(max_length=100, null=True)
#
#     class Meta:
#         managed = True
#         app_label = 'cover_letter_tracking'
#         verbose_name_plural = "raw names"
#
#     def __str__(self):
#         return str(self.name)
#
#
# class BasicCoverLetterManager(models.Manager):
#
#     def create_basic_cover_letter(self, data, sender):
#         basic_cover_letter = self.create(data=data, sender=sender)
#         return basic_cover_letter
#
#     class Meta:
#         managed = True
#         app_label = 'cover_letter_tracking'
#
#
# class BasicCoverLetter(models.Model):
#     sender = models.CharField(max_length=120, null=True)
#     data = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     objects = BasicCoverLetterManager()
#
#     def __str__(self):
#         return str(self.sender)
#
#     class Meta:
#         managed = True
#         app_label = 'cover_letter_tracking'
#
#
# class FullCoverLetterManager(models.Manager):
#
#     def create_full_cover_letter(self, data, sender):
#         full_cover_letter = self.create(data=data, sender=sender)
#         return full_cover_letter
#
#     def get_full_cover_letter(self, form_id):
#         return self.filter(form_id=form_id)
#
#     class Meta:
#         managed = True
#         app_label = 'cover_letter_tracking'
#
#
# class FullCoverLetter(models.Model):
#     sender = models.CharField(max_length=120, null=True)
#     data = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     objects = FullCoverLetterManager()
#
#     def __str__(self):
#         return str(self.sender)
#
#     class Meta:
#         managed = True
#         app_label = 'cover_letter_tracking'
#
#
# class UpdatedFullCoverLetterManager(models.Manager):
#
#     def create_updated_full_cover_letter(self, data, sender):
#         updated_full_cover_letter = self.create(data=data, sender=sender)
#         return updated_full_cover_letter
#
#     class Meta:
#         managed = True
#         app_label = 'cover_letter_tracking'
#
#
# class UpdatedFullCoverLetter(models.Model):
#     sender = models.CharField(max_length=120, null=True)
#     data = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#     objects = FullCoverLetterManager()
#
#     def __str__(self):
#         return str(self.sender)
#
#     class Meta:
#         managed = True
#         app_label = 'cover_letter_tracking'
#
#
# class OriginalFullCoverLetterManager(models.Manager):
#
#     def create_original_full_cover_letter(self, data, sender):
#         original_full_cover_letter = self.create(data=data, sender=sender)
#         return original_full_cover_letter
#
#     class Meta:
#         managed = True
#         app_label = 'cover_letter_tracking'
#
#
# class OriginalFullCoverLetter(models.Model):
#     sender = models.CharField(max_length=120, null=True)
#     data = JSONField()
#     created_at = models.DateTimeField(auto_now_add=True, null=True)
#
#     def __str__(self):
#         return str(self.sender)
#
#     class Meta:
#         managed = True
#         app_label = 'cover_letter_tracking'
#         verbose_name_plural = "original cover letters"
#
#
#
#
