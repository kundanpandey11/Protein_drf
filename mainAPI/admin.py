from django.contrib import admin
from .models import Protein, domains, pfam, taxanomy

admin.site.register(Protein)

admin.site.register(domains)
 
admin.site.register(pfam)

admin.site.register(taxanomy)