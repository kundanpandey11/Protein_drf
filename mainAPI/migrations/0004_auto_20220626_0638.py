# Generated by Django 3.2.13 on 2022-06-26 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainAPI', '0003_auto_20220626_0120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pfam',
            name='domains',
        ),
        migrations.AddField(
            model_name='pfam',
            name='domains',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ffam', to='mainAPI.domains'),
        ),
    ]
