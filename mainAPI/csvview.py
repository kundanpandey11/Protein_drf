from django.shortcuts import render, HttpResponse
import csv 
from .models import Protein, pfam, domains, taxanomy
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .serializer import ProteinSerializer, PFamSerializer, DomainSerializer, TaxanomySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count







# api/protein/csv
def post_csv_to_protein(request):
    with open('assignment_data_sequences.csv', 'r', newline='', encoding='utf-8') as proteincsv:
        reader = csv.reader(proteincsv)
        proteins  = []
        for _, row in enumerate(reader):
            protein = Protein(
                protein_id = row[0],
                sequence = row[1],
                length = 22,
            )
            proteins.append(protein)
            if len(proteins) == 9030:
                Protein.objects.bulk_create(proteins)
                proteins = []
            else:
                print('All the data loaded successfully. ')
        if proteins:
            Protein.objects.bulk_create(proteins)
        print(f'Proteings added from the list to data base {len(proteins)}.')

        l = 0
        for name in Protein.objects.all():
            l+=1
        print(l) 

        protein_id_duplicate = Protein.objects.values('protein_id', 'id').annotate(Count('protein_id')).order_by().filter(protein_id__count__gt=1)

        # the below codes helps check if there are any duplicate field in the database
        all_duplicate_list = Protein.objects.filter(id__in=[item['id'] for item in duplicate_names])
        print(duplicate_objects)   
        return HttpResponse("Success to database!")








# api/csv/taxanomy
def post_csv_to_taxanomy(request):
    with open('assignment_data_set.csv', 'r', newline='', encoding='utf-8') as taxacsv:
        rows = csv.reader(taxacsv)
        taxalist = []
        prolist = []
        protein_id = ''
        count = 0
        for _, row in enumerate(rows):
            count+=1
            if _ > 8678:
                protein_id = row[0]
                pro = Protein(length=row[8])            
                prolist.append(pro)
                try:
                    protein = Protein.objects.get(protein_id=protein_id)
                    if protein:
                        genus_species = row[3].split(" ")
                        taxanom = taxanomy(
                            protein_id=protein,
                            taxa_id= row[1],
                            clade=row[2],
                            genus = genus_species[0],
                            species= genus_species[1],
                        )
                        taxanom.save()
                        print(protein_id, count)
                        # taxalist.append(taxanom)
                        # if count <= 9999:
                        #     taxanomy.objects.bulk_create(taxalist) 
                        
                        # print(protein_id, count)
                        # 
                        # taxanomy.objects.all().delete()                   
                        # print(f'saving taxanomy with id {protein_id}...')
                        # taxalist.append(taxanom)
                        # if len(taxalist) > 9000:
                        #     print('creating new taxanomy instances...')
                        #     Protein.objects.update(length=row[8])
                        #     taxanomy.objects.bulk_create(texalist)
                        #     print('job done!')
                        #     texalist = []                   
                    elif not protein:
                        print('protein with id {protein_id} not found')
                        pass
                
                        
                except protein.DoesNotExist as pd:
                    print(pd)
                    pass
            else: 
                print("can't be done!")  
        return HttpResponse('working on filling the data to taxa....')



# api/csv/domain
def post_csv_to_domain(request):  
    with open('assignment_data_set.csv', 'r', newline='', encoding='utf-8') as domaincsv:
        rows = csv.reader(domaincsv)
        count = 0
        for _, row in enumerate(rows):
            count+=1
            protein_id = row[0]
            description = row[4]
            start = row[6]
            stop = row[7]
            hidden_domain_id = row[5]
            try:
                protein = Protein.objects.get(protein_id=protein_id)
                if protein:                    
                    domain = domains(
                        protein_id=protein,
                        hidden_domain_id=hidden_domain_id,
                        start=start,
                        stop=stop,
                        description=description)
                    domain.save()
                    print(protein_id, count)                                     
                elif not protein:
                    print('protein with id {protein_id} not found')
                    pass
            except protein.DoesNotExist as e:
                print(e)
                pass
        return HttpResponse('Adding domains to the proteins...')



# api/csv/pfam
def post_csv_to_pfam(request):
    
    with open('pfam_descriptions.csv', 'r', newline='', encoding='utf-8') as pfamcsv:
        rows = csv.reader(pfamcsv)
        count = 0
        for _, row in enumerate(rows):
            count+=1
            
            hidden_domain_id = row[0]
            domain_description = row[1]
            print(hidden_domain_id)
            print(domain_description)


            try:
                domain = domains.objects.all().filter(hidden_domain_id=hidden_domain_id)
                if domain:                  
                    pf = pfam(             
                        domain_id=hidden_domain_id,
                        domain_descripton=domain_description)
                    
                    pf.save()
                    pf.domains.add(domain)
                    pf.save()


                    print(hidden_domain_id, count)
                                      
                elif not domain:
                    print('domain with id {hidden_domain_id} not found')
                    pass
            except Exception as e:
                print(e)
                pass

        return HttpResponse('Adding pfam to the domains...')


# api/csv/protein/update
def update_length_protein(request):
    proteins = Protein.objects.all()

    for protein in proteins:
        protein_id = protein.protein_id
        protein_sequence =  protein.sequence
        protein_length = 0

        try:
            pro = Protein.objects.get(protein_id=protein_id)
            if pro:
                sequence = pro.sequence
                sequence = str(sequence)
                length = len(sequence)
                length = int(length)
                total = protein_length + length
                pro.length = total
                pro.save()
                print(pro.protein_id)
            elif not pro:
                print("something went wrong!")
                pass
        except Exception as e:
            print(e)
            pass 
    return HttpResponse("Protein model is bing updated.")



# csv/pfam/add
def add_pfam_to_domain(request):
    with open('pfam_descriptions.csv', 'r', newline='', encoding='utf-8') as pfamcsv:
        rows = csv.reader(pfamcsv)
        count = 0
        for _, row in enumerate(rows):
            count +=1
            hidden_domain_id = row[0]
            domain_description = row[1]
            try: 
                domain = domains.objects.all().filter(hidden_domain_id=hidden_domain_id)
                if domain:
                    for dom in domain:
                        pf  = pfam(
                            domains=dom,
                            domain_id=hidden_domain_id,
                            domain_descripton=domain_description
                        )
                        pf.save()
                        print(f"{hidden_domain_id}, {count} ")
                elif not dom:
                    print(f'no domain with id {hidden_domain_id}')
                    pass
            except Exception as e:
                print(e)
                pass

        return HttpResponse("Uploading pfam to domains. ")

