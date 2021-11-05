from django.db import models
from product.models import Product
# Create your models here.


class Apitest(models.Model):
    id = models.BigAutoField(primary_key=True)
    Product = models.ForeignKey('product.Product', on_delete=models.CASCADE, null=True)
    apitestfeature = models.CharField('模块名称', max_length=64)
    apiteststory = models.CharField('用例名称', max_length=64)
    apitester = models.CharField('测试负责人', max_length=16)
    apitestresult = models.BooleanField('测试结果')
    create_time = models.DateTimeField('创建时间', auto_now=True)

    class Meta:
        verbose_name = '流程场景接口'
        verbose_name_plural = '流程场景接口'

    def __str__(self):
        return self.apitestname


class Apistep(models.Model):
    Apitest = models.ForeignKey(Apitest, on_delete=models.CASCADE)
    #关联接口ID
    id = models.BigAutoField(primary_key=True)
    waittime = models.CharField('前置等待时间', max_length=100)
    #前置等待时间
    title = models.CharField('用例标题', max_length=200)
    #用例标题
    url = models.CharField('路径', max_length=100, null=False)
    #用例路径
    REQUEST_METHOD = (('get', 'get'), ('post', 'post'), ('put', 'put'), ('delete', 'delete'), ('patch', 'patch'))
    apimethod = models.CharField(verbose_name='请求方法', choices=REQUEST_METHOD, default='get', max_length=200, null=True)
    # 请求方法
    apiparamvalue = models.CharField('请求参数和值', max_length=5000)
    #参数和值
    exceptresponse = models.CharField('期望响应', max_length=200, null=False)
    actualresponse = models.CharField('实际响应', max_length=5000, default='null', null=False)
    result = models.CharField('测试结果', max_length=20, null=False)
    apistatus = models.BooleanField('是否通过')
    create_time = models.DateTimeField('创建时间', auto_now=True)
    #创建时间，自动获取当前时间

    def __str__(self):
        return self.apiname


class Apis(models.Model):

    id = models.BigAutoField(primary_key=True)
    Product = models.ForeignKey('product.Product', on_delete=models.CASCADE, null=True)
    feature = models.CharField('模块名称', max_length=50, null=False)
    story = models.CharField('用例名称', max_length=50, null=False)
    title = models.CharField('用例标题', max_length=50, null=False)
    link = models.CharField('用例链接', max_length=200, null=False)
    issue = models.CharField('缺陷链接', max_length=200, null=False)
    url = models.CharField('url地址', max_length=200, null=False)
    REQUEST_METHOD = (('0', 'get'), ('1', 'post'), ('2', 'put'), ('3', 'delete'), ('4', 'patch'))
    method = models.CharField(verbose_name='请求方法', choices=REQUEST_METHOD, default='0', max_length=200)
    headers = models.CharField('请求头', max_length=200, null=False)
    apiparamvalue = models.CharField('请求参数和值', max_length=5000, null=False)
    enable = models.BooleanField('是否启用', default='1')
    exceptresponse = models.CharField('期望响应', max_length=200, null=False)
    actualresponse = models.CharField('实际响应', max_length=5000, default='null', null=False)
    result = models.CharField('测试结果', max_length=20, null=False)
    tester = models.CharField('测试人', max_length=20, null=False)
    create_time = models.DateTimeField('创建时间', auto_now=True)
    class Meta:
        verbose_name = '单一场景接口'
        verbose_name_plural = '单一场景接口'

    def __str__(self):
        return self.story


class Users(models.Model):

    id = models.BigAutoField(primary_key=True)
    Product = models.ForeignKey('product.Product', on_delete=models.CASCADE, null=True)
    environment = models.CharField('环境', max_length=50, null=False)
    name = models.CharField('别名', max_length=50, null=False)
    merchantcode = models.CharField('商户code', max_length=50, null=False)
    username = models.CharField('账号', max_length=20, default='null', null=False)
    password = models.CharField('密码', max_length=20, default='null', null=False)
    token = models.CharField('token', max_length=500, default='null', null=False)
    creator = models.CharField('创建人', max_length=20)
    create_time = models.DateTimeField('创建时间', auto_now=True)
    class Meta:
        verbose_name = '用例用户'
        verbose_name_plural = '用例用户'

    def __str__(self):
        return self.name
