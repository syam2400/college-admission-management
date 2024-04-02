from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from AdminUI.models import DepartmentDB, CourseDB, StudentDB, FacultyEnrollmentDB, JobsDB, JobApplications, newsDB, \
    placed_studdb, Marquee, newsDB2, InterviewStep, JobStatus2,TrainingDB
from FacultyUI.models import FacultyDB
from .forms import MarqueeForm
import pandas as pd

# Create your views here.


def admin_indexpage(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)

        return render(request,'adminindex.html',{'name': name})
    else:
        return redirect('main_page')





def add_dept(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        return render(request, "AddDepartment.html",{'name': name})
    else:
        return redirect('main_page')

def submit_dept(request):
    if request.method == "POST":
        dep = request.POST.get("deptname")
        obj = DepartmentDB(DeptName=dep)
        obj.save()
        return redirect(view_dept)


def view_dept(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        data = DepartmentDB.objects.all()
        return render(request, "ViewDepartments.html", {"data": data,'name':name})
    else:
        return redirect('main_page')


def edit_dept(request, dataid):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        data = DepartmentDB.objects.get(DeptId=dataid)
        return render(request, "EditDepartment.html", {"data": data,'name':name})
    else:
        return redirect('main_page')


def update_dept(request, dataid):
    if request.method == "POST":
        dep = request.POST.get("deptname")
        DepartmentDB.objects.filter(DeptId=dataid).update(DeptName=dep)
        return redirect(view_dept)
    else:
        return redirect('main_page')


def delete_dept(request, dataid):
    data = DepartmentDB.objects.filter(DeptId=dataid)
    data.delete()
    return redirect(view_dept)


def add_course(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        data = DepartmentDB.objects.all()
        return render(request, "AddCourse.html", {'data': data,'name':name})
    else:
        return redirect('main_page')


def submit_course(request):
    if request.method == "POST":
        course = request.POST.get("coursename")
        dep = request.POST.get("deptname")
        dept_data = DepartmentDB.objects.get(DeptName=dep)
        dept = dept_data.DeptId
        print(dept)
        desc = request.POST.get("course_desc")
        print(dep)
        obj = CourseDB(CourseName=course, DeptId=dept_data, Description=desc)
        obj.save()
        return redirect(add_course)


def view_course(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        data = CourseDB.objects.all()
        return render(request, "ViewCourse.html", {"data": data,'name':name})
    else:
        return redirect('main_page')


def edit_course(request, dataid):
    data = CourseDB.objects.get(CourseId=dataid)
    dep_data = DepartmentDB.objects.all()
    print(data)
    # return redirect(add_course)
    return render(request, "EditCourse.html", {"data": data, "dep_data": dep_data})


def update_course(request, dataid):
    if request.method == "POST":
        course = request.POST.get("coursename")
        dep = request.POST.get("deptname")
        dept_data = DepartmentDB.objects.get(DeptName=dep)
        print(dept_data)
        dept = dept_data.DeptId
        desc = request.POST.get("course_desc")
        CourseDB.objects.filter(CourseId=dataid).update(CourseName=course, DeptId=dept, Description=desc)
        return redirect(view_course)


def delete_course(request, dataid):
    data = CourseDB.objects.filter(id=dataid)
    data.delete()
    return redirect(view_course)


def add_student(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        data = CourseDB.objects.all()
        return render(request, "AddStudent.html", {"data": data,"name":name})
    else:
        return redirect('main_page')

def add_student2(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)

        return render(request, "AddStudentsExcel.html",{"name":name})
    else:
        return redirect('main_page')
def submit_student(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        enid = request.POST.get("enid")
        endate = request.POST.get("endate")
        course = request.POST.get("course")
        course_data = CourseDB.objects.get(CourseName=course)
        coursee = course_data.CourseId
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        address = request.POST.get("address")
        gname = request.POST.get("gname")
        gcontact = request.POST.get("gcontact")
        im = request.FILES['img']
        obj = StudentDB(FirstName=fname, LastName=lname, EnrollmentID=enid, EnrollDate=endate, CourseId=course_data,
                        DateOfBirth=dob, Gender=gender, Email=email, ContactNo=contact, Address=address,
                        GuardianName=gname, GuardianContact=gcontact, Image=im, password=contact)
        obj.save()
        return redirect(add_student)

def submit_student_from_excel(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        if excel_file.name.endswith('.xlsx'):
            try:
                # Read Excel file into a pandas DataFrame
                df = pd.read_excel(excel_file)

                # Iterate over rows and create StudentDB objects
                for index, row in df.iterrows():
                    student = StudentDB(
                        FirstName=row['First Name'],
                        LastName=row['Last Name'],
                        EnrollmentID=row['Enrollment ID'],
                        EnrollDate=row['Enrollment Date'],
                        CourseId=row['Course'],
                        DateOfBirth=row['Date of Birth'],
                        Gender=row['Gender'],
                        Email=row['Email'],
                        ContactNo=row['Contact Number'],
                        Address=row['Address'],
                        GuardianName=row['Guardian Name'],
                        GuardianContact=row['Guardian Contact Number'],
                        # Assuming 'Image' field is handled separately
                    )
                    student.save()

                return redirect('view_students')  # Redirect to a success page or the form page
            except Exception as e:
                # Handle exceptions (e.g., invalid file format, missing columns, etc.)
                return render(request, 'error.html', {'error': str(e)})
        else:
            # Handle invalid file format
            return render(request, 'error.html', {'error': 'Invalid file format. Please upload an Excel file !'})
    else:
        # Handle GET requests or requests without a file
        return render(request, 'AddStudentsExcel.html')


def view_students(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        data = CourseDB.objects.all()
        stud_data = StudentDB.objects.all()
        years = set()
        for i in stud_data:
            year = i.EnrollDate.year
            years.add(year)  # Using a set ensures unique years
        print(years)
        return render(request, "ViewStudents.html", {"data": data, "years": years,"name":name})
    else:
        return redirect('main_page')


def search_students(request):
    if request.method == "POST":
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        course = request.POST.get("course")
        course_data = CourseDB.objects.get(CourseName=course)
        print(course_data)
        cours = course_data.CourseId
        year = request.POST.get("year")
        data = StudentDB.objects.filter(CourseId=cours, EnrollDate__year=year)
        print(course)
        return render(request, "ViewStudentsCourseWise.html", {"data": data, "course": course,'name':name})
    else:
        return redirect('main_page')

def view_single_student(request, dataid):
    if 'username' in request.session:
        data = StudentDB.objects.get(StudentId=dataid)
        course_data = CourseDB.objects.all()
        return render(request, "ViewSingleStudent.html", {"data": data, "course_data": course_data})
    else:
        return redirect('main_page')

def update_student(request, dataid):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        enid = request.POST.get("enid")
        endate = request.POST.get("endate")
        date_obj = datetime.strptime(endate, "%b. %d, %Y")
        formatted_endate = date_obj.strftime("%Y-%m-%d")
        course = request.POST.get("course")
        course_data = CourseDB.objects.get(CourseName=course)
        coursee = course_data.CourseId
        dob = request.POST.get("dob")
        date_objj = datetime.strptime(dob, "%b. %d, %Y")
        formatted_dob = date_objj.strftime("%Y-%m-%d")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        address = request.POST.get("address")
        gname = request.POST.get("gname")
        gcontact = request.POST.get("gcontact")
        try:
            im = request.FILES['img']
            fs = FileSystemStorage()
            file = fs.save(im.name, im)
        except MultiValueDictKeyError:
            file = StudentDB.objects.get(StudentId=dataid).Image
        StudentDB.objects.filter(StudentId=dataid).update(FirstName=fname, LastName=lname, EnrollmentID=enid,
                                                          EnrollDate=formatted_endate, CourseId=course_data,
                                                          DateOfBirth=formatted_dob, Gender=gender, Email=email,
                                                          ContactNo=contact, Address=address, GuardianName=gname,
                                                          GuardianContact=gcontact, Image=file, password=contact)
        return redirect(view_students)


def delete_student(request, dataid):
    data = StudentDB.objects.filter(StudentId=dataid)
    data.delete()
    return redirect(view_students)


def add_faculty(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        data = DepartmentDB.objects.all()
        return render(request, "AddFaculty.html", {"data": data,"name":name})
    else:
        return redirect('main_page')

def submit_faculty(request):
    if request.method == "POST":
        name = request.POST.get("name")
        endate = request.POST.get("date")
        dept = request.POST.get("dept")
        dept_data = DepartmentDB.objects.get(DeptName=dept)
        deptt = dept_data.DeptId
        contact = request.POST.get("contact")
        desig = request.POST.get("designation")
        status = request.POST.get("admin_status")
        if status:
            obj = FacultyEnrollmentDB(Name=name, Joined=endate, DeptId=dept_data, Designation=desig, Contact=contact,
                                      is_admin="True")
            obj.save()
        else:
            obj = FacultyEnrollmentDB(Name=name, Joined=endate, DeptId=dept_data, Designation=desig, Contact=contact,
                                      is_admin="False")
            obj.save()

        return redirect(add_faculty)


def view_faculties(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        data = FacultyEnrollmentDB.objects.all()
        return render(request, "ViewFaculties.html", {"data": data,'name':name})
    else:
        return redirect('main_page')

def search_faculties(request):
    if request.method == "POST":
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        dept = request.POST.get("dept")
        dept_data = DepartmentDB.objects.get(DeptName=dept)
        dep = dept_data.DeptId
        data = FacultyEnrollmentDB.objects.filter(DeptId=dep)
        return render(request, "ViewFacultyDepWise.html", {"data": data, "dept": dept,'name':name})


def view_single_faculty(request, dataid):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        data = FacultyEnrollmentDB.objects.get(FacultyID=dataid)
        try:
            dat = FacultyDB.objects.get(FacultyID=dataid)
        except FacultyDB.DoesNotExist:
            dat = None
        dep_data = DepartmentDB.objects.all()
        return render(request, "ViewSingleFaculty.html", {"data": data, "dep_data": dep_data, "dat": dat,"name":name})
    else:
        return redirect('main_page')

def admin_signin(request):
    if request.method == "POST":
        uname = request.POST.get('login-username')
        pw = request.POST.get('login-password')
        # print(uname)
        # print(pw)
        if User.objects.filter(username__contains=uname).exists():

            user = authenticate(username=uname, password=pw)
            if user is not None:
                login(request, user)
                request.session['username'] = uname
                request.session['password'] = pw
                # messages.success(request, "Logined successfully")
                return redirect(admin_indexpage)
            else:
                # messages.error(request, "Check the credentials")
                return redirect(admin_login)
        elif User.objects.filter(username=uname, password=pw).exists():
            request.session['username'] = uname
            request.session['password'] = pw
            # messages.success(request, "Logined successfully")
            return redirect(admin_indexpage)
        else:
            # messages.error(request, "Check the credentials")
            return redirect(admin_login)


def admin_login(request):
    return render(request, "AdminLogin.html")


def add_job(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        return render(request, "AddJobOpenings.html",{'name':name})

    else:
        return redirect('main_page')

# def job_save(request):
#     if request.method == "POST":
#         title = request.POST.get("title")
#         company = request.POST.get("cname")
#         location = request.POST.get("location")
#         qualification = request.POST.get("qualification")
#         description = request.POST.get("description")
#         email = request.POST.get("email")
#         im = request.FILES['image']
#         obj = JobsDB(Title=title, Company=company, Location=location, Qualification=qualification,
#                      Description=description, Email=email, image_job=im)
#         obj.save()
#         return redirect(add_job)

def job_save(request):
    if request.method == "POST":
        title = request.POST.get("title")
        company = request.POST.get("cname")
        location = request.POST.get("location")
        qualification = request.POST.get("qualification")
        description = request.POST.get("description")
        email = request.POST.get("email")
        im = request.FILES['image']

        # Extracting interview steps from the form
        interview_steps = request.POST.getlist('interview_step[]')

        # Creating a job object and saving it to the database
        obj = JobsDB(Title=title, Company=company, Location=location, Qualification=qualification,
                     Description=description, Email=email, image_job=im)
        obj.save()

        # Saving interview steps associated with the job
        for step_text in interview_steps:
            step = InterviewStep(job=obj, step_text=step_text)
            step.save()

        return redirect(add_job)


def view_jobs(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        job_data = JobsDB.objects.all()
        return render(request, "ViewJobs.html", {'job_data': job_data,'name':name})
    else:
        return redirect('main_page')

def job_delete(request, data_id):
    job_data = JobsDB.objects.filter(JobId=data_id)
    job_data.delete()
    return redirect(view_jobs)


# def view_job_single(request, data_id):
#     if 'username' in request.session:
#         stud_id = request.session["username"]
#         student = StudentDB.objects.get(StudentId=stud_id)
#     job_data = JobsDB.objects.get(JobId=data_id)
#     return render(request, "ViewJobSingle.html", {'job_data': job_data, 'student': student})


def view_job_single(request, data_id):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        job_data = JobsDB.objects.get(JobId=data_id)
        return render(request, "ViewJobSingle.html", {'job_data': job_data,'name':name})
    else:
        return redirect('main_page')

def update_job(request, job_id):
    if request.method == "POST":
        title = request.POST.get("title")
        company = request.POST.get("cname")
        location = request.POST.get("location")
        qualification = request.POST.get("qualification")
        description = request.POST.get("description")
        email = request.POST.get("email")
        JobsDB.objects.filter(JobId=job_id).update(Title=title, Company=company, Location=location,
                                                   Qualification=qualification,
                                                   Description=description, Email=email)
        return redirect(view_jobs)


def job_applications(request, job_id):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        job_data = JobsDB.objects.get(JobId=job_id)
        # job_statuses = JobStatus2.get(job=job_id)
        applications = JobApplications.objects.filter(JobId=job_data)
        return render(request, "JobApplications.html", {'applications': applications,'name':name})
    else:
        return redirect('main_page')


def resume_download(request, stud_id, job_id):
    data = JobApplications.objects.filter(JobId=job_id)
    pdf_file = get_object_or_404(data, StudentId=stud_id)
    response = FileResponse(pdf_file.Resume, as_attachment=True)
    return response


def application_single(request, dataid):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        data = StudentDB.objects.get(StudentId=dataid)
        course_data = CourseDB.objects.all()

        return render(request, "ApplicationDetail.html", {"data": data, "course_data": course_data,'name':name})
    else:
        return redirect('main_page')


def add_news(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        return render(request, "add_news.html",{'name':name})
    else:
        return redirect('main_page')


def add_news2(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        return render(request, "addnews2.html",{'name':name})
    else:
        return redirect('main_page')

def news_save(request):
    if request.method == "POST":
        title = request.POST.get("news_Title")
        company = request.POST.get("news_Location")
        location = request.POST.get("news_date")
        date_obj = datetime.strptime(location, "%d-%m-%Y")
        formatted_endate = date_obj.strftime("%Y-%m-%d")
        description = request.POST.get("Description")
        im = request.FILES['image']
        obj = newsDB(news_Title=title, news_Location=company, news_date=formatted_endate,
                     Description=description, news_image=im)
        obj.save()
        return redirect(add_news2)


def news_save2(request):
    if request.method == "POST":
        title = request.POST.get("news_Title")
        company = request.POST.get("news_Location")
        location = request.POST.get("news_date")
        date_obj = datetime.strptime(location, "%d-%m-%Y")
        formatted_endate = date_obj.strftime("%Y-%m-%d")
        description = request.POST.get("Description")
        im = request.FILES['image']
        obj = newsDB2(news_Title=title, news_Location=company, news_date=formatted_endate,
                      Description=description, news_image=im)
        obj.save()
        return redirect(add_news2)


def news_view(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        obj = newsDB.objects.all()
        return render(request, "news_view.html", {"obj": obj,'name':name})

    else:
        return redirect('main_page')


def news_view2(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        obj = newsDB2.objects.all()
        return render(request, "viewnews2.html", {"obj": obj,'name':name})
    else:
        return redirect('main_page')

def news_delete(request, data_id):
    job_data = newsDB.objects.filter(newsId=data_id)
    job_data.delete()
    return redirect(news_view)


def news_delete2(request, data_id):
    job_data = newsDB2.objects.filter(newsId=data_id)
    job_data.delete()
    return redirect(news_view2)


def placed(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        return render(request, "placed.html",{'name':name})
    else:
        return redirect('main_page')

def add_placed(request):
    if request.method == "POST":
        na = request.POST.get("p_name")
        comp = request.POST.get("p_company")
        des = request.POST.get("p_des")
        dis = request.POST.get("p_dis")
        img = request.FILES["p_img"]
        obj = placed_studdb(p_name=na, p_company=comp, p_des=des, p_dis=dis, p_img=img)
        obj.save()
        return redirect(display_placed)


def display_placed(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        data = placed_studdb.objects.all()
        return render(request, "display_placed.html", {'data': data,"name":name})
    else:
        return redirect('main_page')

def placed_delete(request, data_id):
    placed_data = placed_studdb.objects.filter(p_id=data_id)
    placed_data.delete()
    return redirect(display_placed)


def add_marquee(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        if request.method == 'POST':
            form = MarqueeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('marquee_list')  # Redirect to view page after saving
        else:
            form = MarqueeForm()
        return render(request, 'AddAlerts.html', {'form': form,'name':name})
    else:
        return redirect('main_page')

def marquee_list(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        marquee_list = Marquee.objects.all()
        return render(request, 'ViewAlerts.html', {'marquee_list': marquee_list,"name":name})
    else:
        return redirect('main_page')




def delete_marquee(request, marquee_id):
    if request.method == 'POST':
        marquee = Marquee.objects.get(pk=marquee_id)
        marquee.delete()
    return redirect('marquee_list')


# def job_details(request, data):
#     # Retrieve the job status object based on the job_status_id
#
#     job_status1 = JobStatus2.objects.get(job=data.Company)
#     # Pass job status to the template for rendering
#     return render(request, 'job_status_detail.html', {'job_status': job_status1})


def job_details(request):
    if 'username' in request.session:
        # Retrieve the job status object based on the job_status_id
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        job_statuses = JobStatus2.objects.all()
        # Pass job status to the template for rendering
        return render(request, 'job_status_detail.html', {'job_status': job_statuses,'name':name})
    else:
        return redirect('main_page')
def statussearch(request):
    if 'username' in request.session:
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        data = CourseDB.objects.all()
        data2 = TrainingDB.objects.all()
        stud_data = StudentDB.objects.all()
        years = []
        for i in stud_data:
            year = i.EnrollDate.year
            years.append(year)
        print(years)
        return render(request, "dashboard.html", {"data": data,"data2":data2,'name':name})
    else:
        return redirect('main_page')


def search_studentstatus(request):
    if request.method == 'POST':
        course_name = request.POST.get('course')
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)

        # Filter job statuses based on the selected course
        job_statuses = JobStatus2.objects.filter(course__CourseName=course_name)

        context = {
            'course_name': course_name,
            'job_statuses': job_statuses,
            'name':name
        }
        return render(request, 'Viewstudentstatus.html', context)
    else:
        courses = CourseDB.objects.all()
        return render(request, 'dashboard.html', {'data': courses})
from django.db.models import Max

def delete_status(request, status_id):
    # Retrieve the JobStatus2 object to be deleted
    status = get_object_or_404(JobStatus2, pk=status_id)

    # Delete the status
    status.delete()

    # Redirect back to the same page or any other appropriate page
    return redirect('search_studentstatus')  # Adjust the URL name as needed


def search_trainings(request):
    if request.method == 'POST':
        training_name = request.POST.get('training')
        fac_name = request.session["username"]
        name = FacultyEnrollmentDB.objects.get(FacultyID=fac_name)
        # Filter job statuses based on the selected course
        status = TrainingDB.objects.filter(newsId__news_Title=training_name)

        context = {
            'training_name': training_name,
            'status': status,
            "name":name
        }
        return render(request, 'Viewstudentsname.html', context)
    else:
        courses = CourseDB.objects.all()
        return render(request, 'dashboard.html', {'data': courses})

# def delete_training(request, training_id):
#    if request.method == 'POST':
#         try:
#             # Retrieve the TrainingDB object to delete
#             training = TrainingDB.objects.get(pk=training_id)
#             # Delete the object
#             training.delete()
#             messages.success(request, 'Training status deleted successfully.')
#         except TrainingDB.DoesNotExist:
#             messages.error(request, 'Training status does not exist.')
#     return redirect('search_trainings')

# def delete_training(request, training_id):
#     training = get_object_or_404(TrainingDB, pk=training_id)
#             # Retrieve the TrainingDB object to delete
#             # training = TrainingDB.objects.get(pk=training_id)
#             # Delete the object
#     training.delete()
#         #     messages.success(request, 'Training status deleted successfully.')
#         # except TrainingDB.DoesNotExist:
#         #     messages.error(request, 'Training status does not exist.')
#     return redirect('search_trainings')