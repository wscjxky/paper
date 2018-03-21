from django.db import models
class Author(models.Model):
    name = models.CharField('作者名',unique=True, max_length=244, blank=False, null=True)
    description = models.TextField('作者简述', null=True)
    created = models.DateTimeField('创建时间', auto_now=True)
    url = models.TextField('链接a', null=True)

class Paper(models.Model):
    title = models.CharField('论文标题', unique=True, max_length=244, blank=False, null=True)
    cit_num = models.IntegerField('引用数量', default=0)
    description = models.TextField('标签简述', null=True)
    creator = models.TextField('作者', null=True)
    authors = models.ManyToManyField(Author, verbose_name='作者')
    created = models.DateTimeField('创建时间', auto_now=True)
    url = models.CharField('链接de',unique=True,max_length=244, null=True)
    cit_paper = models.ManyToManyField('self',  symmetrical=False,verbose_name='引用')


