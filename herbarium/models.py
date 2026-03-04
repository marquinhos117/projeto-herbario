from django.db import models

# ==========================================
# CLASSE: Person (Pessoa)
# Representa todos os usuários e colaboradores:
# alunos (digitadores), professores (curadores) e coletores.
# ==========================================
class Person(models.Model):
    full_name = models.CharField(max_length=150) # Nome completo
    collector_acronym = models.CharField(max_length=50, blank=True, null=True) # Ex: A. Silva
    institution = models.CharField(max_length=150, blank=True, null=True) # Instituição de origem
    email = models.EmailField(max_length=100, unique=True) # Usado para login
    access_level = models.CharField(max_length=20) # Ex: Student, Curator, Admin
    account_status = models.CharField(max_length=20, default='Active') # Ativa ou Inativa

    def __str__(self):
        return self.full_name


# ==========================================
# CLASSE: Taxonomy (Taxonomia)
# Serve como um dicionário oficial de nomes.
# Evita que o mesmo nome de planta seja escrito de várias formas erradas.
# ==========================================
class Taxonomy(models.Model):
    scientific_name = models.CharField(max_length=255, unique=True) # Gênero + epíteto + autor
    author = models.CharField(max_length=100, blank=True, null=True) # Autor do nome
    family = models.CharField(max_length=100) # Família botânica
    genus = models.CharField(max_length=100) # Gênero
    specific_epithet = models.CharField(max_length=100, blank=True, null=True) # Epíteto específico
    taxonomic_status = models.CharField(max_length=30, default='Accepted') # Aceito ou Sinônimo

    # Auto-relacionamento: Se for um sinônimo, aponta para o ID do nome aceito
    accepted_name = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='synonyms')

    def __str__(self):
        return self.scientific_name


# ==========================================
# CLASSE: Collection (Coleção)
# Representa a entidade do herbário (ex: Herbário da Faculdade X).
# ==========================================
class Collection(models.Model):
    acronym = models.CharField(max_length=10, unique=True) # Ex: UFG, UB, RB
    name = models.CharField(max_length=150) # Nome completo do herbário
    curator = models.ForeignKey(Person, on_delete=models.PROTECT) # Professor responsável

    def __str__(self):
        return self.acronym


# ==========================================
# CLASSE: CollectionEvent (Evento de Coleta)
# Armazena ONDE e QUANDO a planta foi coletada no campo.
# ==========================================
class CollectionEvent(models.Model):
    collection_date = models.DateField() # Data da coleta no campo
    country = models.CharField(max_length=50, default='Brazil')
    state_province = models.CharField(max_length=50) # Estado
    municipality = models.CharField(max_length=100) # Cidade
    locality = models.TextField() # Descrição detalhada do local

    # Coordenadas inseridas manualmente pelo usuário
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    habitat = models.TextField(blank=True, null=True) # Tipo de vegetação (ex: Cerrado)

    def __str__(self):
        return f"{self.municipality} - {self.collection_date}"


# ==========================================
# CLASSE: Occurrence (Ocorrência / Espécime)
# A tabela principal. Representa a planta física guardada no herbário (Exsicata).
# Conecta todos os outros dados (Quem coletou, onde, qual o nome).
# ==========================================
class Occurrence(models.Model):
    catalog_number = models.CharField(max_length=50, unique=True) # Número de Tombo (ID único do herbário)
    field_number = models.CharField(max_length=50) # Número que o coletor deu no campo
    type_status = models.CharField(max_length=50, blank=True, null=True) # Ex: Holótipo, Isótipo

    # Controle de fluxo (Workflow)
    submission_status = models.CharField(max_length=20, default='Pending') # Pendente ou Aprovado
    approval_date = models.DateField(null=True, blank=True)

    # Relacionamentos de Curadoria
    data_entry_by = models.ForeignKey(Person, on_delete=models.PROTECT, related_name='entries') # Aluno que digitou
    approved_by = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, blank=True, related_name='approvals') # Professor
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE) # A qual herbário pertence
    event = models.ForeignKey(CollectionEvent, on_delete=models.CASCADE) # Dados geográficos

    # Muitos-para-Muitos: Uma planta pode ter vários coletores
    collectors = models.ManyToManyField(Person, through='OccurrenceCollector')

    # Identificação atual (Cache): Aponta para o nome científico válido no momento
    current_identification = models.OneToOneField(
        'IdentificationHistory',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='main_occurrence'
    )

    def __str__(self):
        return f"Catalog: {self.catalog_number}"


# ==========================================
# CLASSE: IdentificationHistory (Histórico de Identificação)
# Registra quem deu o nome à planta. Como a taxonomia muda,
# uma planta pode ser identificada como 'Espécie A' em 2010 e 'Espécie B' em 2024.
# ==========================================
class IdentificationHistory(models.Model):
    identification_date = models.DateField()
    remarks = models.TextField(blank=True, null=True) # Observações técnicas do botânico

    occurrence = models.ForeignKey(Occurrence, on_delete=models.CASCADE, related_name='identifications')
    taxonomy = models.ForeignKey(Taxonomy, on_delete=models.PROTECT) # Nome científico atribuído
    identified_by = models.ForeignKey(Person, on_delete=models.PROTECT) # Especialista que identificou

    def __str__(self):
        return f"{self.taxonomy.scientific_name} ({self.identification_date})"


# ==========================================
# CLASSE: OccurrenceCollector (Tabela Intermediária)
# Resolve a relação de muitos-para-muitos entre Ocorrência e Coletores.
# Define quem é o coletor principal do grupo.
# ==========================================
class OccurrenceCollector(models.Model):
    occurrence = models.ForeignKey(Occurrence, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False) # Define se é o coletor principal (ex: Silva, A. et al.)

    class Meta:
        unique_together = ('occurrence', 'person') # Impede duplicar a mesma pessoa na mesma planta


# ==========================================
# CLASSE: SpecimenImage (Fotos)
# Armazena as imagens da exsicata ou da planta viva.
# ==========================================
class SpecimenImage(models.Model):
    occurrence = models.ForeignKey(Occurrence, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='herbarium/specimens/') # O Django cria a pasta automaticamente
    image_type = models.CharField(max_length=50, blank=True) # Ex: Scan da folha, Foto do campo
    created_at = models.DateTimeField(auto_now_add=True)