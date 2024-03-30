from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import (LipilaUser, LipilaCollection, LipilaDisbursement)
from web.models import Product, BNPL, Invoice, InvoiceLipilaUser

class LipilaUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipilaUser
        fields = ('id', 'username', 'city', 'email', 'password',
                  'phone_number', 'bio', 'user_category')
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = LipilaUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LipilaCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipilaCollection
        fields = ('payer', 'payee', 'amount', 'description')