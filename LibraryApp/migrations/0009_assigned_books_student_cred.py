# Generated by Django 4.2 on 2023-08-26 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0008_alter_books_book_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assigned_Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=10)),
                ('book_id', models.CharField(max_length=16)),
                ('issued_date', models.CharField(max_length=10)),
                ('due_date', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Student_Cred',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=10)),
                ('password', models.CharField(max_length=16)),
            ],
        ),
    ]
