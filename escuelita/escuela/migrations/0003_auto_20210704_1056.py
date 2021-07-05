# Generated by Django 3.2.5 on 2021-07-04 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escuela', '0002_auto_20210703_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='grade',
            field=models.IntegerField(choices=[(1, 'Primero'), (2, 'Segundo'), (3, 'Tercero'), (4, 'Cuarto'), (5, 'Quinto'), (6, 'Sexto')], null=True),
        ),
    ]
