# Generated by Django 3.0.7 on 2020-08-11 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200810_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='scrapmodel',
            name='professional_code',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome do(a) beneficiário'),
        ),
        migrations.AddField(
            model_name='scrapmodel',
            name='professional_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome do(a) profissional'),
        ),
        migrations.AlterField(
            model_name='scrapmodel',
            name='birth',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Nascimento do(a) beneficiário(a)'),
        ),
        migrations.AlterField(
            model_name='scrapmodel',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True, verbose_name='CPF do(a) beneficiário(a)'),
        ),
        migrations.AlterField(
            model_name='scrapmodel',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome do(a) beneficiário(a)'),
        ),
    ]
