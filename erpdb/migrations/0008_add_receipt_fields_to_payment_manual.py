from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('erpdb', '0007_payment_receipt_generated_payment_receipt_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='receipt_generated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='payment',
            name='receipt_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
