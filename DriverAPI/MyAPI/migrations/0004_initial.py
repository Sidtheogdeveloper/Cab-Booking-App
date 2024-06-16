# Generated by Django 5.0.6 on 2024-06-09 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('MyAPI', '0003_delete_driver_delete_ride_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('driverID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=100, unique=True)),
                ('phone', models.CharField(default='', max_length=12, unique=True)),
                ('password', models.CharField(default='', max_length=50)),
                ('vehicle_number', models.CharField(default='', max_length=15)),
                ('latitude', models.FloatField(default=0)),
                ('longitude', models.FloatField(default=0)),
                ('vehicle_type', models.CharField(default='', max_length=20)),
                ('rating', models.FloatField(default=5)),
                ('available', models.BooleanField(default=False)),
                ('no_of_ratings', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('rideID', models.AutoField(primary_key=True, serialize=False)),
                ('userID', models.IntegerField(default=1)),
                ('driverID', models.IntegerField(default=1)),
                ('start_lat', models.FloatField(default=0)),
                ('end_lat', models.FloatField(default=0)),
                ('start_long', models.FloatField(default=0)),
                ('end_long', models.FloatField(default=0)),
                ('time', models.TimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('advanced_booking', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=0)),
                ('status', models.CharField(choices=[('ONGOING', 'Ongoing'), ('COMPLETED', 'Completed')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userID', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=100)),
                ('email', models.CharField(default='', max_length=100, unique=True)),
                ('phone', models.CharField(default='', max_length=12, unique=True)),
                ('password', models.CharField(default='', max_length=50)),
            ],
        ),
    ]