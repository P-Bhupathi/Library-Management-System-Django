# Generated by Django 4.2.4 on 2023-09-02 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryApp', '0019_remove_books_book_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book_pdfs',
            name='book_image',
            field=models.FileField(default='media/images/no_img.jpg', upload_to='images/'),
        ),
    ]
