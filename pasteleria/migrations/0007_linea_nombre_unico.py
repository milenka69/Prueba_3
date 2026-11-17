from django.db import migrations, models
from django.db.models.functions import Lower, Trim


class Migration(migrations.Migration):
    dependencies = [('pasteleria', '0006_encargo_comprobante')]

    operations = [
        migrations.AddConstraint(
            model_name='linea',
            constraint=models.UniqueConstraint(
                Lower(Trim('nombre')),
                name='linea_nombre_unico',
                violation_error_message='Ya existe una línea con este nombre.',
            ),
        ),
    ]
