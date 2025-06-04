# Generated manually for comment moderation fields

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='Approuvé'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='blog.comment', verbose_name='Commentaire parent'),
        ),
    ]
