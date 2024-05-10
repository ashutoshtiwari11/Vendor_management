from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import PurchaseOrder, Vendor, HistoricalPerformance

# On-Time Delivery Rate
@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_delivered_pos = completed_pos.filter(delivery_date__lte=timezone.now())
        on_time_delivery_rate = (on_time_delivered_pos.count() / completed_pos.count()) * 100
        vendor.on_time_delivery_rate = on_time_delivery_rate
        vendor.save()

# Quality Rating Average
@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, created, **kwargs):
    if instance.quality_rating is not None:
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        quality_ratings = completed_pos.exclude(quality_rating=None).values_list('quality_rating', flat=True)
        quality_rating_avg = sum(quality_ratings) / len(quality_ratings)
        vendor.quality_rating_avg = quality_rating_avg
        vendor.save()

# Average Response Time
@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, created, **kwargs):
    if instance.acknowledgment_date is not None:
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', acknowledgment_date__isnull=False)
        response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_pos]
        average_response_time = sum(response_times) / len(response_times)
        vendor.average_response_time = average_response_time
        vendor.save()

# Fulfilment Rate
@receiver(post_save, sender=PurchaseOrder)
@receiver(pre_delete, sender=PurchaseOrder)
def update_fulfilment_rate(sender, instance, **kwargs):
    vendor = instance.vendor
    total_pos = PurchaseOrder.objects.filter(vendor=vendor)
    fulfilled_pos = total_pos.filter(status='completed')
    fulfilment_rate = (fulfilled_pos.count() / total_pos.count()) * 100
    vendor.fulfillment_rate = fulfilment_rate
    vendor.save()


#API ENDPOINT IMPLEMENTATIONS

