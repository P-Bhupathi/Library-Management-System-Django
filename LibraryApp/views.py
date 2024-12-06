from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
import datetime
from django.db.models import Q
from django.http import FileResponse,Http404
from django.shortcuts import get_object_or_404
import os
# from django.db import connection

# def getBorrowers():   
#     query = """
#         SELECT
#             t2.student_id,
#             t1.book_id,
#             t1.book_name,
#             t2.issued_date,
#             t2.due_date
#         FROM
#             Books AS t1
#         INNER JOIN
#             Assigned_Books AS t2 ON t1.book_id = t2.book_id
#     """
#     with connection.cursor() as cursor:
#         cursor.execute(query)
#         result = cursor.fetchall()
#     return result
# print(type(getBorrowers()))
def getHistory():
    hd = Return_History.objects.all()
    return hd
def eBookCount():
    cnt = Book_Pdfs.objects.all().count()
    return cnt
def overduesBooks():
    format_string = "%Y-%m-%d"
    duebooks = Assigned_Books.objects.all()
    overduebooks_count = 0
    for i in duebooks:
        if str(datetime.datetime.now().date())>i.due_date:
            overduebooks_count += 1
            duedate = datetime.datetime.strptime(i.due_date, format_string)
            i.fine_cost = 1*((datetime.datetime.now().date()) - duedate.date()).days
            i.save()
    duebooks1 = Assigned_Books.objects.raw("SELECT * from libraryapp_assigned_books WHERE fine_cost>0")
    return [duebooks1,overduebooks_count]


def admin_student(request):
    return render(request,'log.html')

def admin_login(request):
    return render(request,'adlog.html')

def admin_logout(request):
    request.session.flush()
    return render(request,'adlog.html',{'message':"Logged out..."})

def admin_new_register(request):
    return render(request,'adlog2.html')

def student_login(request):
    return render(request,'std.html')

def student_dashboard(request):
    return render(request,'student_dashboard.html')

def admin_valid(request):
    if request.method == 'POST':
        id_number = request.POST.get('id_number')
        password = request.POST.get('password')
        
        try:
            admin_cred = Admin_Cred.objects.get(admin_id=id_number)
            if admin_cred.password == password:
                request.session['adminid'] = request.POST.get('id_number')
                print(request.session['adminid'])
                request.session.modified=True
                #print("VALID:", request.session['adminid'])
                books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
                borrowers = Assigned_Books.objects.all()
                total_books = Books.objects.all()
                overduebooks=overduesBooks()
                return render(request, 'admin_main.html',{'books_data':books_data,'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
            else:
                return render(request, 'adlog.html', {'message': "Invalid password",'ebookscount':eBookCount()})
        except Admin_Cred.DoesNotExist:
            return render(request, 'adlog.html', {'message': "Invalid username",'ebookscount':eBookCount()})
            
    return render(request, 'adlog.html')


def all_books(request):
    all_books = Books.objects.all()
    context = {'books': all_books}
    return render(request, 'all_books.html', context)


def add_book(request):
    if request.method == 'POST' and 'adminid' in request.session:
        # Get form data
        book_id = request.POST.get('bookId')
        book_name = request.POST.get('bookName')
        # Other fields...
        book_author=request.POST.get('bookAuthor')
        # Get the uploaded image file
        #uploaded_image = request.FILES.get('bookImage')
        book_cost=request.POST.get('cost')
        book_isbn=request.POST.get('isbn')
        # Process the uploaded image
        #books_data = Books.objects.all().values('book_id','book_name','book_author')
        books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
        
        if Books.objects.filter(book_id=book_id).count():
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':'Already existed, BookID: '+str(book_id),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
        new_entry = Books(book_id=book_id,
                            book_name=book_name,
                            book_author=book_author,
                            book_isbn=book_isbn,
                            book_cost=book_cost)
        new_entry.save()
        if BooksCount.objects.filter(book_isbn=book_isbn).count():
            count_data = BooksCount.objects.get(book_isbn=book_isbn)

            count_data.book_total_count +=1
            count_data.book_available +=1
            count_data.save()
            books_data1 = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data1,'status':'Successfully added, BookID: '+str(book_id),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
        else:
            books_count_entry = BooksCount(
                            book_name=book_name,
                            book_author=book_author,
                            book_isbn=book_isbn,
                            book_total_count=1,
                            book_available=1,
                            book_lended=0,
            )
            books_count_entry.save()
            books_data1 = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data1,'status':'Successfully added, BookID: '+str(book_id),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
        #print(book_id,book_name)
        
    else:
        return render(request,'adlog.html',{'message':"You have logged out previously..."})
    #return render(request, 'admin_main.html',{'books_data':books_data,'status':'Successfully added, BookID: '+str(book_id),'ebookscount':eBookCount()})  # Render the form initially

def delete_book(request):
    if request.method == 'POST' and 'adminid' in request.session:
        book_id=request.POST.get('bookId')
        book_isbn=request.POST.get('isbn_del')
        #print(book_id)
        books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
        if book_id=='' and book_isbn =='':
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':'Enter bookID or ISBN number...','totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
        if book_id !='':

            try:
                book_obj = Books.objects.get(book_id=request.POST.get('bookId'))
                if book_obj.book_status=='available':
                    isbn_to_decrease = book_obj.book_isbn
                    book_count_data = BooksCount.objects.get(book_isbn=isbn_to_decrease)
                    if book_count_data.book_total_count==1:
                        book_count_data.delete()
                        book_obj.delete()
                        books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
                        total_books = Books.objects.all()
                        borrowers = Assigned_Books.objects.all()
                        overduebooks=overduesBooks()
                        return render(request, 'admin_main.html',{'books_data':books_data,'status':'Deleted book with bookID: '+str(request.POST.get('bookId')),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
                    
                    else:
                        book_count_data.book_total_count -= 1
                        book_count_data.book_available -= 1
                        book_count_data.save()
                        book_obj.delete()
                        books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
                        total_books = Books.objects.all()
                        borrowers = Assigned_Books.objects.all()
                        overduebooks=overduesBooks()
                        return render(request, 'admin_main.html',{'books_data':books_data,'status':'Deleted book with bookID: '+str(request.POST.get('bookId')),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
                elif book_obj.book_status == 'unavailable':
                    books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
                    total_books = Books.objects.all()
                    borrowers = Assigned_Books.objects.all()
                    overduebooks=overduesBooks()
                    return render(request, 'admin_main.html',{'books_data':books_data,'status':'Book already assigned, Unavaialable to delete, BookID: '+str(request.POST.get('bookId')),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
                #return render(request, 'admin_main.html',{'books_data':books_data,'status':'Deleted book with bookID: '+book_obj.book_id,'ebookscount':eBookCount()})
            except Books.DoesNotExist:
                books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
                total_books = Books.objects.all()
                borrowers = Assigned_Books.objects.all()
                overduebooks=overduesBooks()
                return render(request, 'admin_main.html',{'books_data':books_data,'status':('BookID: '+book_id+' not existed..!'),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
                #return HttpResponse("<h3>not existed </h3>")
        elif book_isbn !='':
            try:
                book_obj = Books.objects.filter(book_isbn=request.POST.get('isbn_del'))
                #book_obj = Books.objects.filter(Q(book_isbn=request.POST.get('isbn_del')) & Q(book_status='available'))
                cnt=str(book_obj.count())
                isbn_to_decrease = request.POST.get('isbn_del')
                book_count_data = BooksCount.objects.get(book_isbn=isbn_to_decrease)
                if int(cnt) > 0 and book_count_data.book_total_count == book_count_data.book_available:

                    book_count_data = BooksCount.objects.get(book_isbn=isbn_to_decrease)
                    book_count_data.delete()
                    book_obj.delete()
                    # book_count_data.book_total_count -= 1
                    # book_count_data.book_available -= 1
                    # book_obj.delete()
                    books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
                    total_books = Books.objects.all()
                    borrowers = Assigned_Books.objects.all()
                    overduebooks=overduesBooks()
                    return render(request, 'admin_main.html',{'books_data':books_data,'status':'Deleted all books with ISBN: '+request.POST.get('isbn_del'),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
                elif int(cnt) > 0 and book_count_data.book_total_count != book_count_data.book_available:
                    books_to_remove_from_total = book_count_data.book_available
                    book_count_data.book_available=0
                    total_isbn_book = book_count_data.book_total_count
                    book_count_data.book_total_count -= books_to_remove_from_total
                    book_count_data.save()
                    book_obj = Books.objects.filter(Q(book_isbn=request.POST.get('isbn_del')) & Q(book_status='available'))
                    book_obj.delete()
                    ######
                    books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
                    total_books = Books.objects.all()
                    borrowers = Assigned_Books.objects.all()
                    overduebooks=overduesBooks()
                    return render(request, 'admin_main.html',{'books_data':books_data,'status':str(books_to_remove_from_total)+" of "+str(total_isbn_book)+" books removed with ISBN: "+request.POST.get('isbn_del'),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})

                else:
                    books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
                    total_books = Books.objects.all()
                    borrowers = Assigned_Books.objects.all()
                    overduebooks=overduesBooks()
                    
                    return render(request, 'admin_main.html',{'books_data':books_data,'status':"Books doesn't exists with ISBN: "+request.POST.get('isbn_del'),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})  
            except Books.DoesNotExist:
                books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
                total_books = Books.objects.all()
                borrowers = Assigned_Books.objects.all()
                overduebooks=overduesBooks()
                return render(request, 'admin_main.html',{'books_data':books_data,'status':"Books doesn't exists with ISBN: "+request.POST.get('isbn_del'),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
    
    else:
        return render(request,'adlog.html',{'message':"You have logged out previously..."})
    # return render(request, 'adlog.html')

def assign_book(request):
    if request.method == 'POST' and 'adminid' in request.session:
        student_id = request.POST.get('studentId')
        book_id = request.POST.get('bookId')
        existed_student_or_not = Student_Cred.objects.filter(student_id=student_id).count()
        count_of_book1 = Books.objects.filter(book_id=book_id).count()
        books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
        books_count_data_object =  BooksCount.objects.all()
        if count_of_book1 == 0 and existed_student_or_not == 1:
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':"Books doesn't exists with ID: "+book_id,'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
            #return HttpResponse("Book doesn't exist.....")
        if count_of_book1 == 0 and existed_student_or_not == 0:
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':"Invalid student ID or Book doesn't exist...",'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
        status_obj = Books.objects.get(book_id=book_id)
        if count_of_book1 == 1 and existed_student_or_not == 0 and status_obj.book_status == "available":
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':"Invalid student ID: "+student_id,'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
        if count_of_book1==1 and status_obj.book_status == "available" and existed_student_or_not==1:
            asignBookObj = Assigned_Books(

                     student_id=student_id,
                     student_name=Student_Cred.objects.get(student_id=student_id).student_name,
                     book_id = book_id,
                     book_name=Books.objects.get(book_id=book_id).book_name,
                     issued_date = str(datetime.datetime.now().date()),
                     due_date = str(datetime.datetime.now().date() + datetime.timedelta(days=15)),
                     book_cost = Books.objects.get(book_id=book_id).book_cost

            )
            asignBookObj.save()
            status_obj.book_status = "unavailable"
            status_obj.save()
            isbn = Books.objects.get(book_id=book_id).book_isbn
            books_count_data_object = BooksCount.objects.get(book_isbn=isbn)
            books_count_data_object.book_available -= 1
            books_count_data_object.book_lended += 1
            books_count_data_object.save()
            books_data1 = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data1,'status':"Assigned successfully, due date: "+ str(datetime.datetime.now().date() + datetime.timedelta(days=15)),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
            #return HttpResponse("Assigned successfully.....")
        elif status_obj.book_status == "unavailable" and existed_student_or_not==1:
            books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':"Book Already assigned...",'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
            #return HttpResponse("Book Already assigned....")
        elif status_obj.book_status == "unavailable" or existed_student_or_not==0 or count_of_book1==0:
            books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':"Invalid student ID or Book doesn't exist...",'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
            #return HttpResponse("Invalid student creds or Book doesn't exist...")
    else:
        return render(request,'adlog.html',{'message':"You have logged out previously..."})
def clone_book(request):
    if request.method == 'POST' and 'adminid' in request.session:
        print(request.session['adminid'])
        idtoadd = request.POST.get('bookID')
        isbnclone = request.POST.get('isbn_clone')
        #books_data_count = Books.objects.filter(book_isbn=isbnclone).count()
        if Books.objects.filter(book_isbn=isbnclone).count() and Books.objects.filter(book_id=idtoadd).count()==0:
            book_data = Books.objects.filter(book_isbn=isbnclone)
            for i in book_data:
                bd = i
                break
            # print(book_data)
            book_name = bd.book_name
            book_author = bd.book_author
            book_isbn = isbnclone
            book_cost = bd.book_cost
            newBook = Books(
                book_id=request.POST.get('bookID'),
                book_name=book_name,
                book_author=book_author,
                book_isbn = request.POST.get('isbn_clone'),
                book_cost=book_cost,
            )
            newBook.save()
            book_count_data = BooksCount.objects.get(book_isbn=isbnclone)
            book_count_data.book_total_count += 1
            book_count_data.book_available += 1
            book_count_data.save()
            books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':"Book successfully added with ID:"+str(idtoadd),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
        elif Books.objects.filter(book_id=idtoadd).count()>0:
            books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':"Book already existed with ID:"+str(idtoadd),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
        else:
            books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':"Book doesn't existed with ISBN: "+isbnclone,'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
    else:
        return render(request,'adlog.html',{'message':"You have logged out previously..."})        
#Return Book
def return_book(request):
    if request.method=="POST" and 'adminid' in request.session:
        bookId = request.POST.get('bookId')
        #assigned_books = Assigned_Books.objects.filter(book_id=bookId).count()
        if Assigned_Books.objects.filter(book_id=bookId).count():
            if Assigned_Books.objects.get(book_id=bookId).fine_cost == 0:
                assigned_books_data = Assigned_Books.objects.get(book_id=bookId)
                return_history=Return_History(student_id = assigned_books_data.student_id,
                                           student_name = assigned_books_data.student_name,
                                            book_id=assigned_books_data.book_id,
                                            book_name=assigned_books_data.book_name,
                                            issued_date =assigned_books_data.issued_date,
                                            returned_date =str(datetime.datetime.now().date()),
                                            book_isbn=Books.objects.get(book_id=bookId).book_isbn,
                                            book_status = 'returned',
                                            fine_paid = 0,
                )
                return_history.save()
                assigned_books_data.delete()
                books_data = Books.objects.get(book_id=bookId)
                books_data.book_status = 'available'
                books_data.save()
                bookISBN = Books.objects.get(book_id=bookId).book_isbn
                books_count_data = BooksCount.objects.get(book_isbn=bookISBN)
                books_count_data.book_available += 1
                books_count_data.book_lended -= 1
                books_count_data.save()
                #return data
                books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
                total_books = Books.objects.all()
                borrowers = Assigned_Books.objects.all()
                overduebooks=overduesBooks()
                return render(request, 'admin_main.html',{'books_data':books_data,'status':"Successfully returned BookID: "+bookId,'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})

            elif Assigned_Books.objects.get(book_id=bookId).fine_cost > 0:
                assigned_books_data = Assigned_Books.objects.get(book_id=bookId)
                return_history=Return_History(student_id = assigned_books_data.student_id,
                                           student_name = assigned_books_data.student_name,
                                            book_id=assigned_books_data.book_id,
                                            book_name=assigned_books_data.book_name,
                                            issued_date =assigned_books_data.issued_date,
                                            returned_date =str(datetime.datetime.now().date()),
                                            book_isbn=Books.objects.get(book_id=bookId).book_isbn,
                                            book_status = 'returned',
                                            fine_paid = Assigned_Books.objects.get(book_id=bookId).fine_cost,
                )
                return_history.save()
                assigned_books_data.delete()
                books_data = Books.objects.get(book_id=bookId)
                books_data.book_status = 'available'
                books_data.save()
                bookISBN = Books.objects.get(book_id=bookId).book_isbn
                books_count_data = BooksCount.objects.get(book_isbn=bookISBN)
                books_count_data.book_available += 1
                books_count_data.book_lended -= 1
                books_count_data.save()
                #return data
                books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
                total_books = Books.objects.all()
                borrowers = Assigned_Books.objects.all()
                overduebooks=overduesBooks()
                return render(request, 'admin_main.html',{'books_data':books_data,'status':"Successfully paid and returned BookID: "+bookId,'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
        else:
            books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':"Incorrect book ID",'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
    else:
        return render(request,'adlog.html',{'message':"You have logged out previously..."})

def lost_book_delete(request):
    if request.method=="POST" and 'adminid' in request.session:
        bookId = request.POST.get('bookId')
        #assigned_books = Assigned_Books.objects.filter(book_id=bookId).count()
        if Assigned_Books.objects.filter(book_id=bookId).count():
            if Assigned_Books.objects.get(book_id=bookId).fine_cost == 0:
                assigned_books_data = Assigned_Books.objects.get(book_id=bookId)
                return_history=Return_History(student_id = assigned_books_data.student_id,
                                           student_name = assigned_books_data.student_name,
                                            book_id=assigned_books_data.book_id,
                                            book_name=assigned_books_data.book_name,
                                            issued_date =assigned_books_data.issued_date,
                                            returned_date =str(datetime.datetime.now().date()),
                                            book_isbn=Books.objects.get(book_id=bookId).book_isbn,
                                            book_status = 'lost',
                                            fine_paid = Assigned_Books.objects.get(book_id=bookId).book_cost,
                )
                # delete_book_in_library = Books.objects.get(book_id=assigned_books_data.book_id)
                #delete_book_in_library.delete()
                return_history.save()
                assigned_books_data.delete()
                books_data = Books.objects.get(book_id=bookId)
                #books_data.book_status = 'available'
                #books_data.save()
                bookISBN = Books.objects.get(book_id=bookId).book_isbn
                books_count_data = BooksCount.objects.get(book_isbn=bookISBN)
                if books_count_data.book_total_count == 1:
                    books_count_data.delete()
                elif books_count_data.book_available == 0:
                    books_count_data.book_total_count -= 1
                    books_count_data.book_lended -= 1
                    books_count_data.save()
                else:
                    books_count_data.book_total_count -= 1
                    books_count_data.book_available -= 1
                    books_count_data.book_lended -= 1
                    books_count_data.save()
                books_data.delete()
                #return data
                books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
                total_books = Books.objects.all()
                borrowers = Assigned_Books.objects.all()
                overduebooks=overduesBooks()
                return render(request, 'admin_main.html',{'books_data':books_data,'status':"Successfully paid",'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})

            elif Assigned_Books.objects.get(book_id=bookId).fine_cost > 0:
                assigned_books_data = Assigned_Books.objects.get(book_id=bookId)
                return_history=Return_History(student_id = assigned_books_data.student_id,
                                           student_name = assigned_books_data.student_name,
                                            book_id=assigned_books_data.book_id,
                                            book_name=assigned_books_data.book_name,
                                            issued_date =assigned_books_data.issued_date,
                                            returned_date =str(datetime.datetime.now().date()),
                                            book_isbn=Books.objects.get(book_id=bookId).book_isbn,
                                            book_status = 'lost',
                                            fine_paid = Assigned_Books.objects.get(book_id=bookId).book_cost + Assigned_Books.objects.get(book_id=bookId).fine_cost,
                )
                # delete_book_in_library = Books.objects.get(book_id=assigned_books_data.book_id)
                #delete_book_in_library.delete()
                return_history.save()
                assigned_books_data.delete()
                books_data = Books.objects.get(book_id=bookId)
                #books_data.book_status = 'available'
                #books_data.save()
                bookISBN = Books.objects.get(book_id=bookId).book_isbn
                books_count_data = BooksCount.objects.get(book_isbn=bookISBN)
                if books_count_data.book_total_count == 1:
                    books_count_data.delete()
                else:
                    books_count_data.book_total_count -= 1
                    books_count_data.book_available -= 1
                    books_count_data.book_lended -= 1
                    books_count_data.save()
                books_data.delete()
                #return data
                books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
                total_books = Books.objects.all()
                borrowers = Assigned_Books.objects.all()
                overduebooks=overduesBooks()
                return render(request, 'admin_main.html',{'books_data':books_data,'status':"Successfully paid",'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
        else:
            books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':"Incorrect book ID",'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
    else:
        return render(request,'adlog.html',{'message':"You have logged out previously..."})

def add_student(request):
    if request.method=="POST" and 'adminid' in request.session:
        if Student_Cred.objects.filter(student_id=request.POST.get("studentid")).count():
            books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':"Student already exists..",'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
        else:
            new_student = Student_Cred(
                student_id=request.POST.get("studentid"),
                student_name=request.POST.get("studentname"),
                password=request.POST.get("password1"),
            )
            new_student.save()
            books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':"Successfully registered with ID: "+str(request.POST.get("studentid")),'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
    else:
        return render(request,'adlog.html',{'message':"You have logged out previously..."})

def add_ebook(request):
    if request.method=="POST" and 'adminid' in request.session:
        if Book_Pdfs.objects.filter(book_isbn=request.POST.get('ebookisbn')).count()==0:
            book_name = request.POST.get('ebookname')
            book_isbn= request.POST.get('ebookisbn')
            book_img = request.FILES.get('imagefileupload')
            # print(type(book_img))
            book_pdf = request.FILES.get('fileupload')
            e_book=Book_Pdfs(
                book_name=book_name,
                book_isbn=book_isbn,
                pdf_file=book_pdf,
                book_image=book_img,
            )
            e_book.save()
            books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':"Uploaded successfully...",'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
        else:
            books_data = BooksCount.objects.all().values('book_name','book_author','book_isbn','book_total_count','book_available','book_lended')
            total_books = Books.objects.all()
            borrowers = Assigned_Books.objects.all()
            overduebooks=overduesBooks()
            return render(request, 'admin_main.html',{'books_data':books_data,'status':"e-Book already exists...",'totalbooks':total_books,'totalbooksondashboard':total_books.count(),"borrowestable":borrowers,"borrowerscount":borrowers.count(),'overduebookstable':overduebooks[0],'overduebookscount':overduebooks[1],'historytable':getHistory(),'ebookscount':eBookCount(),'adminid':request.session['adminid']})
    else:
        return render(request,'adlog.html',{'message':"You have logged out previously..."})   


# def delete_ebook(isbn):
#     if Book_Pdfs.objects.filter(book_isbn=isbn).count():
#         ebook = Book_Pdfs.objects.get(book_isbn=isbn)
#         if ebook.book_image.name == 'images/no_img.jpg':
#             os.remove(ebook.pdf_file.path)
#             ebook.delete()
#         else:
#             os.remove(ebook.pdf_file.path)
#             os.remove(ebook.book_image.path)
#             ebook.delete()
#     else:
#         print("No such book exists")



# STUDENT VIEWS

def books_borrowed(request,student_id):
    if_cond=Assigned_Books.objects.filter(student_id=student_id).count()
    if (if_cond):
        borrowed=Assigned_Books.objects.filter(student_id=student_id)
        
        return render(request,"books_bur.html",{'library_records':borrowed})
    else:
        return render(request,"books_bur.html",{'message':"No books borrowed"})

def books_returned(request,student_id):
    if_cond=Return_History.objects.filter(student_id=student_id).count()
    if if_cond:
        returned=Return_History.objects.filter(student_id=student_id)
        return render(request,"books_ret.html",{'library_records':returned})
    else:
        return render(request,"books_ret.html",{'message':"No books returned"})


def books_overdue(request,student_id):
    if_cond=Assigned_Books.objects.filter(Q(student_id=student_id) & Q(fine_cost__gt=0)).count()
    if if_cond:
        overdue=Assigned_Books.objects.filter(Q(student_id=student_id) & Q(fine_cost__gt=0))
        return render(request,"books_overdue.html",{'library_records':overdue})
    else:
        return render(request,"books_overdue.html",{'message':"No books overdue"})
    
def e_books(request):
    library_records=Book_Pdfs.objects.all()
    
    
    return render(request,"ebooks.html",{'library_records':library_records})

def download_book(request, book_id):
    book = get_object_or_404(Book_Pdfs, book_id=book_id)
    file_path = book.pdf_file.path
    # print(book_id)

    try:
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{book.pdf_file.name}"'
        return response
    except FileNotFoundError:
        raise Http404

def student_valid(request):
    if request.method == 'POST':
        stud_id=request.POST.get('student_id')
        stud_pass=request.POST.get('student_pass')
        
        try:
            student_cred = Student_Cred.objects.get(student_id=stud_id)
            if student_cred.password == stud_pass:
                borrowed_count=Assigned_Books.objects.filter(student_id=stud_id).count()
                returned_count=Return_History.objects.filter(student_id=stud_id).count()
                overdue_count=Assigned_Books.objects.filter(Q(student_id=stud_id) & Q(fine_cost__gt=0)).count()
                ebooks_count=Book_Pdfs.objects.all().count()

                
                return render(request, 'stumain.html',{'student_id':stud_id,'borrowed_count':borrowed_count,'returned_count':returned_count,'overdue_count':overdue_count,'ebooks_count':ebooks_count})
            else:
                return render(request, 'std.html', {'message': "Invalid password"})
        except Student_Cred.DoesNotExist:
            return render(request, 'std.html', {'message': "Invalid username"})
            
    return render(request, 'adlog.html')

def student_home(request):
    return render(request,'stumain.html')