# Generated by Django 4.2.4 on 2023-09-01 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0016_return_history_fine_paid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book_Pdfs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_id', models.CharField(default='-', max_length=16)),
                ('book_name', models.CharField(default='-', max_length=50)),
                ('book_author', models.CharField(default='-', max_length=50)),
                ('book_isbn', models.CharField(default='-', max_length=20)),
                ('pdf_file', models.FileField(upload_to='pdfs/')),
            ],
        ),
    ]
