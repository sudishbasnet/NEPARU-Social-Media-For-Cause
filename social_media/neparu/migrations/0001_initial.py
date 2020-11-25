# Generated by Django 2.2.4 on 2020-03-16 12:01

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0026_auto_20190920_1449'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(max_length=30, verbose_name='last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('contact', models.IntegerField()),
                ('photo', models.ImageField(default='profile/avtar.jpg', upload_to='profile')),
                ('bio', models.CharField(blank=True, max_length=100)),
                ('account_type', models.CharField(default='public', max_length=15)),
                ('blood_group', models.CharField(blank=True, max_length=5)),
                ('follower', models.ManyToManyField(blank=True, related_name='user_follower', to=settings.AUTH_USER_MODEL)),
                ('following', models.ManyToManyField(blank=True, related_name='user_following', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=15)),
                ('price', models.IntegerField()),
                ('space_no', models.IntegerField()),
                ('description', models.TextField(max_length=1000)),
                ('location', models.CharField(max_length=125)),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(on_delete='CASCADE', related_name='rental_actor', to=settings.AUTH_USER_MODEL)),
                ('book_accepted', models.ManyToManyField(blank=True, related_name='book_accepted', to=settings.AUTH_USER_MODEL)),
                ('bookedby', models.ManyToManyField(blank=True, related_name='bookedby', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RentalPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='rental')),
                ('rental', models.ForeignKey(on_delete='CASCADE', related_name='rentalphoto', to='neparu.Rental')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(on_delete='CASCADE', to=settings.AUTH_USER_MODEL)),
                ('like', models.ManyToManyField(blank=True, related_name='like_posts', to=settings.AUTH_USER_MODEL)),
                ('report', models.ManyToManyField(blank=True, related_name='report_posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='photos')),
                ('post', models.ForeignKey(on_delete='CASCADE', related_name='my_photo', to='neparu.Post')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(blank=True, max_length=255)),
                ('action', models.CharField(max_length=25)),
                ('blood_group', models.CharField(blank=True, max_length=10)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('location', models.CharField(blank=True, max_length=125)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('actor', models.ForeignKey(default='Neparu', on_delete=django.db.models.deletion.CASCADE, related_name='notification_actor', to=settings.AUTH_USER_MODEL)),
                ('blood_available', models.ManyToManyField(blank=True, related_name='blood_responder', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(blank=True, null=True, on_delete='CASCADE', related_name='my_notification', to='neparu.Post')),
                ('receiver', models.ManyToManyField(related_name='notification_receiver', to=settings.AUTH_USER_MODEL)),
                ('rental', models.ForeignKey(blank=True, null=True, on_delete='CASCADE', related_name='my_rental', to='neparu.Rental')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank='true', null=True, upload_to='message')),
                ('message', models.CharField(blank='true', max_length=1000, null=True)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('actor', models.ForeignKey(on_delete='CASCADE', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete='CASCADE', related_name='my_comments', to='neparu.Post')),
            ],
        ),
    ]
