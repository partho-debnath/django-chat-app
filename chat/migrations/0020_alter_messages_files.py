# Generated by Django 5.1.6 on 2025-03-09 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0019_alter_messages_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='files',
            field=models.ManyToManyField(blank=True, related_name='message', to='chat.file'),
        ),
    ]
