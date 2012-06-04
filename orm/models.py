# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from django.db import models

class MozAnnoAttributes(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    name = models.CharField(unique=True, max_length=32)
    class Meta:
        db_table = u'moz_anno_attributes'

class MozAnnos(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    place_id = models.IntegerField()
    anno_attribute_id = models.IntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=32, blank=True)
    content = models.TextField(blank=True) # This field type is a guess.
    flags = models.IntegerField(null=True, blank=True)
    expiration = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    dateadded = models.IntegerField(null=True, db_column=u'dateAdded', blank=True) # Field name made lowercase.
    lastmodified = models.IntegerField(null=True, db_column=u'lastModified', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'moz_annos'

class MozBookmarks(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    fk = models.IntegerField(null=True, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    title = models.TextField(blank=True) # This field type is a guess.
    keyword_id = models.IntegerField(null=True, blank=True)
    folder_type = models.TextField(blank=True)
    dateadded = models.IntegerField(null=True, db_column=u'dateAdded', blank=True) # Field name made lowercase.
    lastmodified = models.IntegerField(null=True, db_column=u'lastModified', blank=True) # Field name made lowercase.
    guid = models.TextField(unique=True, blank=True)
    class Meta:
        db_table = u'moz_bookmarks'

class MozBookmarksRoots(models.Model):
    root_name = models.CharField(unique=True, max_length=16, blank=True)
    folder_id = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'moz_bookmarks_roots'

class MozFavicons(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    url = models.TextField(unique=True, blank=True) # This field type is a guess.
    data = models.TextField(blank=True) # This field type is a guess.
    mime_type = models.CharField(max_length=32, blank=True)
    expiration = models.TextField(blank=True) # This field type is a guess.
    guid = models.TextField(unique=True, blank=True)
    class Meta:
        db_table = u'moz_favicons'

class MozHistoryvisits(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    from_visit = models.IntegerField(null=True, blank=True)
    place_id = models.IntegerField(null=True, blank=True)
    visit_date = models.IntegerField(null=True, blank=True)
    visit_type = models.IntegerField(null=True, blank=True)
    session = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'moz_historyvisits'

class MozInputhistory(models.Model):
    place_id = models.IntegerField(primary_key=True)
    input = models.TextField(primary_key=True) # This field type is a guess.
    use_count = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = u'moz_inputhistory'

class MozItemsAnnos(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    item_id = models.IntegerField()
    anno_attribute_id = models.IntegerField(null=True, blank=True)
    mime_type = models.CharField(max_length=32, blank=True)
    content = models.TextField(blank=True) # This field type is a guess.
    flags = models.IntegerField(null=True, blank=True)
    expiration = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    dateadded = models.IntegerField(null=True, db_column=u'dateAdded', blank=True) # Field name made lowercase.
    lastmodified = models.IntegerField(null=True, db_column=u'lastModified', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'moz_items_annos'

class MozKeywords(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    keyword = models.TextField(unique=True, blank=True)
    class Meta:
        db_table = u'moz_keywords'

class MozPlaces(models.Model):
    id = models.IntegerField(null=True, primary_key=True, blank=True)
    url = models.TextField(unique=True, blank=True) # This field type is a guess.
    title = models.TextField(blank=True) # This field type is a guess.
    rev_host = models.TextField(blank=True) # This field type is a guess.
    visit_count = models.IntegerField(null=True, blank=True)
    hidden = models.IntegerField()
    typed = models.IntegerField()
    favicon_id = models.IntegerField(null=True, blank=True)
    frecency = models.IntegerField()
    last_visit_date = models.IntegerField(null=True, blank=True)
    guid = models.TextField(unique=True, blank=True)
    class Meta:
        db_table = u'moz_places'

class SqliteStat1(models.Model):
    tbl = models.TextField(blank=True) # This field type is a guess.
    idx = models.TextField(blank=True) # This field type is a guess.
    stat = models.TextField(blank=True) # This field type is a guess.
    class Meta:
        db_table = u'sqlite_stat1'

