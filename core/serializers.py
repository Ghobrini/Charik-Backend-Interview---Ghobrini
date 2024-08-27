from rest_framework import serializers


class ContactSerialiser(serializers.Serializer):
    """
    Serializer for contact objects.

    This serializer handles the validation and deserialization of contact data.
    """
    firstname = serializers.CharField(required=True, max_length=150)
    lastname = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True)
    company = serializers.CharField(required=True, max_length=17)
    website = serializers.CharField(required=False, max_length=17)
    

class DealSerialiser(serializers.Serializer):
    """
    Serializer for deal objects.

    This serializer handles the validation and deserialization of deal data.
    """
    amount = serializers.DecimalField(required=True, max_digits=30, decimal_places=2)
    closedate = serializers.DateTimeField(required=True)
    dealname = serializers.CharField(required=True, max_length=150)
    def validate(self, data):
        data["pipeline"]="default"
        data["dealstage"]="contractsent"
        return data
    
class AssociateSerialiser(serializers.Serializer):
    """
    Serializer for association objects between contacts and deals.

    This serializer handles the validation and deserialization of association data.
    """
    contact_id = serializers.CharField(required=True, max_length=150)
    deal_id = serializers.CharField(required=True, max_length=150)