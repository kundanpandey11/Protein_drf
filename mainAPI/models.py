from django.db import models

# Create your models here.

class Protein(models.Model):
    protein_id = models.CharField(max_length=12, unique=True)
    sequence = models.CharField(max_length=300)
    length = models.IntegerField()

    def __str__(self):
        return self.protein_id




class domains(models.Model):
    protein_id = models.ForeignKey(Protein, related_name='domains', on_delete=models.PROTECT, null=True)
    description = models.CharField(max_length=400)
    hidden_domain_id = models.CharField(max_length=20, null=True)
    start = models.IntegerField()
    stop = models.IntegerField()

    def __str__(self):
        return self.description
    



class taxanomy(models.Model):
    protein_id = models.ForeignKey(Protein, related_name='taxanomy', on_delete=models.PROTECT, null=True)
    taxa_id = models.CharField(max_length=12)
    clade = models.CharField(max_length=2)
    genus = models.CharField(max_length=50)
    species = models.CharField(max_length=50)

    def __str__(self):
        return self.taxa_id


class pfam(models.Model):
    domains = models.ForeignKey(domains, on_delete=models.CASCADE, related_name='pfam', null=True)
    domain_id = models.CharField(max_length=10)
    domain_descripton = models.CharField(max_length=200)

    def __str__(self):
        return self.domain_descripton




    











