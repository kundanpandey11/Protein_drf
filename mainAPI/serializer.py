from rest_framework.serializers import ModelSerializer, ReadOnlyField
from rest_framework import serializers
from .models import Protein, pfam, domains, taxanomy 


class TaxanomySerializer(ModelSerializer):
    class Meta:
        model = taxanomy
        fields = ['taxa_id', "clade", 'genus', 'species']


class PFamSerializer(ModelSerializer):
    class Meta:
        model = pfam
        fields = ['domain_id', 'domain_descripton']



class DomainSerializer(ModelSerializer):
    pfam = PFamSerializer(many=True, read_only=True)
    class Meta:
        model = domains
        fields = ['pfam', 'description', 'start', 'stop']


class ProteinSerializer(ModelSerializer):
    taxanomy = TaxanomySerializer(many=True, read_only=True)
    domains = DomainSerializer(many=True, read_only=True)
    class Meta:
        model = Protein
        fields = ['protein_id', 'sequence', 'taxanomy', 'length', 'domains']


class proteintaxaserialize(ModelSerializer):
    class Meta:
        model = Protein
        fields = ['id', 'protein_id']



class pfamproteinserializer(ModelSerializer):
    pfam = PFamSerializer(many=True, read_only=True)
    class Meta:
        model = domains
        fields = ['id', 'pfam']


    # def get_accounts_items(self, obj):
    #     customer_account_query = models.Account.objects.filter(
    #         customer_id=obj.id)
    #     serializer = AccountSerializer(customer_account_query, many=True)

    #     return serializer.data