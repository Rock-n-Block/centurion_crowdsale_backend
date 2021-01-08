# Generated by Django 3.1.3 on 2021-01-08 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vouchers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=0, max_digits=78)),
                ('currency', models.CharField(max_length=10)),
                ('ducx_address', models.CharField(max_length=50)),
                ('tx_hash', models.CharField(max_length=100)),
                ('tx_error', models.TextField(default='')),
                ('status', models.CharField(default='WAITING FOR TRANSFER', max_length=50)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('voucher', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='vouchers.voucher')),
            ],
        ),
    ]
