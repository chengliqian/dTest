import  xlwt,io,time
from django.shortcuts import render,redirect,HttpResponse
from app1 import models
from app1 import myForms
import  json,random
from django.core.exceptions import ValidationError
from app1.Pager import Pager
#from django.views.decorators.csrf import csrf_protect

# Create your views here.
class JsonCustomEncoder(json.JSONEncoder):
    def default(self, field):
        if isinstance(field, ValidationError):
            return {'code': field.code, 'messages': field.messages}
        else:
            return json.JSONEncoder.default(self, field)

#登录
def login(request):
    #UserList = {'admin':'123456'}
    if request.method == 'POST':
        lg = myForms.login_form(request.POST)
        sta = lg.is_valid()
        datas = lg.cleaned_data
        result = {'status': True, "error": None, "data": None}
        if sta:
            u = datas['user']
            p = datas['pwd']
        # u = request.POST.get('user')
        # p = request.POST.get('pwd')
        # if u in UserList and p==UserList[u]:
            request.session['user']=u
            request.session['pwd']=p
            request.session['is_login']=True
            #return redirect('/index')
        else:
            result["status"] = False
            result["error"] = lg.errors.as_data()
            print(result["error"])
        res = json.dumps(result, cls=JsonCustomEncoder)
        return HttpResponse(res)
    elif request.method =='GET':
        lg = myForms.login_form()
        #print("+++++++ ",lg)
        return render(request,'login.html',{'ulogin':lg})

#登录装饰器
def check_login(func):
    def inner(request,*args,**kwargs):
        user = request.session.get('user')
        passwd = request.session.get('pwd')
        stas = request.session.get('is_login')
        if stas != True:
            #return render(request,'login.html')
            return redirect('/')
        return func(request,*args,**kwargs)
    return inner

# 退出
@check_login
def logout(request):
    # del request.session['user']
    # del request.session['pwd']
    # del request.session['sta']
    request.session.clear()
    return redirect('/')#返回到登录页

@check_login
def index(request):
    user = request.session.get('user')
    return render(request,'index.html',{'user':user})

# 学生列表
@check_login
def search_stu(request):
    cos = models.Courses.objects.all().order_by('-id') #课程下拉列表
    cls = models.Clas.objects.all().order_by('-id') #班级下拉列表
    '''current_page = request.GET.get('page',1)
    current_page = int(current_page)
    page_obj = Pager(current_page)'''
    if request.method == "POST":
        # 除了课程和班级，其余条件均是模糊搜索
        sname = request.POST.get('sname')#学生姓名
        sqq = request.POST.get('sqq')#qq号
        sphone = request.POST.get('sphone')#电话号码
        cours = request.POST.get('coursId')#课程
        #print("#########",cours,type(cours))
        cls = request.POST.get('clsId')#班级
        #print(">>>>>>>>>>>", cls)
        if int(cours) == 0: #cours=0 代表未选择任何课程
            if sname or sqq or sphone :
                param = {'name__icontains':sname,'qqNo__icontains':sqq,'phoneNo__icontains':sphone}
                stu = models.Stu.objects.filter(**param).order_by('-clsId__id','-id')
            else:# 未输入任何搜索条件 显示全部数据
                stu = models.Stu.objects.all().order_by('-clsId__id','-id')
        elif int(cls) == 0: #cls=0 代表未选择任何班级
            param = {'name__icontains': sname, 'qqNo__icontains': sqq, 'phoneNo__icontains': sphone,'couId__id':cours}
            stu = models.Stu.objects.filter(**param).order_by('-clsId__id','-id')
        else:
            param = {'name__icontains': sname, 'qqNo__icontains': sqq, 'phoneNo__icontains': sphone,
                         'couId__id': cours,'clsId__id':cls}
            stu = models.Stu.objects.filter(**param).order_by('-clsId__id','-id')

        #print(stu)
        # all_item = stu.count()
        # pager_str = page_obj.page_str(all_item,'/search_stu')
        # cls= models.Clas.objects.filter(clsName="cls3")

        #return render(request, 'stu_list.html', {'stu_list': stu})
    elif request.method == "GET":
        stu = models.Stu.objects.all().order_by('-clsId__id','-id')
        #print(stu)
    #print(stu)
    '''stu1 = stu[page_obj.start:page_obj.end]
    all_item = stu.count()
    print("总数：",all_item)
    pager_str = page_obj.page_str(all_item, '/search_stu')'''

    return render(request, 'stu_list.html', {'stu_list':stu,'cos_list':cos,'cls_list':cls,})

# 新增学员
@check_login
def add_stu(request):
    result = {'status': True, "error": None, "data": None}
    if request.method == "POST":
        stu = myForms.stu_form(request.POST)
        sta = stu.is_valid()
        stu_data = stu.cleaned_data
        if sta:
            #print(stu_data)
            #sno = stu_data['stuno']
            name = stu_data['stuname']
            mobile = stu_data['phone']
            qq = stu_data['qq']
            coursId = stu_data['coursId']
            clsId = stu_data['clsId']
            clstype = stu_data['clstype']
            tu_total = stu_data['tu_total']
            tu_paid = stu_data['tu_paid']
            is_recom = stu_data['is_recom']
            #print("is_recom:",is_recom)
            recom = stu_data['recom']
            #print('recom>>>>',recom)

            stunew = models.Stu.objects.create(
                    name=name,
                    phoneNo=mobile,
                    qqNo=qq,
                    couId=coursId,
                    clsId=clsId,
                    clsType=clstype,
                    tuition_total=tu_total,
                    tuition_paid=tu_paid,
                    isRecommended=is_recom,
                    recommender=recom)
             #s_rec = models.Stu.objects.filter(name=recom).first()
            # s_rec = models.Stu.objects.filter(name=recom)
            #print("推荐人：",s_rec)

            #print("stunew: ",stunew)
            stunew.save()

        else:
            result["status"] = False
            result["error"] = stu.errors.as_data()
            print(result["error"])
        res = json.dumps(result, cls=JsonCustomEncoder)
        print(res)
        return HttpResponse(res)

    else:
        stu = myForms.stu_form()
    return render(request, "add_stu.html", {'stu': stu})

#编辑学员
@check_login
def edit_stu(request,sid):# 根据学员id，搜索要编辑的学员
    cos = models.Courses.objects.all().order_by('-id')#课程下拉列表
    cls = models.Clas.objects.all().order_by('-id') #班级下拉列表
    isre_list = []#是否推荐下拉列表
    # is_re = {}
    for i in range(len(models.IS_RECOM)):
        # is_re["id"]=models.IS_RECOM[i][0]
        # is_re["txt"]=models.IS_RECOM[i][1]
        isre_list.append({"id":models.IS_RECOM[i][0],
                          "txt":models.IS_RECOM[i][1]}
                         )
        #print("is_re:",isre_list)
    ctype_list = [] # 班级类型下拉列表
    # clstype = {}
    for j in range(len(models.CLAS_TYPE)):
        # clstype["id"] = models.IS_RECOM[j][0]
        # clstype["txt"] = models.IS_RECOM[j][1]
        ctype_list.append({"id":models.CLAS_TYPE[j][0],
                           "txt":models.CLAS_TYPE[j][1]}
                          )
        #print(ctype_list)

    if request.method=="GET":
        stu_select = models.Stu.objects.filter(id=sid).first() # 被选中要编辑的学员，按照学员id查询
        #print("GET: ",stu_select.isRecommended," ",stu_select.clsType)

    elif request.method=="POST":
        stu_select = myForms.stu_form(request.POST)
        sta = stu_select.is_valid()
        datas = stu_select.cleaned_data
        result = {'status': True, "error": None, "data": None}
        if sta:
            print("clean datas: ",datas)
            name = datas['stuname']
            mobile = datas['phone']
            qq = datas['qq']
            coursId = datas['coursId']
            clsId = datas['clsId']
            clstype = datas['clstype']
            tu_total = datas['tu_total']
            tu_paid = datas['tu_paid']
            is_recom = datas['is_recom']
            print("is_recom:", is_recom)
            recom = datas['recom']

            #更新为最新输入的信息
            stu = models.Stu.objects.filter(id=sid).first()
            stu.name = name
            stu.phoneNo = mobile
            stu.qqNo = qq
            stu.couId = coursId
            stu.clsId = clsId
            stu.clsType = clstype
            stu.tuition_total = tu_total
            stu.tuition_paid = tu_paid
            stu.isRecommended = is_recom
            stu.recommender = recom
            stu.save()
        else:
            result['status']=False
            result['error'] = stu_select.errors.as_data()
        result = json.dumps(result, cls=JsonCustomEncoder)
        return HttpResponse(result)
    return render(request,"stu_detail.html",{'stu_select':stu_select,'cos_list':cos,'cls_list':cls,'is_re':isre_list,'cls_type':ctype_list})

#删除学员
@check_login
def delete_stu(request):
    sid = request.POST.get("stuid")
    stu_delete = models.Stu.objects.filter(id=sid)
    res = {'status': True, "error": None, "data": None}
    if stu_delete:
        stu_delete.delete()
        return HttpResponse("OK")
    else:
        return HttpResponse("False")

#根据课程，联动显示该课程所有的班级
@check_login
def clas_select(request,cousid):
    cls_list = []
    #cours = request.GET['coursId']
    #print("-->",cours)
    cls = models.Clas.objects.filter(course_id = cousid).order_by('-id') #根据传入的课程id，搜索该课程关联的所有班级
    #print("--->>",cls)
    for cs in cls:
        c={}
        c['cid'] = cs.id #返回班级id
        c['cname'] = cs.clsName #返回班级名称
        cls_list.append(c)
        #print("list:",cls_list)
    return  HttpResponse(json.dumps(cls_list))

#数据库插数据
def add(request):
    # cls = models.Clas(clsName = "cls4",startTime="2017-11-1 14:43",endTime = "2018-3-1 14:43")
    # cls.save()
    # for i in range(8,30):
    #     dict = {'clsName':'cls%d'%i,'course_id':1,'startTime':'2015-1-1','endTime':'2015-5-1'}
    #     c = models.Clas.objects.create(**dict)
    #     c.save()

    for j in range(0,50):
        dic = {'name':'stu%d'%j,
               'phoneNo':'13910122469',
               'qqNo':'774686297',
               'clsId_id':random.randint(1,29),
               'couId_id':random.randint(1,4),
               'clsType':random.randint(1,2),
               'tuition_total':10000,
               'tuition_paid':10000,
               'isRecommended':False}
        s = models.Stu.objects.create(**dic)
        s.save()
    # cls = models.Clas.objects.get(clsName ="cls4" )
    # s1 = models.Stu.objects.get(Sno=1001)
    # stu = models.Stu()
    # stu.name = "lucy"
    # stu.Sno = 1003
    # stu.phoneNo = 13910122469
    # stu.qqNo = 774686297
    # stu.clsId = cls
    # stu.tuition_total = 10000
    # stu.tuition_paid = 6600
    # stu.isRecommended = True
    # stu.recommender =s1
    # stu.clsType = 1
    # stu.save()

    return HttpResponse('OK')

#班级列表
@check_login
def search_cls(request):
    # if 'q' in request.GET:
    #     q = request.GET['q']
    #     print(q)
    '''current_page = request.GET.get('page', 1)
    current_page = int(current_page)
    page_obj = Pager(current_page)'''
    cos = models.Courses.objects.all().order_by('-id') #课程下拉列表
    if request.method == "POST":
        cname = request.POST.get('cname')
        cous = request.POST.get('coursId')
        if int(cous)==0:# 课程id为0，代表未选择任何课程，搜索全部课程类型，只判断班级名称
            if cname:# 班级名称模糊查询
                para = {'clsName__icontains':cname}
                cls = models.Clas.objects.filter(**para).order_by('-id')#查询结果按照id倒序排列
            else: #未输入任何搜索条件，搜索全部数据
                cls = models.Clas.objects.all().order_by('-id')
        else:#根据课程类型、班级名称查询
            para = {'clsName__icontains':cname,'course__id':cous}
            cls = models.Clas.objects.filter(**para).order_by('-id')
            #print(cls)
        #cls= models.Clas.objects.filter(clsName="cls3")

        #return render(request, 'cls_list.html', {'cls_list':cls})
    elif request.method == "GET":
        cls = models.Clas.objects.all().order_by('-id')

    '''cls1 = cls[page_obj.start:page_obj.end]
    all_item = cls.count()
    print("总数：", all_item)
    pager_str = page_obj.page_str(all_item, '/search_cls')'''

    return render(request,'cls_list.html',{'cls_list':cls,'cos_list':cos})
    #return redirect('/search_cls')

#新增班级
@check_login
def add_cls(request):
    if request.method == "POST":
        cls_obj = myForms.clas_form(request.POST)
        sta = cls_obj.is_valid()
        datas = cls_obj.cleaned_data
        #print(datas)
        result = {'status':True,"error":None,"data":None}

        if sta:
            # print('cls_obj.clean(): ',cls_obj.clean())
            # print('cls_obj.cleaned_data: ',cls_obj.cleaned_data)
            clsname = datas['clsname']#班级名称
            cs = datas['coursId']#所属课程
            startT = datas['starttime']#开课时间
            endT = datas['endtime']#结课时间
            if clsname and cs and startT and endT:
                c = models.Clas.objects.create(clsName=clsname, course = cs,startTime=startT, endTime=endT)
                c.save()

            #return render(request, "add_cls.html")
            #return HttpResponse("OK")
        else:
            result["status"] = False
            result["error"] = cls_obj.errors.as_data()
            print(result["error"])
        res = json.dumps(result,cls=JsonCustomEncoder)
        return HttpResponse(res)
    elif request.method == "GET":
        cls_obj = myForms.clas_form()
    return render(request, "add_cls.html",{'cls_obj':cls_obj})


    #business_list = models.Business.objects.all()

#编辑班级
@check_login
def edit_cls(request,cid):#根据传入的班级id，搜索要编辑的班级
    cos = models.Courses.objects.all()#课程类型下拉列表
    if request.method == "GET":
        cls_select = models.Clas.objects.filter(id=cid).first()
    elif request.method == "POST":
        cls_select = myForms.clas_form(request.POST)
        sta = cls_select.is_valid()
        datas = cls_select.cleaned_data
        print("datas: ",datas)
        result = {'status': True, "error": None, "data": None}

        if sta:
            print('cls_select.clean(): ', cls_select.clean())
            print('cls_select.cleaned_data: ', cls_select.cleaned_data)
            clsname = datas['clsname']
            cs = datas['coursId']
            startT = datas['starttime']
            endT = datas['endtime']
            if clsname and cs and startT and endT:
                #更新为最新输入的信息
                c = models.Clas.objects.filter(id = cid).first()
                c.clsName = clsname
                c.course = cs
                c.startTime = startT
                c.endTime = endT
                c.save()
        else:
            result["status"] = False
            result["error"] = cls_select.errors.as_data()
            print(result["error"])
        res = json.dumps(result, cls=JsonCustomEncoder)
        return HttpResponse(res)
    return render(request, "cls_detail.html", {'cls_select': cls_select,'cos_list':cos})

#删除班级
@check_login
def delete_cls(request):#根据班级id 删除所选班级
    cid = request.POST.get("clsid")
    cls_delete = models.Clas.objects.filter(id = cid)
    #res= {'status': True, "error": None, "data": None}
    if cls_delete:
       cls_delete.delete()
       return HttpResponse("OK")
    else:
        return HttpResponse("False")
    #return render(request,"cls_list.html")

#查询课程
@check_login
def search_course(request):
    if request.method == "GET":
        cous = models.Courses.objects.all().order_by('-id')
    elif request.method == "POST":
        cname = request.POST.get('cname')
        if cname:#根据课程名称模糊搜索
            cous = models.Courses.objects.filter(couName__icontains=cname).order_by('-id')
        else:#未输入搜素条件，查询所有数据
            cous = models.Courses.objects.all().order_by('-id')
    print(cous)
    return render(request,'course_list.html',{'cou_list':cous})

#删除课程
@check_login
def del_course(request):
    cosid = request.POST.get("couid")
    course_del = models.Courses.objects.filter(id=cosid)
    if course_del:
        course_del.delete()
        return HttpResponse("OK")
    else:
        return HttpResponse("False")

#新增课程
@check_login
def add_course(request):
    if request.method == "POST":
        cours_obj = myForms.course_form(request.POST)
        sta = cours_obj.is_valid()
        datas = cours_obj.cleaned_data
        print(datas)
        result = {'status': True, "error": None, "data": None}
        if sta:
            cousName =  datas['coursname']
            if cousName:
                new_cours = models.Courses.objects.create(couName=cousName)
                new_cours.save()
            else:
                result["status"] = False
                result["error"] = {"course": [{"code": "", "messages": ["课程名称不允许空！"]}]}
        else:
            result["status"] = False
            result["error"] = cours_obj.errors.as_data()
            print(result["error"])
        res = json.dumps(result, cls=JsonCustomEncoder)
        return HttpResponse(res)



@check_login
def edit_course(request):
    coursid = request.POST.get("couid")
    # if request.method == "GET":
    #     cours_select = models.Courses.objects.filter(id=coursid).first()
    if request.method == "POST":
        cours_select = myForms.course_form(request.POST)
        sta = cours_select.is_valid()
        datas = cours_select.cleaned_data
        print("datas: ", datas)
        result = {'status': True, "error": None, "data": None}
        if sta:
            coursname = datas['coursname']
            if coursname:
                cos  = models.Courses.objects.filter(id=coursid).first()
                if cos:
                    cos.couName = coursname
                    cos.save()
                else:
                    result["status"] = False
                    result["error"]={"course":[{"code":"","messages":["课程不存在！"]}]}
        else:
            result["status"] = False
            result["error"] = cours_select.errors.as_data()
            print(result["error"])
        res = json.dumps(result, cls=JsonCustomEncoder)
        return HttpResponse(res)
    #return render(request, "course_list.html", {'cours_select': cours_select,})

#导出班级
@check_login
def download_clas(request):
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet("sheet1")
    row0 = [u'所属课程',u'班级名称',u'开课时间',u'结课时间']
    for i in range(0,len(row0)):
        sheet.write(0,i,row0[i])

    if request.method == "POST":
        cours = request.POST.get('coursId1')
        clsname = request.POST.get('cname1')
        if int(cours) == 0:  # 课程id为0，代表未选择任何课程，搜索全部课程类型，只判断班级名称
            if clsname:  # 班级名称模糊查询
                para = {'clsName__icontains': clsname}
                cls = models.Clas.objects.filter(**para).order_by('-id')  # 查询结果按照id倒序排列
            else:  # 未输入任何搜索条件，搜索全部数据
                cls = models.Clas.objects.all().order_by('-id')
        else:  # 根据课程类型、班级名称查询
            para = {'clsName__icontains': clsname, 'course__id': cours}
            cls = models.Clas.objects.filter(**para).order_by('-id')

        row=1
        for c in cls:
            print("--->>>",c)
            sheet.write(row,0,c.course.couName)
            sheet.write(row,1,c.clsName)
            sheet.write(row,2,c.startTime.strftime("%Y-%m-%d"))
            sheet.write(row,3,c.endTime.strftime("%Y-%m-%d"))
            #print(c.startTime,type(c.startTime),type(str(c.startTime)))
            # sheet.write(row,1,time.strptime((str(c.startTime)),"%Y-%m-%d"))
            # sheet.write(row,1,c.clsName)
            row+=1
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=classes' + time.strftime('%Y%m%d', time.localtime(
            time.time())) + '.xls'
        workbook.save(response)
        print(workbook)
        print(response)
        return response
