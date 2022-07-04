from django.shortcuts import render, HttpResponse
import csv 
from .models import Protein, pfam, domains, taxanomy
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializer import ProteinSerializer,PFamSerializer, DomainSerializer, TaxanomySerializer,  proteintaxaserialize, pfamproteinserializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from rest_framework.views import APIView






# api/protein/
@api_view(['GET', 'POST'])
def protein_list(request):

    if request.method == 'GET':
        proteins = Protein.objects.all()[:10]
        serializer = ProteinSerializer(proteins, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProteinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# api/protein/protein_id
@api_view(['GET', 'PUT'])
def protein_details_api_view(request, protein_id):

    try:
        protein = Protein.objects.get(protein_id=protein_id)
    except protein.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ProteinSerializer(protein)
        return Response(serializer.data)

    elif request.method == 'PUT':
        jsondata = JSONParser().parse(request)
        serializer = ProteinSerializer(protein, data=jsondata)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', "POST"])
def domains_list_api_view(request):
    
    if request.method == "GET":
        domain = domains.objects.all()
        serializer = DomainSerializer(domain, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        domain = DomainSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)   


# pfam/[domain_id]/
@api_view(['GET'])
def get_pfam_with_id(request, domain_id):
    
    try:
        pfamdata = pfam.objects.get(domain_id=domain_id)
    except pfam.DoesNotExist:
        return HttpResponse(f"pfam with domain id {domain_id}, not found.")

    if request.method == "GET":
        pfdata = PFamSerializer(pfamdata)
        return Response(pfdata.data)
    else: 
        return redirect('/')

    # elif request.method == "PUT":



# api/proteins/[taxa_id] 
@api_view(['GET'])
def Protein_list_taxa_id(request, taxa_id):

    if request.method == "GET":
        l = [ ]
        protein_list = Protein.objects.all().filter(taxanomy__taxa_id=taxa_id)
        for pl in protein_list:
            print(protein_list)
            l.append(pl)
            jsonserialized = proteintaxaserialize(l, many=True)        
        return Response(jsonserialized.data)

    else:
        return HttpResponse(f"No proteins with {taxa_id} found.")


# api/pfam/[PFAM ID]
@api_view(['GET'])
def get_pfam_with_pfam_id(request, pfam_id):

    if request.method == "GET":
        try:
            pf = pfam.objects.get(domain_id=pfam_id)

            if pf:
                seriazer = PFamSerializer(pf.data)
                return Response(seriazer.data)
            else:
                print('pfam not found!')
                pass
        except pf.DoesNotExist as e:
            raise ValueError(e)
        





# http://127.0.0.1:8000/api/pfams/[TAXA ID]
@api_view(['GET'])
def get_pfam_with_taxaid(request, taxa_id):
    pro_List =  []
    if request.method == "GET":        
        domain_list = domains.objects.all().filter(protein_id__taxanomy__taxa_id=taxa_id)
        pro_List.append(protein_list)
        print(pro_List)
        serializ_data = pfamproteinserializer(domain_list, many=True)
        return Response(serializ_data.data)

    else:
        raise Exception("Any other method is not applicable. ")




# http://127.0.0.1:8000/api/coverage/[PROTEIN ID]
@api_view(["GET"])
def protein_coverage(request, protein_id):
    if request.method == "GET":
        l = []
        try:
            domain = domains.objects.filter(protein_id__protein_id=protein_id)
            protein = Protein.objects.get(protein_id=protein_id)

            if domain:
                for d in domain:
                    start = d.start
                    stop = d.stop
                    start = int(start)
                    stop = int(stop)
                    domain_length = stop-start
                    l.append(domain_length)

                protein_length = protein.length

                print(domain_length)
                protein_length = int(protein_length)

                coverage = (domain_length)/protein_length

                return HttpResponse(f"Coverage: {coverage}")
        except Exception as e:
            raise Exception(e)

    else:
        print("Only get method is allowed.")

# class ProteinListTaxaId(APIView):
#     """
#     Retrieve, update or delete a snippet instance.
#     """
#     def get_object(self, taxa_id):
#         try:
#             return Protein.objects.all().filter(taxanomy__taxa_id=taxa_id)
#         except Snippet.DoesNotExist:
#             raise Http404

#     def get(self, request, taxa_id, format=None):
#         proteins = self.get_object(taxa_id)
#         serializer = ProteinSerializer(proteins)
#         return Response(serializer.data)

#     def put(self, request, taxa_id, format=None):
#         snippet = self.get_object(taxa_id)
#         serializer = SnippetSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, taxa_id, format=None):
#         snippet = self.get_object(taxa_id)
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)