# Generated by Django 5.0.2 on 2024-03-17 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0006_myuser_fullname_alter_myuser_identity_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(null=True),
        ),
    ]
