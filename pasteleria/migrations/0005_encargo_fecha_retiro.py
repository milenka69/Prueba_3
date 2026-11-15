from django.db import migrations, models


def completar_fechas(apps, schema_editor):
    Encargos = apps.get_model('pasteleria', 'Encargos')
    Encargos.objects.using(schema_editor.connection.alias).update(
        fecharetiro_fecha=models.F('fechapedido')
    )


class Migration(migrations.Migration):
    dependencies = [('pasteleria', '0004_alter_producto_imagen')]

    operations = [
        migrations.AlterField(
            model_name='encargos', name='telefono',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='encargos', name='fecharetiro_fecha',
            field=models.DateField(null=True),
        ),
        migrations.RunPython(completar_fechas, migrations.RunPython.noop),
        migrations.RemoveField(model_name='encargos', name='fecharetiro'),
        migrations.RenameField(
            model_name='encargos', old_name='fecharetiro_fecha', new_name='fecharetiro',
        ),
        migrations.AlterField(
            model_name='encargos', name='fecharetiro', field=models.DateField(),
        ),
    ]
