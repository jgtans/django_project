from django.db import migrations


def create_groups(apps, schema_editor):
    group = apps.get_model("auth", "Group")
    group.objects.get_or_create(name="watchers")
    group.objects.get_or_create(name="admins")


class Migration(migrations.Migration):
    dependencies = [("employees", "0008_alter_employeephoto_employee")]

    operations = [migrations.RunPython(create_groups, migrations.RunPython.noop)]
