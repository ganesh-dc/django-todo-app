from django.db import migrations


def seed_categories(apps, schema_editor):
    Category = apps.get_model("todos", "Category")
    defaults = [
        ("Work", "#6366F1"),
        ("Personal", "#EC4899"),
        ("Shopping", "#F59E0B"),
        ("Health", "#14B8A6"),
    ]
    for name, color in defaults:
        Category.objects.get_or_create(name=name, defaults={"color": color})


def reverse(apps, schema_editor):
    Category = apps.get_model("todos", "Category")
    Category.objects.filter(
        name__in=["Work", "Personal", "Shopping", "Health"]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("todos", "0001_initial"),
    ]
    operations = [
        migrations.RunPython(seed_categories, reverse),
    ]
