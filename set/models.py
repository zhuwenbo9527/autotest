from django.db import models

class Set(models.Model):
    setname = models.CharField('系统名称',max_length=64)
    setvalue = models.CharField('系统设置-值',max_length=200)
    class Meta:
        verbose_name = '系统名称'
        verbose_name_plural = '系统设置-值'

    def __str__(self):
        return self.setname
# Create your models here.
