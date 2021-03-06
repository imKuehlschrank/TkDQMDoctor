# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-05 15:04
from __future__ import unicode_literals

from django.db import migrations

from categories.models import Category as NewCategory


# python manage.py makemigrations --empty --name migrate_old_categories example

def copy_old_categories_to_new_django_categories(apps, schema_editor):
    """
    Migrates the data from the old "Category", "Subcategory" and "SubSubCategory"
    model to the new Category model from the django-category package
    """
    Category = apps.get_model('certhelper', 'Category')
    SubCategory = apps.get_model('certhelper', 'SubCategory')
    SubSubCategory = apps.get_model('certhelper', 'SubSubCategory')
    RunInfo = apps.get_model('certhelper', 'RunInfo')
    print(" migrating old Categories")

    found_msg = "[FND] Duplicate Category {} with parent {} found. No need to create."
    created_msg = "[NEW] Created new Category {} with parent {}"
    duplicate_warning_msg = "!! [ERR] Warning! Multiple Categories with the name {} exist. Choosing the first one " \
                            "with parent {} "
    no_parent_warning_msg = "!! [ERR] {} {} has no Parent! Don't know what to do."

    def create_new_category(old_category, new_parent_category):
        try:
            new_cat = NewCategory.objects.get(name=old_category.name, parent=new_parent_category)
            print(found_msg.format(new_cat.name, new_cat.parent))
        except NewCategory.DoesNotExist:
            new_cat = NewCategory.objects.create(name=old_category.name, parent=new_parent_category)
            print(created_msg.format(new_cat.name, new_cat.parent))
        except NewCategory.MultipleObjectsReturned:
            new_cat = NewCategory.objects.filter(name=old_category.name, parent=new_parent_category)[1]
            print(duplicate_warning_msg.format(new_cat.name, new_cat.parent))
        return new_cat

    for cat in Category.objects.all():
        newcat = create_new_category(cat, None)
        for subcat in cat.subcategory_set.all():
            newsubcat = create_new_category(subcat, newcat)
            for subsubcat in subcat.subsubcategory_set.all():
                create_new_category(subsubcat, newsubcat)

    for cat in SubCategory.objects.filter(parent_category__name=None):
        print(no_parent_warning_msg.format(cat, cat.name))
    for cat in SubSubCategory.objects.filter(parent_category__name=None):
        print(no_parent_warning_msg.format(cat, cat.name))

    print("updating RunInfo objects...")

    for run in RunInfo.all_objects.all():
        try:
            # SubSubCategory
            if run.category and run.subcategory and run.subsubcategory:
                new_cat = NewCategory.objects.get(
                    name=run.subsubcategory.name,
                    parent=NewCategory.objects.get(
                        name=run.subcategory.name,
                        parent=NewCategory.objects.get(
                            name=run.category.name,
                            parent=None
                        )
                    )
                )
                print("[ADD] Adding {} to {}".format(new_cat, run))
                run.problem_categories.add(new_cat.id)
            # SubCategory
            elif run.category and run.subcategory:
                new_cat = NewCategory.objects.get(
                    name=run.subcategory.name,
                    parent=NewCategory.objects.get(
                        name=run.category.name,
                        parent=None
                    )
                )
                print("[ADD] Adding {} to {}".format(new_cat, run))
                run.problem_categories.add(new_cat.id)
            # Category
            elif run.category and not run.subsubcategory:
                new_cat = NewCategory.objects.get(
                    name=run.category.name,
                    parent=None
                )
                print("[ADD] Adding {} to {}".format(new_cat, run))
                run.problem_categories.add(new_cat.id)

            # No Category set
            elif not run.category and not run.subcategory and not run.subsubcategory:
                # All Good.
                pass
            # Inconsistent Categories
            else:
                print("!! [ERR] Inconsistency !! RunInfo {} Category {} SubCategory {} SubSubCategory {}".format(
                    run, run.category, run.subcategory, run.subsubcategory))
        # Should never ever happen
        except NewCategory.DoesNotExist:
            print("!! [ERR] DoesNotExist !! RunInfo {} Category {} SubCategory {} SubSubCategory {}".format(
                run, run.category, run.subcategory, run.subsubcategory))


class Migration(migrations.Migration):
    dependencies = [
        ('certhelper', '0011_auto_20180705_1515'),
    ]

    operations = [
        migrations.RunPython(copy_old_categories_to_new_django_categories),
    ]
