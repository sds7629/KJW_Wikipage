# Generated by Django 4.2.7 on 2023-11-30 12:32

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(error_messages={'required': ' 제목을 입력해주세요.'}, max_length=50)),
                ('payload', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='FeedRelWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word_list', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, size=None)),
            ],
        ),
        migrations.CreateModel(
            name='PayloadWord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
                ('count', models.BigIntegerField(default=0)),
                ('percent', models.FloatField(null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
            ],
            options={
                'default_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='RelationFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similar', models.FloatField(verbose_name=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('from_feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_from_feed', to='feeds.feed')),
                ('sim_feed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rel_sim_feed', to='feeds.feed')),
            ],
        ),
        migrations.AddField(
            model_name='feed',
            name='rel_feed',
            field=models.ManyToManyField(blank=True, related_name='+', through='feeds.RelationFeed', to='feeds.feed'),
        ),
        migrations.AddField(
            model_name='feed',
            name='sim_word',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sim_feed', to='feeds.feedrelword'),
        ),
    ]
