# Generated by Django 2.0.8 on 2018-10-23 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("campaigns", "0028_campaignevent_start_mode")]

    operations = [
        migrations.AddField(
            model_name="eventfire",
            name="fired_result",
            field=models.CharField(
                blank=True,
                choices=[("F", "Fired"), ("S", "Skipped")],
                help_text="Whether the event is fired or skipped, null if not yet fired",
                max_length=1,
                null=True,
            ),
        )
    ]
