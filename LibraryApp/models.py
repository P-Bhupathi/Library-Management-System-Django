from django.db import models

# Create your models here.
class Admin_Cred(models.Model):
    admin_id = models.CharField(max_length=10, unique=True) 
    password = models.CharField(max_length=16)

    def __str__(self):
        return self.admin_id


class Books(models.Model):
    # Add the image field
    # book_image = models.ImageField(upload_to='images/',default='WIN_20221102_11_55_29_Pro.jpg')  # Specify the upload_to path as needed
    
    book_id=models.CharField(max_length=16,default="-")
    book_name=models.CharField(max_length=50,default="-")
    book_author=models.CharField(max_length=50,default="-")
    book_isbn=models.CharField(max_length=20,default="-")
    book_cost=models.IntegerField(default=0)
    book_status=models.CharField(max_length=12,default="available")
    # def _str_(self):
    #     return self.name

class BooksCount(models.Model):
    book_name=models.CharField(max_length=50,default="-")
    book_author=models.CharField(max_length=50,default="-")
    book_isbn=models.CharField(max_length=20,default="-")
    #book_cost=models.CharField(max_length=6)
    book_total_count = models.IntegerField(default=0)
    book_available = models.IntegerField(default=0)
    book_lended = models.IntegerField(default=0)
    
class Student_Cred(models.Model):
    student_id = models.CharField(max_length=10,default="-", unique=True)
    student_name = models.CharField(max_length=30,default="-")
    password = models.CharField(max_length=16,default="-")

class Assigned_Books(models.Model):
    student_id = models.CharField(max_length=10,default="-")
    student_name = models.CharField(max_length=30,default="-")
    book_id = models.CharField(max_length=16,default="-")
    book_name=models.CharField(max_length=50,default="-")
    issued_date = models.CharField(max_length=10,default="-")
    due_date = models.CharField(max_length=10,default="-")
    fine_cost = models.IntegerField(default=0)
    book_cost=models.IntegerField(default=0)

class Return_History(models.Model):
    student_id = models.CharField(max_length=10,default="-")
    student_name = models.CharField(max_length=30,default="-")
    book_id=models.CharField(max_length=16,default="-")
    book_name=models.CharField(max_length=50,default="-")
    book_isbn=models.CharField(max_length=20,default="-")
    issued_date = models.CharField(max_length=10,default="-")
    returned_date = models.CharField(max_length=10,default="-")
    book_status = models.CharField(max_length=8,default='-')
    fine_paid =  models.IntegerField(default=0)

class Book_Pdfs(models.Model):
    book_id=models.CharField(max_length=16,default="-")
    book_name=models.CharField(max_length=50,default="-")
    book_author=models.CharField(max_length=50,default="-")
    book_isbn=models.CharField(max_length=20,default="-")
    book_image = models.FileField(upload_to='images/',default='no_img.jpg')
    pdf_file = models.FileField(upload_to='pdfs/',default=None)
    
    def __str__(self):
        return self.book_name