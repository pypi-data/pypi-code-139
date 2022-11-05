# Generated by Django 3.1.7 on 2021-03-19 14:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("screenshots", "0004_auto_20201002_1423"),
        ("trans", "0128_fix_pending_read_only"),
    ]

    operations = [
        migrations.AddField(
            model_name="change",
            name="screenshot",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="screenshots.screenshot",
            ),
        ),
        migrations.AlterField(
            model_name="change",
            name="action",
            field=models.IntegerField(
                choices=[
                    (0, "Resource update"),
                    (1, "Translation completed"),
                    (2, "Translation changed"),
                    (5, "New translation"),
                    (3, "Comment added"),
                    (4, "Suggestion added"),
                    (6, "Automatic translation"),
                    (7, "Suggestion accepted"),
                    (8, "Translation reverted"),
                    (9, "Translation uploaded"),
                    (13, "New source string"),
                    (14, "Component locked"),
                    (15, "Component unlocked"),
                    (16, "Found duplicated string"),
                    (17, "Committed changes"),
                    (18, "Pushed changes"),
                    (19, "Reset repository"),
                    (20, "Merged repository"),
                    (21, "Rebased repository"),
                    (22, "Failed merge on repository"),
                    (23, "Failed rebase on repository"),
                    (28, "Failed push on repository"),
                    (24, "Parse error"),
                    (25, "Removed translation"),
                    (26, "Suggestion removed"),
                    (27, "Search and replace"),
                    (29, "Suggestion removed during cleanup"),
                    (30, "Source string changed"),
                    (31, "New string added"),
                    (32, "Bulk status change"),
                    (33, "Changed visibility"),
                    (34, "Added user"),
                    (35, "Removed user"),
                    (36, "Translation approved"),
                    (37, "Marked for edit"),
                    (38, "Removed component"),
                    (39, "Removed project"),
                    (40, "Found duplicated language"),
                    (41, "Renamed project"),
                    (42, "Renamed component"),
                    (43, "Moved component"),
                    (44, "New string to translate"),
                    (45, "New contributor"),
                    (46, "New announcement"),
                    (47, "New alert"),
                    (48, "Added new language"),
                    (49, "Requested new language"),
                    (50, "Created project"),
                    (51, "Created component"),
                    (52, "Invited user"),
                    (53, "Received repository notification"),
                    (54, "Replaced file by upload"),
                    (55, "License changed"),
                    (56, "Contributor agreement changed"),
                    (57, "Screnshot added"),
                    (58, "Screnshot uploaded"),
                ],
                db_index=True,
                default=2,
            ),
        ),
    ]
