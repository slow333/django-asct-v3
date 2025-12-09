from django.db import migrations


def create_profiles(apps, schema_editor):
    Profile = apps.get_model('users', 'Profile')
    User = apps.get_model('auth', 'User')

    for user in User.objects.all():
        # Create a Profile only if it doesn't already exist
        if not Profile.objects.filter(user_id=user.id).exists():
            Profile.objects.create(user_id=user.id)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_profiles, noop),
    ]
