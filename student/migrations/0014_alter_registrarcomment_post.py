# Generated by Django 3.2.9 on 2022-04-26 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0013_auto_20220426_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrarcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.registrarpost'),
        ),
    ]
