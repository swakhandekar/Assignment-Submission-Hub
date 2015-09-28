from django.shortcuts import render,HttpResponse,Http404,HttpResponseRedirect
from models import *
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from forms import MyForm
from django.core.exceptions import ValidationError
from django.conf import settings
from os.path import join
from os import mkdir
from datetime import datetime

def is_teacher(request):
    if request.user.is_authenticated():
        if Teacher.objects.filter(user=request.user).exists():
            return True
    return False

def is_student(request):
    if request.user.is_authenticated():
        if Student.objects.filter(user=request.user).exists():
            return True
    return False

def home(request):
    if is_student(request):
        return student_home(request)
    elif is_teacher(request):
        return teacher_home(request)
    return render(request,"home.html")

def student_home(request):
    if is_student(request):
        try:
            mybatch = MyBatch.objects.get(user = request.user)
            batch = mybatch.batch
        except:
            batch = None
        if batch is not None:
            subs = Subject.objects.all()
            l = []
            for i in subs:
                x={}
                d = Assignment.objects.filter(sub = i,to_batch=batch)
                x[i.id] = d
                l.append(x)
            return render(request,"student_home.html",{"subs":subs,"list":l})
        return Http404("Something went wrong!!")
    return render(request,"home.html")

def teacher_home(request):
    if is_teacher(request):
        try:
            myBatches = MyBatch.objects.filter(user=request.user)
        except:
            myBatches = None
        teacher = Teacher.objects.get(user=request.user)
        if myBatches is not None:
            l = []
            for i in myBatches:
                x = {}
                d = Assignment.objects.filter(assigned_by=teacher,
                                              to_batch=i.batch
                                            )
                x[i] = d
                l.append(x)
            print l

        return render(request,"teacher_home.html",{'list':l})
    return render(request,"home.html")


def log_in(request):
    if request.method == "POST":
        user = authenticate(username = request.POST['uname'],
                            password = request.POST['passwd']
                            )
        print user
        if user is not None:
            if user.is_active:
                login(request, user)
                if is_teacher(request):
                    return teacher_home(request)
                else:
                    return student_home(request)
        else:
            return HttpResponse("<script>alert('Wrong Username or password combination!');window.location.href = '/';</script>")
    elif is_student(request):
        return student_home(request)
    elif is_teacher(request):
        return teacher_home(request)
    return render(request,"home.html")


def sign_up_stud(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username= request.POST['uname'],
            password= request.POST['passwd'],
            email = request.POST['email'],
            first_name = request.POST['fname'],
            last_name = request.POST['lname'],
        )
        Student.objects.create(user = user,rollno = request.POST['rollno'])
        try:
            MyBatch.objects.create(user = user,
                                   batch = Batch.objects.get(bname = request.POST.get('optradio')),
                                   )
        except:
            print "!!!!!!!!!!!!!!!!!Batch Creation Error!!!!!!!!!!!!!!!!!"
            Student.objects.filter(user=user, rollno = request.POST['rollno']).delete()
            User.objects.filter(username = request.POST['uname']).delete()
            raise Http404("Please select a correct Batch!!")
        try:
            mkdir(join('Uploads', str(user.id)))
        except:
            pass
        return HttpResponse("<script>alert('Signup Successful. Please Login!!');window.location.href = '/';</script>")
    return render(request,"home.html")


def sign_up_teach(request):
    if is_teacher(request):
        return teacher_home(request)
    elif is_student(request):
        return student_home(request)

    elif request.method=="POST":
        user = User.objects.create_user(
            username = request.POST['uname'],
            password = request.POST['passwd'],
            email = request.POST['email'],
            first_name = request.POST['fname'],
            last_name = request.POST['lname']
        )

        Teacher.objects.create(user = user,emp_no = request.POST['empno'])
        try:
            batch_list = request.POST.getlist('batch')
            for i in batch_list:
                MyBatch.objects.create(batch = Batch.objects.get(bname=i), user =user )
        except:
            print "!!!!!!!!!!!!!!!!!Batch Creation Error!!!!!!!!!!!!!!!!!"
            Teacher.objects.filter(user=user).delete()
            User.objects.filter(username=request.POST['uname']).delete()
            raise Http404("Please select a correct Batch!!")
        return HttpResponse("<script>alert('Signup Successful. Please Login!!');window.location.href = '/';</script>")
    return render(request,"home.html")


@csrf_exempt
def assignment_view(request):
    if is_student(request):
        if request.method == "GET":
            x = int(request.GET.get('x'))
            if x is None:
                return HttpResponse("!!!!!!!!!!Error!!!!!!!!")
            try:
                a = Assignment.objects.get(id=x)
                b = MyBatch.objects.get(user=request.user)
            except:
                return HttpResponse("!!!!!!!!!!Error!!!!!!!!")
            if a.to_batch != b.batch:
                return HttpResponse("!!!!!!!!!!Error!!!!!!!!")
            return render(request,"assignment_view_stud.html",{'a':a})
        return student_home(request)

    elif is_teacher(request):
        subjects = Subject.objects.all()
        options = MyBatch.objects.filter(user=request.user)
        if request.method == "POST":
            return render(request,"assignment_view_teach.html",{'flag':False,'options':options,'subjects':subjects})
        else:
            x = request.GET.get('x')
            if x is None:
                return render(request,"assignment_view_teach.html",{'flag':False,'options':options,'subjects':subjects})
            a = Assignment.objects.get(id=x,
                                          assigned_by=Teacher.objects.get(user=request.user)
                                        )
            return render(request,"assignment_view_teach.html",{'flag':True,'a':a,'options':options,'subjects':subjects})
    return render(request,"home.html")


def add_assignment(request):
    if is_teacher(request):
        if request.method == "POST":
            Assignment.objects.create(
                title = request.POST['title'],
                deadline = request.POST['datetime'],
                sub = Subject.objects.get(id=request.POST['sub']),
                assigned_by = Teacher.objects.get(user=request.user),
                to_batch = Batch.objects.get(bname=request.POST['batch']),
                problem_statement = request.POST['desc']
            )
        return teacher_home(request)
    elif is_student(request):
        return student_home(request)
    return render(request,"home.html")


def submit(request):
    if is_student(request):
        if request.method == "POST":
            try:
                a = request.FILES['pdf']
            except:
                return HttpResponse("Please select a file")
            f = MyForm(request.POST,request.FILES)
            if f.is_valid():
                try:
                    valid_file = f.clean_content()
                except ValidationError as e:
                    return HttpResponse(e.message)

                assignment = Assignment.objects.get(id=int(request.POST['id']))
                try:
                    sub = Submission.objects.get(user = request.user,
                                           assignment = assignment
                                            )
                    sub.is_checked = False
                    if assignment.deadline.microsecond < datetime.now().microsecond:
                        sub.is_late = True
                    sub.save()
                except:
                    sub = Submission.objects.create(user=request.user,
                                                    assignment=assignment
                                                    )
                    if assignment.deadline.microsecond < datetime.now().microsecond:
                        sub.is_late = True
                        sub.save()
                with open(join(settings.BASE_DIR ,'Uploads/'+str(request.user.id))+'/'+str(request.POST['id'])+'.pdf', 'wb+') as destination:
                    for chunk in valid_file.chunks():
                        destination.write(chunk)
            else:
                return HttpResponse("Select a file")

        return student_home(request)
    elif is_teacher(request):
        return teacher_home(request)
    return render(request,"home.html")

def remark(request):
    if is_student(request):
        if Submission.objects.filter(user=request.GET['u'],
                                     assignment = Assignment.objects.get(id=request.GET['a'])
                                    ):
            s = Submission.objects.get(user=request.GET['u'],
                                     assignment = Assignment.objects.get(id=request.GET['a'])
                                    )
            if s.is_checked:
                html = "<div style='text-align:left;'><label class='col-md-3 control-label' for='title'>Score: </label><div class='col-md-9'><div class='progress'><div class='progress-bar' role='progressbar' aria-valuenow="+str(s.scale)+" aria-valuemin='0' aria-valuemax='10' style='width:"+str(s.scale)+"0%'>"+str(s.scale)+"</div></div></div><br><br><label class='col-md-3 control-label' for='title'>Remark: </label><div class='col-md-9'>"+str(s.remark)+"</div></div>"
                return HttpResponse(html)
            else:
                return HttpResponse("<h2 style='color:black;'>Yet to be checked!!</h2>")
        else:
            return HttpResponse("<h2 style='color:red;'>First Submit the Assignment!!</h2>")
    return HttpResponse("Error!!")


def ret_file(request):
    if is_teacher(request):
        if request.method=="GET":
            file_name = str(request.GET['aid'])+".pdf"
            path_to_file = join(settings.BASE_DIR,"Uploads/"+str(request.GET['uid'])+"/"+file_name)
            print path_to_file
            with open(path_to_file, 'rb') as pdf:
                response = HttpResponse(pdf.read(),content_type='application/pdf')
                response['Content-Disposition'] = 'filename=download.pdf'
                return response
            var = pdf.closed


def check_list(request):
    if is_teacher(request):
        if request.method=="GET":
            myb = request.GET['b']
            a = request.GET['a']
            if myb is not None and a is not None:
                if MyBatch.objects.filter(id=myb).exists() and Assignment.objects.filter(id=a).exists():
                    asgnmnt = Assignment.objects.get(id=a)
                    sub = Submission.objects.filter(assignment=asgnmnt,is_checked=False)

                    return render(request,"check_list.html",{'sublist':sub,'b':myb})
        return teacher_home(request)
    elif is_student(request):
        return student_home(request)
    return render(request,"home.html")


def grade_de(requset):
    if is_teacher(requset):
        if requset.method=="GET":
            s = requset.GET['s']
            b = requset.GET['b']
            if s is not None:
                try:
                    sub = Submission.objects.get(id=s)
                except:
                    return HttpResponse("Invalid Submission")
                return render(requset,"grade_teach.html",{'sub':sub,'b':b})
        return teacher_home(requset)
    elif is_student(requset):
        return student_home(requset)
    return render(requset,"home.html")

def remark_sub(request):
    if is_teacher(request):
        if request.method=="POST":
            marks = int(request.POST.get('optradio'))
            rmark = request.POST['remark']
            uid = request.POST['uid']
            aid = request.POST['aid']

            try :
                sub = Submission.objects.get(assignment=Assignment.objects.get(id=aid),
                                             user=User.objects.get(id=uid)
                                            )
                if marks<0 or marks>10:
                    raise ValueError("Are Limit madhe!!")
            except:
                return HttpResponse("Error")
            sub.scale = marks
            sub.remark = rmark
            sub.is_checked=True
            sub.save()


            link = '/check_list/?b='+str(request.POST['b'])+'&a='+str(aid)
            return HttpResponseRedirect(link)


def create_batches(request):

    b= ["K1","L1","M1","N1","K2","L2","M2","N2","K3","L3","M3","N3","K4","L4","M4","N4"]
    for i in b:
        Batch.objects.create(bname = i)

    s = ["CFCA","OSD","DMSA","DCWSN","TOC","PL I","PL II","ESDL"]
    for i in s:
        Subject.objects.create(name = i)
    return HttpResponse("Created Successfully")


def contact_us(request):
    return render(request,"contact_us.html")


def log_out(request):
    logout(request)
    return render(request,'home.html')