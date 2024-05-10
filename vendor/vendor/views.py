from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor, PurchaseOrder

# Vendor Profile Management
@api_view(['POST'])
def create_vendor(request):
    data = request.data
    try:
        vendor = Vendor.objects.create(
            name=data['name'],
            contact_details=data['contact_details'],
            address=data['address'],
            vendor_code=data['vendor_code']
        )
        return Response({'id': vendor.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_vendors(request):
    vendors = Vendor.objects.all()
    return Response([{'id': vendor.id, 'name': vendor.name} for vendor in vendors])

@api_view(['GET', 'PUT', 'DELETE'])
def vendor_details(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    if request.method == 'GET':
        return Response({
            'name': vendor.name,
            'contact_details': vendor.contact_details,
            'address': vendor.address,
            'vendor_code': vendor.vendor_code
        })
    elif request.method == 'PUT':
        data = request.data
        vendor.name = data.get('name', vendor.name)
        vendor.contact_details = data.get('contact_details', vendor.contact_details)
        vendor.address = data.get('address', vendor.address)
        vendor.vendor_code = data.get('vendor_code', vendor.vendor_code)
        vendor.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'DELETE':
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Purchase Order Tracking
@api_view(['POST'])
def create_purchase_order(request):
    data = request.data
    try:
        purchase_order = PurchaseOrder.objects.create(
            po_number=data['po_number'],
            vendor_id=data['vendor_id'],
            order_date=data['order_date'],
            delivery_date=data['delivery_date'],
            items=data['items'],
            quantity=data['quantity'],
            status=data['status']
        )
        return Response({'id': purchase_order.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_purchase_orders(request):
    purchase_orders = PurchaseOrder.objects.all()
    return Response([{'id': po.id, 'po_number': po.po_number} for po in purchase_orders])

@api_view(['GET', 'PUT', 'DELETE'])
def purchase_order_details(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
    if request.method == 'GET':
        return Response({
            'po_number': purchase_order.po_number,
            'vendor_id': purchase_order.vendor_id,
            'order_date': purchase_order.order_date,
            'delivery_date': purchase_order.delivery_date,
            'items': purchase_order.items,
            'quantity': purchase_order.quantity,
            'status': purchase_order.status
        })
    elif request.method == 'PUT':
        data = request.data
        purchase_order.po_number = data.get('po_number', purchase_order.po_number)
        purchase_order.vendor_id = data.get('vendor_id', purchase_order.vendor_id)
        purchase_order.order_date = data.get('order_date', purchase_order.order_date)
        purchase_order.delivery_date = data.get('delivery_date', purchase_order.delivery_date)
        purchase_order.items = data.get('items', purchase_order.items)
        purchase_order.quantity = data.get('quantity', purchase_order.quantity)
        purchase_order.status = data.get('status', purchase_order.status)
        purchase_order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'DELETE':
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Vendor Performance Evaluation
@api_view(['GET'])
def vendor_performance(request, vendor_id):
    vendor = get_object_or_404(Vendor, id=vendor_id)
    return Response({
        'on_time_delivery_rate': vendor.on_time_delivery_rate,
        'quality_rating_avg': vendor.quality_rating_avg,
        'average_response_time': vendor.average_response_time,
        'fulfillment_rate': vendor.fulfillment_rate
    })

# Update Acknowledgment Endpoint
@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=po_id)
    if request.method == 'POST':
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        return Response({'message': 'Purchase order acknowledged successfully.'}, status=status.HTTP_200_OK)

