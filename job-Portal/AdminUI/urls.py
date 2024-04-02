from django.urls import path
from AdminUI import views

urlpatterns = [
    path('admin_indexpage/', views.admin_indexpage, name="admin_indexpage"),
    path('add_dept/', views.add_dept, name="add_dept"),
    path('submit_dept/', views.submit_dept, name="submit_dept"),
    path('view_dept/', views.view_dept, name="view_dept"),
    path('edit_dept/<int:dataid>/', views.edit_dept, name="edit_dept"),
    path('update_dept/<int:dataid>/', views.update_dept, name="update_dept"),
    path('delete_dept/<int:dataid>/', views.delete_dept, name="delete_dept"),
    path('add_course/', views.add_course, name="add_course"),
    path('submit_course/', views.submit_course, name="submit_course"),
    path('view_course/', views.view_course, name="view_course"),
    path('edit_course/<int:dataid>/', views.edit_course, name="edit_course"),
    path('update_course/<int:dataid>/', views.update_course, name="update_course"),
    path('delete_course/<int:dataid>/', views.delete_course, name="delete_course"),
    path('add_student/', views.add_student, name="add_student"),
    path('add_student2/', views.add_student2, name="add_student2"),
    path('submit_student/', views.submit_student, name="submit_student"),
    path('submit_student2/', views.submit_student_from_excel, name="submit_student2"),
    path('view_students/', views.view_students, name="view_students"),
    path('search_students/', views.search_students, name="search_students"),
    path('view_single_student/<int:dataid>/', views.view_single_student, name="view_single_student"),
    path('update_student/<int:dataid>/', views.update_student, name="update_student"),
    path('delete_student/<int:dataid>/', views.delete_student, name="delete_student"),
    path('add_faculty/', views.add_faculty, name="add_faculty"),
    path('submit_faculty/', views.submit_faculty, name="submit_faculty"),
    path('view_faculties/', views.view_faculties, name="view_faculties"),
    path('search_faculties/', views.search_faculties, name="search_faculties"),
    path('view_single_faculty/<int:dataid>/', views.view_single_faculty, name="view_single_faculty"),
    path('admin_login/', views.admin_login, name="admin_login"),
    path('admin_signin/', views.admin_signin, name="admin_signin"),

    path('add_job/', views.add_job, name="add_job"),
    path('job_save/', views.job_save, name="job_save"),
    path('view_jobs/', views.view_jobs, name="view_jobs"),
    path('job_delete/<int:data_id>/', views.job_delete, name="job_delete"),
    path('view_job_single/<int:data_id>/', views.view_job_single, name="view_job_single"),

    path('update_job/<int:job_id>/', views.update_job, name="update_job"),
    path('job_applications/<int:job_id>/', views.job_applications, name="job_applications"),
    path('resume_download/<int:job_id>/<int:stud_id>/', views.resume_download, name="resume_download"),
    path('application_single/<int:dataid>/', views.application_single, name="application_single"),

    path('add_news/', views.add_news, name="add_news"),
    path('news_save/', views.news_save, name="news_save"),
    path('news_view/', views.news_view, name="news_view"),
    path('add_news2/', views.add_news2, name="add_news2"),
    path('news_delete/<int:data_id>/', views.news_delete, name="news_delete"),

    path('add_news2/', views.add_news2, name="add_news2"),
    path('news_save2/', views.news_save2, name="news_save2"),
    path('news_view2/', views.news_view2, name="news_view2"),
    path('news_delete2/<int:data_id>/', views.news_delete2, name="news_delete2"),

    path('placed/',views.placed,name="placed"),
    path('add_placed/', views.add_placed, name="add_placed"),
    path('display_placed/', views.display_placed,name="display_placed"),
    path('placed_delete/<int:data_id>/', views.placed_delete,name="placed_delete"),

    path('add_marquee/', views.add_marquee, name='add_marquee'),
    path('marquee_list/', views.marquee_list, name='marquee_list'),
    path('delete/<int:marquee_id>/', views.delete_marquee, name='delete_marquee'),
    path('job_details/', views.job_details, name='job_details'),
    path('statussearch/', views.statussearch, name='statussearch'),
    path('search_studentstatus/', views.search_studentstatus, name="search_studentstatus"),
    path('delete-status/<int:status_id>/', views.delete_status, name='delete_status'),
    path('search_trainings/', views.search_trainings, name="search_trainings"),


]


# path('job_details/<str:data>/', views.job_details, name='job_details'),