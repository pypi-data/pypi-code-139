# Generated by Django 4.0.4 on 2022-05-17 08:11

from django.db import migrations

from weblate.utils.hash import calculate_hash


def fix_convert_context(apps, schema_editor):
    Translation = apps.get_model("trans", "Translation")
    Unit = apps.get_model("trans", "Unit")
    translations = Translation.objects.using(schema_editor.connection.alias).filter(
        component__file_format__in=(
            "html",
            "idml",
            "rc",
            "txt",
            "dokuwiki",
            "mediawiki",
        )
    )
    for translation in translations:
        hashes = set()
        duplicate_hashes = set()
        units = translation.unit_set.all()
        for unit in units:
            unit.tmp_id_hash = calculate_hash(unit.source, "")
            unit.location = unit.context
            if unit.tmp_id_hash in hashes:
                duplicate_hashes.add(unit.tmp_id_hash)
            hashes.add(unit.tmp_id_hash)

        for unit in units:
            if unit.tmp_id_hash in duplicate_hashes:
                unit.id_hash = calculate_hash(unit.source, unit.context)
            else:
                unit.id_hash = unit.tmp_id_hash
                unit.context = ""

        Unit.objects.using(schema_editor.connection.alias).bulk_update(
            units, ["location", "context", "id_hash"]
        )


class Migration(migrations.Migration):

    dependencies = [
        ("trans", "0149_component_pull_message"),
    ]

    operations = [migrations.RunPython(fix_convert_context, elidable=True)]
