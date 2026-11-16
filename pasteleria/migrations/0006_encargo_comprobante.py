from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [('pasteleria', '0005_encargo_fecha_retiro')]

    operations = [
        migrations.AddField(
            model_name='encargos',
            name='fecha_hora',
            field=models.DateTimeField(null=True, editable=False),
        ),
        migrations.AlterField(
            model_name='encargos',
            name='fecha_hora',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, editable=False),
        ),
        migrations.AddField(
            model_name='encargos',
            name='total',
            field=models.IntegerField(null=True, editable=False),
        ),
    ]
