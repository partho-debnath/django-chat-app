# Generated by Django 5.1.6 on 2025-03-01 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('chat', '0007_friendship_chat_friend_person__b3c1f9_idx_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='extenduser',
            options={},
        ),
        migrations.AddIndex(
            model_name='extenduser',
            index=models.Index(fields=['id'], name='chat_extend_id_4e220d_idx'),
        ),
        migrations.AddIndex(
            model_name='extenduser',
            index=models.Index(fields=['username'], name='chat_extend_usernam_9dc9d7_idx'),
        ),
    ]
