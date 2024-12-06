# Generated by Django 4.2 on 2023-08-31 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0014_assigned_books_book_cost_assigned_books_book_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Return_History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(default='-', max_length=10)),
                ('student_name', models.CharField(default='-', max_length=30)),
                ('book_id', models.CharField(default='-', max_length=16)),
                ('book_name', models.CharField(default='-', max_length=50)),
                ('book_isbn', models.CharField(default='-', max_length=20)),
                ('issued_date', models.CharField(default='-', max_length=10)),
                ('returned_date', models.CharField(default='-', max_length=10)),
                ('book_status', models.CharField(default='-', max_length=8)),
            ],
        ),
    ]
