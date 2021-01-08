# Generated by Django 3.1.3 on 2021-01-08 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuantumAccess',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.TextField(null=True)),
                ('token_type', models.CharField(max_length=20, null=True)),
                ('token_expires_at', models.BigIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='QuantumCharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('charge_id', models.IntegerField(unique=True)),
                ('status', models.CharField(max_length=50)),
                ('usd_amount', models.DecimalField(decimal_places=2, max_digits=100)),
                ('hash', models.CharField(max_length=100)),
                ('redirect_url', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=50)),
                ('last_update_datetime', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.centurionproject')),
            ],
        ),
    ]
