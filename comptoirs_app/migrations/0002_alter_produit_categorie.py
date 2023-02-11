# Generated by Django 4.1.5 on 2023-01-30 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comptoirs_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='categorie',
            field=models.ForeignKey(db_column='Categorie', on_delete=django.db.models.deletion.DO_NOTHING, related_name='produits', related_query_name='produit', to='comptoirs_app.categorie'),
        ),
    ]
