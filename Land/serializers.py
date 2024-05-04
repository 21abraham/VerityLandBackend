from rest_framework import serializers
from .models import CustomUser, Buyer, Inspector, Seller


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ['aadhar_number', 'pan_number', 'address', 'mobile_number']


class InspectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspector
        fields = ['designation']


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['aadhar_number', 'pan_number', 'address', 'mobile_number']


class CustomUserSerializer(serializers.ModelSerializer):
    buyer = BuyerSerializer(required=False)
    inspector = InspectorSerializer(required=False)
    seller = SellerSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'user_type', 'buyer', 'inspector', 'seller']

    def create(self, validated_data):
        user_type = validated_data.get('user_type')
        buyer_data = validated_data.pop('buyer', None)
        inspector_data = validated_data.pop('inspector', None)
        seller_data = validated_data.pop('seller', None)
        user = CustomUser.objects.create_user(**validated_data)

        if user_type == 1 and inspector_data:
            if hasattr(user, 'inspector'):
                inspector_instance = user.inspector
                inspector_instance.designation = inspector_data['designation']
                inspector_instance.save()
            else:
                Inspector.objects.create(admin=user, **inspector_data)
        elif user_type == 2 and buyer_data:
            if hasattr(user, 'buyer'):
                buyer_instance = user.buyer
                for attr, value in buyer_data.items():
                    setattr(buyer_instance, attr, value)
                buyer_instance.save()
            else:
                Buyer.objects.create(admin=user, **buyer_data)
        elif user_type == 3 and seller_data:
            if hasattr(user, 'seller'):
                seller_instance = user.seller
                for attr, value in seller_data.items():
                    setattr(seller_instance, attr, value)
                seller_instance.save()
            else:
                Seller.objects.create(admin=user, **seller_data)

        return user

