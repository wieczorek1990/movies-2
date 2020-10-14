# Generated by Django 3.1.2 on 2020-10-14 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_body', models.TextField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.movie')),
            ],
        ),
    ]