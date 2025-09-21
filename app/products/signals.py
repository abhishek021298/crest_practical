from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Product, ProductChangeLog
import logging

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Product)
def track_product_changes(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Product.objects.get(pk=instance.pk)
            changed_fields = {}
            
            for field in instance._meta.fields:
                field_name = field.name
                old_value = getattr(old_instance, field_name)
                new_value = getattr(instance, field_name)
                
                if old_value != new_value:
                    changed_fields[field_name] = {
                        'old': str(old_value),
                        'new': str(new_value)
                    }
            
            if changed_fields:
                instance._changed_fields = changed_fields
        except Product.DoesNotExist:
            pass

@receiver(post_save, sender=Product)
def log_product_save(sender, instance, created, **kwargs):
    action = 'created' if created else 'updated'
    changed_fields = getattr(instance, '_changed_fields', {})
    
    ProductChangeLog.objects.create(
        product=instance,
        action=action,
        changed_fields=changed_fields if not created else {'all_fields': 'Product created'},
    )
    logger.info(f"Product {action}: {instance.title}")

@receiver(post_delete, sender=Product)
def log_product_delete(sender, instance, **kwargs):
    logger.info(f"Product deleted: {instance.title}")