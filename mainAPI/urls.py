from django.urls import path
from . import views 
from . import csvview
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [ 
    path('protein/', views.protein_list, name='protein-list'),
    path('protein/<protein_id>/', views.protein_details_api_view, name='protein-details'),
    path('domain/', views.domains_list_api_view, name='domain-list'),
    path('pfam/<str:domain_id>/', views.get_pfam_with_id, name='pfam-id-view'),
    path('proteins/<str:taxa_id>/', views.Protein_list_taxa_id, name='protein-list-taxa-id'),
    path('pfam/<str:pfam_id>/', views.get_pfam_with_pfam_id, name='pfam-Pfam_id'),
    path('pfams/<str:taxa_id>', views.get_pfam_with_taxaid, name='pfams-with-taxa_id'),
    path('coverage/<str:protein_id>/', views.protein_coverage, name='protein-coverage'),



    # urls to fill the database from csv file
    path('csv/protein', csvview.post_csv_to_protein, name='csv-to-protein'),
    path('csv/taxanomy', csvview.post_csv_to_taxanomy, name='csv-to-taxanomy'),
    path('csv/domain', csvview.post_csv_to_domain, name='csv-to-domain'),
    path('csv/pfam', csvview.post_csv_to_pfam, name='csv-to-pfam'),
    path('csv/proteinupdate', csvview.update_length_protein, name='update-protein'),
    path('csv/pfam/add', csvview.add_pfam_to_domain, name='add-pfam'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
