# Generated by Django 4.2 on 2023-08-29 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0013_bookscount'),
    ]

    operations = [
        migrations.AddField(
            model_name='assigned_books',
            name='book_cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='assigned_books',
            name='book_name',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AddField(
            model_name='assigned_books',
            name='fine_cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='assigned_books',
            name='student_name',
            field=models.CharField(default='-', max_length=30),
        ),
        migrations.AddField(
            model_name='student_cred',
            name='student_name',
            field=models.CharField(default='-', max_length=30),
        ),
        migrations.AlterField(
            model_name='assigned_books',
            name='book_id',
            field=models.CharField(default='-', max_length=16),
        ),
        migrations.AlterField(
            model_name='assigned_books',
            name='due_date',
            field=models.CharField(default='-', max_length=10),
        ),
        migrations.AlterField(
            model_name='assigned_books',
            name='issued_date',
            field=models.CharField(default='-', max_length=10),
        ),
        migrations.AlterField(
            model_name='assigned_books',
            name='student_id',
            field=models.CharField(default='-', max_length=10),
        ),
        migrations.AlterField(
            model_name='books',
            name='book_author',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AlterField(
            model_name='books',
            name='book_cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='books',
            name='book_id',
            field=models.CharField(default='-', max_length=16),
        ),
        migrations.AlterField(
            model_name='books',
            name='book_isbn',
            field=models.CharField(default='-', max_length=20),
        ),
        migrations.AlterField(
            model_name='books',
            name='book_name',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AlterField(
            model_name='bookscount',
            name='book_author',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AlterField(
            model_name='bookscount',
            name='book_available',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bookscount',
            name='book_isbn',
            field=models.CharField(default='-', max_length=20),
        ),
        migrations.AlterField(
            model_name='bookscount',
            name='book_lended',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='bookscount',
            name='book_name',
            field=models.CharField(default='-', max_length=50),
        ),
        migrations.AlterField(
            model_name='bookscount',
            name='book_total_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='student_cred',
            name='password',
            field=models.CharField(default='-', max_length=16),
        ),
        migrations.AlterField(
            model_name='student_cred',
            name='student_id',
            field=models.CharField(default='-', max_length=10),
        ),
    ]