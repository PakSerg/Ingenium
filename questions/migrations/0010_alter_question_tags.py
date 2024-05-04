# Generated by Django 5.0.4 on 2024-05-04 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_alter_question_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='questions', to='questions.tag'),
        ),
    ]
