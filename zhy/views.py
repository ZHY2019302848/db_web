import json

import MySQLdb
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import reverse

from django.contrib import messages


# Create your views here.

username =""



def register(request):
    global  username
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        #username, email=None, password=None, **extra_fields
        user = User.objects.create_user(username=username,password=password)
        user.save()
        if user:
            auth.login(request, user)
            return redirect('../login')
    return render(request,'student/register.html')





def leader(request):
    return render(request, 'student/leader.html')


# 登录系统
def do_login(request):
    global username
    username = request.POST.get('username')
    password = request.POST.get('password')
    print(username)
    print("\n")
    print(password)
    if (username == 'root' and password == '000815'):
        return redirect('../leader')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)  # 这里做了登录
            return redirect('../leader')
        #return render(request, "../leader")
        #return render(request, 'student/login.html', {
        #    'username': username,
       #     'password': password
       # })


def login(request):
    return render(request, 'student/login.html')


# 学生信息列表处理函数
def index(request):
    global username
    print("用户名_index:\n")
    print(username)
    student_no = request.GET.get('student_no', '')
    student_name = request.GET.get('student_name', '')
    student_gender = request.GET.get('student_gender', '')
    sql = "SELECT student_no,student_name ,student_age,student_birth,student_gender,student_sdept FROM zhy_student WHERE 1=1 "
    if student_no.strip() != '':
        sql = sql + " and student_no = '" + student_no + "'"
    if student_name.strip() != '':
        sql = sql + " and student_name = '" + student_name + "'"
    if student_gender.strip() != '':
        sql = sql + " and student_gender = '" + student_gender + "'"


    print(sql)

    conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute(sql)
        students = cursor.fetchall()
    return render(request, 'student/index.html', {'students': students,
                                                  'student_no': student_no, 'student_name': student_name})




# 学生信息新增处理函数
def add(request):
    print("用户名:\n")
    print(username)
    if request.method == 'GET':
        if username == 'root':
         return render(request, 'student/add.html')

        else:
         messages.error(request, '您没有相关权限')
         return redirect('../index')

    else:
        student_no = request.POST.get('student_no', '')
        student_name = request.POST.get('student_name', '')
        student_age = request.POST.get('student_age', '')
        student_birth = request.POST.get('student_birth', '')
        student_gender = request.POST.get('student_gender', '')
        student_sdept = request.POST.get('student_sdept', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("select * from zhy_student,zhy_c where student_no = %s ", [student_no])
            inquiry = cursor.fetchone()
            if inquiry == None:
             cursor.execute(
                "INSERT INTO zhy_student (student_no,student_name,student_age,student_birth,student_gender,student_sdept) "
                "values (%s,%s,%s,%s,%s,%s)",
                [student_no, student_name, student_age, student_birth, student_gender, student_sdept])
             conn.commit()
            else:
              messages.error(request, '该学号相关信息已存在不可再次添加')
        return redirect('../index')


# 学生信息修改处理函数
def edit(request):
    if request.method == 'GET':
        student_no = request.GET.get("student_no")
        print(student_no)
        if username == student_no or username == "root":
         conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
         with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SELECT student_no,student_name,student_age,student_birth,student_gender,student_sdept FROM zhy_student where student_no =%s", [student_no])
            student = cursor.fetchone()
         return render(request, 'student/edit.html', {'student': student})
        else:
         messages.error(request, '您没有相关权限')
         return redirect('../index')
    else:
        student_no = request.POST.get('student_no', '')
        student_name = request.POST.get('student_name', '')
        student_age = request.POST.get('student_age', '')
        student_birth = request.POST.get('student_birth', '')
        student_gender = request.POST.get('student_gender', '')
        student_sdept = request.POST.get('student_sdept', '')

        conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:

            cursor.execute(
                "UPDATE zhy_student set student_name=%s,student_age=%s,student_birth=%s,student_gender=%s,student_sdept=%s where student_no =%s",
                [student_name, student_age, student_birth, student_gender, student_sdept, student_no])
            conn.commit()

        return redirect('../index')


# 学生信息删除处理函数
def delete(request):
    student_no = request.GET.get("student_no")
    if username == "root":
     conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
     with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("DELETE FROM zhy_student WHERE student_no =%s", [student_no])
        conn.commit()
    else:
        messages.error(request, '您没有相关权限')
    return redirect('../index')

#课程信息列表处理函数
def index_c(requset):
    cno = requset.GET.get('cno', '')
    cname = requset.GET.get('cname', '')

    sql = "SELECT id,cno,cname,credit FROM zhy_c WHERE 1=1 "
    if cno.strip() != '':
        sql = sql + " and cno = '" + cno + "'"
    if cname.strip() != '':
        sql = sql + " and cname = '" + cname + "'"

    print(sql)
    conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute(sql)
        courses = cursor.fetchall()
    return render(requset, 'student/index_c.html', {'courses': courses,'id':id,
                                                  'cno': cno, 'cname':cname})


#课程信息添加函数
def add_c(request):
    if request.method == 'GET':
        if username == "root":
            return render(request, 'student/add_c.html')
        else:
            messages.error(request, '您没有相关权限')
            return redirect('../index_c')

    else:
        cno = request.POST.get('cno', '')
        cname = request.POST.get('cname', '')
        credit = request.POST.get('credit', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("select * from zhy_c where cno = %s ", [cno])
            inquiry = cursor.fetchone()
            if inquiry == None:
             cursor.execute(
                "INSERT INTO zhy_c (cno,cname,credit) "
                "values (%s,%s,%s)",
                [cno, cname, credit])
             conn.commit()
            else:
             messages.error(request, '该课程号相关信息已存在不可再次添加')

        return redirect('../index_c')


#课程信息修改函数
def edit_c(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        print(id)
        if username == "root":
         conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
         with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SELECT id,cno,cname,credit FROM zhy_c where id =%s", [id])
            course = cursor.fetchone()
         return render(request, 'student/edit_c.html', {'course': course})
        else:
         messages.error(request, '您没有相关权限')
         return redirect('../index_c')

    else:
        id = request.POST.get("id")
        print(id)
        cno = request.POST.get('cno', '')
        print(cno)
        cname = request.POST.get('cname', '')
        print(cname)
        credit = request.POST.get('credit', '')
        print(credit)

        conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:

            cursor.execute(
                "UPDATE zhy_c set cno=%s,cname=%s,credit=%s where id =%s",
                [cno, cname, credit, id])
            conn.commit()
        return redirect('../index_c')

#课程信息删除函数
def delete_c(request):
    id = request.GET.get("id")
    if username == "root":
     conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
     with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("DELETE FROM zhy_c WHERE id =%s", [id])
        conn.commit()
    else:
        messages.error(request, '您没有相关权限')

    return redirect('../index_c')



def index_sc(requset):
    student_no = requset.GET.get('student_no', '')
    cno = requset.GET.get('cno', '')

    sql = "SELECT id,student_no,cno,mark FROM zhy_sc WHERE 1=1 "
    if student_no.strip() != '':
        sql = sql + " and student_no = '" + student_no + "'"
    if cno.strip() != '':
        sql = sql + " and cno = '" + cno + "'"


    print(sql)
    conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute(sql)
        scs = cursor.fetchall()
    return render(requset, 'student/index_sc.html', {'scs': scs,
                                                  'student_no': student_no, 'cno':cno})


#课程信息添加函数
def add_sc(request):
    if request.method == 'GET':
        if username == "root":
         return render(request, 'student/add_sc.html')
        else:
            messages.error(request, '您没有相关权限')
            return redirect('../index_sc')
    else:
        cno = request.POST.get('cno', '')
        student_no = request.POST.get('student_no', '')
        mark = request.POST.get('mark', '')
        conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("select * from zhy_student,zhy_c where student_no = %s and cno = %s", [student_no, cno])
            inquiry = cursor.fetchone()
            if inquiry == None:
                messages.error(request, '学生或课程不存在，无法插入')
                return redirect('../index_sc')
            else:
                 messages.error(request, '添加成功')
                 cursor.execute(
                "INSERT INTO zhy_sc (student_no,cno,mark) "
                "values (%s,%s,%s)",
                [student_no, cno, mark])
            conn.commit()
        return redirect('../index_sc')


#课程信息修改函数
def edit_sc(request):

    if request.method == 'GET':
        id = request.GET.get("id")
        print(id)
        if username == "root":
         conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
         with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("SELECT id,student_no,cno,mark FROM zhy_sc where id =%s", [id])
            sc = cursor.fetchone()
         return render(request, 'student/edit_sc.html', {'sc': sc})
        else:
            messages.error(request, '您没有相关权限')
            return redirect('../index_sc')
    else:
        id = request.POST.get("id")
        student_no = request.POST.get('student_no', '')
        cno= request.POST.get('cno', '')
        mark = request.POST.get('mark', '')

        conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
        with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:

           cursor.execute("select * from zhy_student,zhy_c where student_no = %s and cno = %s",[student_no,cno])
           inquiry = cursor.fetchone()
           if inquiry == None:
               messages.error(request, '学生或课程不存在，无法修改')
               return redirect('../index_sc')
           else:
              messages.error(request,'修改成功')
              cursor.execute(
                "UPDATE zhy_sc set student_no=%s,cno=%s,mark=%s where id =%s",
                [student_no, cno, mark, id])
              conn.commit()
        return redirect('../index_sc')

#课程信息删除函数
def delete_sc(request):
    id = request.GET.get("id")
    if username == "root":
     conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
     with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute("DELETE FROM zhy_sc WHERE id =%s", [id])
        conn.commit()
    else:
        messages.error(request, '您没有相关权限')
    return redirect('../index_sc')


def chart(request):

    sql = "SELECT zhy_sc.student_no as student_no,student_name, sum(mark*credit)/sum(credit) as avgm FROM zhy_sc,zhy_c,zhy_student WHERE zhy_c.cno = zhy_sc.cno  and zhy_sc.student_no=zhy_student.student_no group by student_no;"
    sql1 = "call proc_addNum(90.0000,100.0000,@sum)"
    sql2 = "select @sum"
    sql3 = "call proc_addNum(80.0000,89.9999,@sum)"
    sql4 = "call proc_addNum(70.0000,79.9999,@sum)"
    sql5 = "call proc_addNum(60.0000,69.9999,@sum)"
    sql6 = "call proc_addNum(0.0000,59.9999,@sum)"
    conn = MySQLdb.connect(host="localhost", user="root", passwd="Zhy000815", db="carol", charset='utf8')
    with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        cursor.execute(sql)
        chs = cursor.fetchall()
        cursor.execute(sql1)
        cursor.execute(sql2)
        data_90 = cursor.fetchone()
        cursor.execute(sql3)
        cursor.execute(sql2)
        data_80 = cursor.fetchone()
        cursor.execute(sql4)
        cursor.execute(sql2)
        data_70 = cursor.fetchone()
        cursor.execute(sql5)
        cursor.execute(sql2)
        data_60 = cursor.fetchone()
        cursor.execute(sql6)
        cursor.execute(sql2)
        data_0 = cursor.fetchone()

        return render(request, 'student/chart.html',{'chs': chs , 'data_90':json.dumps(data_90),'data_80':json.dumps(data_80),
                                                     'data_70':json.dumps(data_70),'data_60':json.dumps(data_60),
                                                      'data_0':json.dumps(data_0)})