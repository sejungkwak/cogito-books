# Generated by Django 3.2 on 2023-01-27 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(choices=[('product', 'Product Enquiries'), ('order', 'Order Enquiries'), ('loyalty', 'Loyalty Points Enquiries'), ('refund', 'Refund Enquiries'), ('website', 'Website Enquiries'), ('other', 'Other')], default='product', max_length=50)),
                ('name', models.CharField(max_length=254)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed')], default='open', max_length=50)),
            ],
            options={
                'ordering': ['status', 'date'],
            },
        ),
    ]
