from django.db import models


class Categorie(models.Model):
    code = models.AutoField(db_column='Code', primary_key=True, blank=True)  # Field name made lowercase.
    libelle = models.TextField(db_column='Libelle', unique=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Categorie'

    def __str__(self):
        return self.libelle


class Client(models.Model):
    code = models.CharField(db_column='Code', primary_key=True, max_length=255)  # Field name made lowercase.
    societe = models.TextField(db_column='Societe', unique=True)  # Field name made lowercase.
    contact = models.TextField(db_column='Contact', blank=True, null=True)  # Field name made lowercase.
    fonction = models.TextField(db_column='Fonction', blank=True, null=True)  # Field name made lowercase.
    adresse = models.TextField(db_column='Adresse', blank=True, null=True)  # Field name made lowercase.
    ville = models.TextField(db_column='Ville', blank=True, null=True)  # Field name made lowercase.
    region = models.TextField(db_column='Region', blank=True, null=True)  # Field name made lowercase.
    code_postal = models.CharField(db_column='Code_postal', blank=True, null=True,
                                   max_length=255)  # Field name made lowercase.
    pays = models.TextField(db_column='Pays', blank=True, null=True)  # Field name made lowercase.
    telephone = models.TextField(db_column='Telephone', blank=True, null=True)  # Field name made lowercase.
    fax = models.TextField(db_column='Fax', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Client'

    def __str__(self):
        return self.code


class Commande(models.Model):
    numero = models.AutoField(db_column='Numero', primary_key=True, blank=True)  # Field name made lowercase.
    client = models.ForeignKey(Client, models.DO_NOTHING, db_column='Client', related_name='commandes',
                               related_query_name='commande')  # Field name made lowercase.
    saisiele = models.DateField(db_column='SaisieLe')  # Field name made lowercase.
    envoyeele = models.DateField(db_column='EnvoyeeLe', blank=True, null=True)  # Field name made lowercase.
    port = models.DecimalField(db_column='Port', max_digits=10, decimal_places=5, blank=True,
                               null=True)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    destinataire = models.TextField(db_column='Destinataire', blank=True, null=True)  # Field name made lowercase.
    adresse_livraison = models.TextField(db_column='Adresse_livraison', blank=True,
                                         null=True)  # Field name made lowercase.
    ville_livraison = models.TextField(db_column='Ville_livraison', blank=True, null=True)  # Field name made lowercase.
    region_livraison = models.TextField(db_column='Region_livraison', blank=True,
                                        null=True)  # Field name made lowercase.
    code_postal_livraison = models.TextField(db_column='Code_Postal_livraison', blank=True,
                                             null=True)  # Field name made lowercase.
    pays_livraison = models.TextField(db_column='Pays_Livraison', blank=True, null=True)  # Field name made lowercase.
    remise = models.DecimalField(db_column='Remise', max_digits=10,
                                 decimal_places=5)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    produits = models.ManyToManyField('Produit', through='Ligne')

    class Meta:
        db_table = 'Commande'

    def lignes(self):
        return Ligne.objects.filter(commande=self)

    def __str__(self):
        return f"{self.numero}  {self.envoyeele}"


class Ligne(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True, blank=True)  # Field name made lowercase.
    commande = models.ForeignKey(Commande, models.DO_NOTHING, db_column='Commande', related_name='commande',
                                 related_query_name='commande')  # Field name made lowercase.
    produit = models.ForeignKey('Produit', models.DO_NOTHING, db_column='Produit', related_name='produit',
                                related_query_name='produit')  # Field name made lowercase.
    quantite = models.SmallIntegerField(db_column='Quantite')  # Field name made lowercase.

    class Meta:
        db_table = 'Ligne'

    def __str__(self):
        return f"{self.commande.numero} {self.produit.nom} {self.quantite}"


class Produit(models.Model):
    reference = models.AutoField(db_column='Reference', primary_key=True, blank=True)  # Field name made lowercase.
    nom = models.TextField(db_column='Nom', unique=True)  # Field name made lowercase.
    fournisseur = models.IntegerField(db_column='Fournisseur')  # Field name made lowercase.
    categorie = models.ForeignKey(Categorie, models.DO_NOTHING, db_column='Categorie', related_name='produits',
                                  related_query_name='produit')  # Field name made lowercase.
    quantite_par_unite = models.TextField(db_column='Quantite_par_unite', blank=True,
                                          null=True)  # Field name made lowercase.
    prix_unitaire = models.DecimalField(db_column='Prix_unitaire', max_digits=10,
                                        decimal_places=5)  # Field name made lowercase. max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    unites_en_stock = models.SmallIntegerField(db_column='Unites_en_stock')  # Field name made lowercase.
    unites_commandees = models.SmallIntegerField(db_column='Unites_commandees')  # Field name made lowercase.
    niveau_de_reappro = models.SmallIntegerField(db_column='Niveau_de_reappro')  # Field name made lowercase.
    indisponible = models.SmallIntegerField(db_column='Indisponible')  # Field name made lowercase.

    class Meta:
        db_table = 'Produit'

    def commandes(self):
        return self.commande_set.all()

    def lignes(self):
        return Ligne.objects.filter(produit=self)

    def __str__(self):
        return self.nom