# Generated by Django 2.2.6 on 2019-10-14 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_feelinluckyguess_feelinluckysubmission_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameinstance',
            name='accepting_joins',
            field=models.BooleanField(default=True),
        ),
    ]
