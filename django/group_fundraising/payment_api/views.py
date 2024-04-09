from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, serializers, generics
from .models import Collect, Payment, now
from django.db import transaction
from .serializers import CollectSerializer, PaymentSerializer
from django.core.signals import request_finished

# Create your views here.


@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'Add Collect': '/collects/create',
        'Get all Collects': '/collects',
        'Get Collect by pk': '/collects/pk',
        'Update Collect': '/collects/pk/update',
        'Delete Collect': '/collects/pk/delete',
        'Add Payment': '/payments/create',
        'Get all Payments': '/payments',
        'Get Payment by pk': '/payments/pk',
        'Update Payment': '/payments/pk/update',
        'Delete Payment': '/payments/pk/delete',
    }
    return Response(api_urls)
    

class CollectCreate(generics.CreateAPIView):
    """Class for Collect creating"""
    serializer_class = CollectSerializer

    def create(self, request, *args, **kwargs):
        serializer = CollectSerializer(data=request.data)
        # validating for already existing data
        if Collect.objects.filter(**request.data).exists():
            raise serializers.ValidationError('This data already exists')
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CollectDetail(generics.GenericAPIView):
    """Class for Collects reading"""
    serializer_class = CollectSerializer

    def get_queryset(self):
        if self.request.query_params:
            collects = Collect.objects.filter(**self.request.query_params.dict())
        else:
            pk = self.kwargs.get('pk')
            if pk:
                collects = Collect.objects.filter(pk=pk)
            else:
                collects = Collect.objects.all()
        return collects

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request, pk=None):
        collects = self.get_queryset()
        if collects:
            serializer = CollectSerializer(instance=collects, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CollectUpdate(generics.UpdateAPIView):
    """Class for Collect updating"""
    serializer_class = CollectSerializer

    def update(self, request, *args, **kwargs):
        collect = get_object_or_404(Collect, pk=kwargs.get('pk'))
        serializer = CollectSerializer(instance=collect, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.clear()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class CollectDelete(generics.DestroyAPIView):
    """Class for Collect deleting"""
    serializer_class = CollectSerializer

    def destroy(self, request, *args, **kwargs):
        collect = get_object_or_404(Collect, pk=self.kwargs.get('pk'))
        collect.delete()
        cache.clear()
        return Response(status=status.HTTP_202_ACCEPTED)


class PaymentCreate(generics.CreateAPIView):
    """Class for Payment creating"""
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            collect = serializer.validated_data['collect']
            if now() < collect.finish_collect_date_time:
                with transaction.atomic():
                    payment = serializer.create(serializer.validated_data)
                    collect.update_collect_after_payment_creation(payment=payment)
                return Response(serializer.data)
            else:
                # the collect is already ended
                return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class PaymentDetail(generics.GenericAPIView):
    """Class for Payments reading"""
    serializer_class = PaymentSerializer

    def get_queryset(self):
        if self.request.query_params:
            payments = Payment.objects.filter(**self.request.query_params.dict())
        else:
            pk = self.kwargs.get('pk')
            if pk:
                payments = Payment.objects.filter(pk=pk)
            else:
                payments = Payment.objects.all()
        return payments

    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request, pk=None):
        payments = self.get_queryset()
        if payments:
            serializer = PaymentSerializer(instance=payments, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PaymentUpdate(generics.UpdateAPIView):
    """Class for Payment updating"""
    serializer_class = PaymentSerializer

    def update(self, request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=kwargs.get('pk'))
        old_pay = int(payment.payment)
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            if payment.can_update():
                old_collect_pk = payment.collect.pk
                new_collect = serializer.validated_data.get('collect', None)
                with transaction.atomic():
                    if new_collect and old_collect_pk != new_collect.pk:
                        payment.collect.update_collect_before_delete_payment(payment=payment)
                        payment = serializer.update(payment, serializer.validated_data)
                        payment.collect.update_collect_after_payment_creation(payment=payment)
                    else:
                        serializer.update(payment, serializer.validated_data)
                        payment.collect.update_collect_after_update_payment(payment=payment, old_pay=old_pay)
                    cache.clear()
                return Response(serializer.data)
            else:
                Response(status=status.HTTP_403_FORBIDDEN)
        else:

            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)
        

class PaymentDelete(generics.DestroyAPIView):
    """Class for Collect deleting"""
    serializer_class = PaymentSerializer

    def destroy(self, request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=self.kwargs.get('pk'))
        if payment.can_delete():
            with transaction.atomic():
                payment.collect.update_collect_before_delete_payment(payment=payment)
                payment.delete()
                cache.clear()
        else:
            Response(status=status.HTTP_403_FORBIDDEN)
        return Response(status=status.HTTP_202_ACCEPTED)
