from django.template.loader import get_template
from rest_framework import serializers
from .models import Collect, Payment
from django.core.mail import send_mail


class CollectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collect
        fields = '__all__'

    def create(self, validated_data):
        collect = Collect.objects.create(**validated_data)
        email_template = get_template("payment_api/message_to_collect_author.html")
        message_context = {"aim_sum": str(collect.aim_sum) + ' р',
                           'end_date': str(collect.finish_collect_date_time),
                           'name': collect.name, 'occasion': collect.occasion,
                           'author': collect.author, 'infinity_sum': collect.infinity_sum}
        message = email_template.render(message_context)
        send_mail(subject="Создание группового денежного сбора.",
                  message=message,
                  from_email=None,
                  recipient_list=[collect.author.email])
        return collect
        
        
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('pk', 'user', 'collect', 'payment')

    def create(self, validated_data):
        payment = Payment.objects.create(**validated_data)
        collect = payment.collect
        email_template = get_template("payment_api/message_to_payment_author.html")
        message_context = {"payment": payment, "aim_sum": str(collect.aim_sum) + ' р',
                           'end_date': str(collect.finish_collect_date_time),
                           'name': collect.name, 'occasion': collect.occasion}
        message = email_template.render(message_context)
        send_mail(subject="Участие в групповом денежном сборе.",
                  message=message,
                  from_email=None,
                  recipient_list=[payment.user.email])
        return payment

    def update(self, instance, validated_data):
        instance.collect = validated_data.get('collect', instance.collect)
        instance.user = validated_data.get('user', instance.user)
        instance.payment = validated_data.get('payment', instance.payment)
        instance.save()
        return instance
