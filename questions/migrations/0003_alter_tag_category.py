# Generated by Django 5.0.4 on 2024-04-30 03:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0002_question_slug_tag_question_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='questions.category'),
        ),
    ]
