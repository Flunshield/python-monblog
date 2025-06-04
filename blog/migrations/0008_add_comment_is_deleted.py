# Generated manually for is_deleted field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_add_comment_moderation_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Supprimé'),
        ),
    ]
