from django.db import models

# Create your models here.

CLAS_TYPE = [(1,"现场"),(2,"网络"),]
IS_RECOM = [(1, "是"),(2, "否"),]

class Login(models.Model):
    uname = models.CharField(verbose_name="用户名",max_length=32,unique=True)
    passwd = models.CharField(verbose_name="密码",max_length=32)

#课程类型
class Courses(models.Model):
    couName = models.CharField(verbose_name="班级名称",max_length=64,unique=True)

    def __str__(self):
        return self.couName

#学生表
class Stu(models.Model):
    #nid = models.BigAutoField(primary_key=True)
    #Sno = models.IntegerField(verbose_name='学号',unique=True)
    name = models.CharField(verbose_name='姓名', max_length=64)
    phoneNo = models.CharField(verbose_name='手机号',max_length=20,null=False)
    qqNo = models.CharField(verbose_name='qq号',max_length=15,null=False)
    couId = models.ForeignKey(Courses,default=1,db_constraint=False)
    clsId = models.ForeignKey("Clas",db_constraint=False)
    tuition_total = models.FloatField(verbose_name="应交学费")
    tuition_paid = models.FloatField(verbose_name="已交学费")
    isRecommended = models.IntegerField(verbose_name='是否内部推荐',choices=IS_RECOM,)
    recommender = models.ForeignKey('self',blank=True,null=True,db_constraint=False)
    clsType = models.IntegerField(choices=CLAS_TYPE,default=1,verbose_name="班级类型，1现场，2网络")

    def __str__(self):
        return self.name



#班级表
class Clas(models.Model):
    clsName = models.CharField(verbose_name="班级名称",max_length=128,unique=True)
    startTime = models.DateField(verbose_name="开课时间")
    endTime = models.DateField(verbose_name="结束时间")
    course = models.ForeignKey("Courses",default=1,db_constraint=False)

    def __str__(self):
        return self.clsName



