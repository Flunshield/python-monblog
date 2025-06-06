# Generated by Django 5.2.1 on 2025-06-03 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_article_auteur_user_comment_auteur_user_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='auteur_user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='auteur_user',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('lecteur', 'Lecteur'), ('journaliste', 'Journaliste'), ('admin', 'Admin')], default='lecteur', max_length=20),
        ),
    ]
