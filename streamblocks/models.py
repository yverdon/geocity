from django.db import models

class PrintBlockParagraph(models.Model):
    title = models.CharField(max_length=1000)
    content = models.TextField()

class PrintBlockMap(models.Model):
    url = models.CharField(max_length=1000)

class PrintBlockContacts(models.Model):
    content = models.TextField()

class PrintBlockValidation(models.Model):
    content = models.TextField()

# Register blocks for StreamField as list of models
STREAMBLOCKS_MODELS = [
    PrintBlockParagraph,
    PrintBlockMap,
    PrintBlockContacts,
    PrintBlockValidation,
]
