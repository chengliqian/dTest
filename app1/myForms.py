# Authour :chenglq
from django import forms
from django.forms import fields,ModelChoiceField
import re
from django.core.exceptions import ValidationError
from app1 import models
import json
#校验电话号码
def phone_validate(value):
    phone_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not phone_re.match(value):
        raise ValidationError('手机号不正确')

#校验qq号
def qqNo_validate(value):
    qq_re = re.compile(r'^[1-9][0-9]{4,}')
    if not qq_re.match(value):
        raise ValidationError('QQ号码不正确')

#校验输入是否为数字
def digit_validate(value):
    str_value = str(value)
    digit = re.compile(r'^[0-9]+(\.[0-9]){0,2}$')
    if not digit.match(str_value):
        raise  ValidationError("请输入数字")

#新增学员页，初始化课程下拉列表
cs = models.Courses.objects.all().order_by('-id')
COURSES_LIST = []
for c in cs:
    COURSES_LIST.append([c.id,c.couName],)
#登录form
class login_form(forms.Form):
    user = fields.CharField(max_length=32,
                            min_length=5,
                            required=True,
                            error_messages={
                                'required':"请输入登录名",
                                'min_length':"请至少输入5位",
                                })
    pwd = fields.CharField(max_length=32,
                           min_length=6,
                           required=True,
                           error_messages={
                                'required':"请输入密码",
                                'min_length': "请至少输入6位",
                                },
                           widget=forms.widgets.PasswordInput())
    def clean(self):
        clean_data = self.cleaned_data
        #print("**********", clean_data)
        u = clean_data.get('user')
        p = clean_data.get('pwd')
        #print("======>>> ",u," ",p)
        #ulist = []
        if u and p:
            usr = models.Login.objects.filter(uname=u).filter(passwd=p).first()
            #print("uuuuuu",usr,type(usr))
            if not usr :
                raise ValidationError("用户名或密码错误！")
            else:
                return self.cleaned_data



#课程form
class course_form(forms.Form):
    coursname = fields.CharField(max_length=64,
                                 required=True,
                                 error_messages={
                                     'required': '请填写科目名称',
                                     'max_length': '科目名称不可超过32个字'
                                 })
#班级form
class clas_form(forms.Form):
    clsId = fields.IntegerField(widget=forms.HiddenInput(),initial=0)
    clsname = fields.CharField(max_length=64,
                               required=True,
                               error_messages={
                                   'required':'请填写班级名称',
                                   'max_length':'班级名称不可超过32个字'

                               },)
    coursId = ModelChoiceField(
        required=True,
        queryset=models.Courses.objects.all().order_by('-id'),#新增班级页面，初始化科目下拉列表
        empty_label="-------",#ModelChoiceField 具有empty_label属性
        error_messages={
            'required': '请选择科目!',
        },)
    starttime = fields.DateTimeField(required=True,
                                    error_messages={
                                   'required':'请填写开课日期',
                                    'invalid':'输入格式不正确，例：2017-01-01',

                               },)
    endtime = fields.DateTimeField(required=True,
                                    error_messages={
                                   'required':'请填写结课日期',
                                    'invalid': '输入格式不正确，例：2017-01-01',

                               },)
    #op = fields.CharField(widget=forms.HiddenInput(),initial='add')
    # class Meta:
    #     model = models.Clas
    #     fields = '__all__'

    def clean_clsname(self):
        clsname = self.cleaned_data['clsname']
        clsId = self.data['clsId']
        #print("123:",clsname)
        #op = self.cleaned_data['op']
        if clsId==0:#clsId 为0，代表新增班级
            if clsname:
                c = models.Clas.objects.filter(clsName=clsname)
                if c:
                    raise ValueError('班级名称已存在，请重新输入！')
                else:
                    return clsname
        else:#clsId 不为0，代表编辑班级
            if clsname:
                c = models.Clas.objects.filter(clsName=clsname).exclude(id=clsId) #查询数据库中是否存在相同名称时，排除当前班级
                if c:
                    raise ValueError('班级名称已存在，请重新输入！')
                else:
                    return clsname

        #clsId = self.cleaned_data['clsId']
        #print("++++++++",clsId)
    def clean(self):
        clean_data = self.cleaned_data
        start = clean_data.get('starttime')
        end = clean_data.get('endtime')
        if start and end:
            if end <= start:
                raise  ValidationError('结课日期必须大于开课日期')
            else:
                return self.cleaned_data

#学生form
class stu_form(forms.Form):
    # stuno = fields.IntegerField(required=True,
    #                             error_messages={
    #                                'required':'请填写学号',
    #
    #                            },)

    stuname = fields.CharField(max_length=64,
                               required=True,
                               error_messages={
                                   'required':'请填写学员姓名',
                                   'max_length':'学员姓名不可超过32个字'

                               },)

    phone = fields.CharField(max_length=20,
                             min_length=11,
                             required=True,
                             validators=[phone_validate,],
                             error_messages={
                                 'required': '请填写手机号码',
                                 'max_length': '手机号最长不可超过20位',
                                 'min_length':'手机号至少11位'},)

    qq = fields.CharField(max_length=15,
                          validators=[qqNo_validate,],
                          error_messages={
                              'required':'请填写QQ号',
                          },)


    """coursId = ModelChoiceField(
        required=True,
        queryset=models.Courses.objects.all(),
        empty_label="-------",
        error_messages={
            'required': '请选择科目!',
        },
    )"""
    coursId = fields.IntegerField(
        widget=forms.Select(attrs={'class':'select','id':'coursID','onChange':'getClasOption(this.value)'},choices=COURSES_LIST,),
    )
    clsId = fields.IntegerField(required=False,
                                widget=forms.Select(choices = (('','-----'),),), )

    # clsId = ModelChoiceField(
    #     required=True,
    #     #queryset=models.Clas.objects.all(),
    #     queryset=models.Clas.objects.filter(couId=coursId),
    #     empty_label="-------",
    #     error_messages={
    #         'required': '请选择班级!',
    #     },
    # )


    clstype = fields.IntegerField(widget=forms.Select(choices=(
        (1, "现场"),
        (2, "网络"),), ))

    tu_total = fields.FloatField(min_value=0.0,
                                 required=True,
                                 validators=[digit_validate,],
                                 error_messages={
                                     'min_value':'请输入正数',
                                     'required':'请填写学费总额'
                                 })
    tu_paid = fields.FloatField( min_value=0.0,
                                 required=True,
                                 validators=[digit_validate,],
                                 error_messages={
                                     'min_value': '请输入正数',
                                     'required': '请填写已交学费'
                                 })

    is_recom = fields.IntegerField(widget=forms.Select(choices=(
        (1, "是"),
        (2, "否"),), ))

    #recom = fields.IntegerField(widget=forms.Select())
    '''recom = ModelChoiceField(
        queryset=models.Stu.objects.all(),
        empty_label="-------"
    )'''
    recom = fields.CharField(required=False,
        max_length=64)


    def __init__(self,*args,**kwargs):
        super(stu_form,self).__init__(*args,**kwargs)
        #self.fields['clsId'].widget.choices = models.Clas.objects.all().values_list('id',"clsName")

        #self.fields['recom'].widget.choices = models.Stu.objects.all().values_list('id',"name")

    # def clean_stuno(self):
    #     sno = self.cleaned_data['stuno']
    #     if sno:
    #         st = models.Stu.objects.filter(Sno=sno)
    #         if st:
    #             raise ValidationError('输入学号已存在，请重新输入！')
    #         else:
    #             return sno

    def clean_coursId(self):
        coursId = self.cleaned_data['coursId']
        print("coursID> ", coursId)
        c = models.Courses.objects.get(id=coursId)
        if not c:
            raise ValidationError('请选择所学科目!!!！')
        else:
            print("form course: ",c)
            return c

    def clean_clsId(self):
        clsId = self.cleaned_data['clsId']
        cls = models.Clas.objects.filter(id=clsId).first()
        if not cls:
            raise ValidationError('请选择班级!!!！')
        else:
            print("form cls: ",type(cls))
            return cls


    def clean_recom(self):
        is_recom = self.cleaned_data['is_recom']
        rec = self.cleaned_data['recom']
        s = models.Stu.objects.filter(name=rec).first()
        if is_recom==1:
            if not rec:
                #print("未输入推荐人")
                raise ValidationError('请选择推荐人！')
            else:
                if not s:
                    #print("-----打印错误-----")
                    raise ValidationError('该学员不存在')
                else:
                    print("form rec:",rec,type(rec))
                    print("from s:",s,type(s))
                    return s
        else:
            if rec:
                raise ValidationError('不需要填写推荐人')
            else:
                return s







