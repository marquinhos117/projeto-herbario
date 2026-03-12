"""
Script de seed de dados para o sistema Herbário IF Goiano.
Uso: python manage.py shell < seed_data.py
"""
import os, sys, django

# Configura o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')
django.setup()

from django.contrib.auth.models import User
from herbarium.models import (
    Pessoa, Taxonomia, Colecao, RegistroColeta,
    Ocorrencia, HistoricoIdentificacao, OcorrenciaColetor, ImagemEspecime
)
from datetime import date

print("🌿 Iniciando seed de dados do Herbário IF Goiano...")

# ==============================================================================
# 1. PESSOAS / USUÁRIOS
# ==============================================================================
print("\n[1/5] Criando usuários e perfis de Pessoas...")

pessoas_dados = [
    {"username": "ana.botanica",  "nome": "Ana Paula Souza Ferreira",   "acronimo": "APSF", "nivel": "CURADOR",  "inst": "IF Goiano - Campus Urutaí"},
    {"username": "carlos.faria",  "nome": "Carlos Eduardo Faria Lima",  "acronimo": "CEFL", "nivel": "ALUNO",    "inst": "IF Goiano - Campus Urutaí"},
    {"username": "julia.mendes",  "nome": "Júlia Cristina Mendes",      "acronimo": "JCM",  "nivel": "ALUNO",    "inst": "UFG - Goiânia"},
    {"username": "roberto.assis", "nome": "Roberto Carlos de Assis",    "acronimo": "RCA",  "nivel": "CURADOR",  "inst": "IF Goiano - Campus Morrinhos"},
    {"username": "patricia.gois", "nome": "Patrícia Lemos Góis",        "acronimo": "PLG",  "nivel": "ALUNO",    "inst": "IF Goiano - Campus Urutaí"},
    {"username": "lucas.silva",   "nome": "Lucas Ferreira da Silva",    "acronimo": "LFS",  "nivel": "ALUNO",    "inst": "IF Goiano - Campus Morrinhos"},
    {"username": "marina.costa",  "nome": "Marina Costa de Oliveira",   "acronimo": "MCO",  "nivel": "ALUNO",    "inst": "UFG - Goiânia"},
    {"username": "gabriel.dias",  "nome": "Gabriel Dias Pereira",       "acronimo": "GDP",  "nivel": "CURADOR",  "inst": "UEG - Quirinópolis"},
]

pessoas_criadas = []
for p in pessoas_dados:
    email = f"{p['username']}@herbario.ifgoiano.edu.br"
    if not User.objects.filter(username=p['username']).exists():
        user = User.objects.create_user(username=p['username'], email=email, password="Herbario@2026")
        pessoa = Pessoa.objects.create(
            usuario=user, nome_completo=p['nome'], acronimo_coletor=p['acronimo'],
            email=email, nivel_acesso=p['nivel'], instituicao=p['inst']
        )
        print(f"   ✔ Criado: {p['nome']} ({p['nivel']})")
        pessoas_criadas.append(pessoa)
    else:
        pessoa = Pessoa.objects.get(usuario__username=p['username'])
        pessoas_criadas.append(pessoa)
        print(f"   ➜ Já existe: {p['nome']}")

# ==============================================================================
# 2. TAXONOMIAS (espécies do Cerrado)
# ==============================================================================
print("\n[2/5] Inserindo taxonomias botânicas do Cerrado...")

taxonomias_dados = [
    {"nome": "Hancornia speciosa Gomes",          "familia": "Apocynaceae",    "genero": "Hancornia",   "epiteto": "speciosa"},
    {"nome": "Caryocar brasiliense Cambess.",      "familia": "Caryocaraceae",  "genero": "Caryocar",    "epiteto": "brasiliense"},
    {"nome": "Dimorphandra mollis Benth.",         "familia": "Fabaceae",       "genero": "Dimorphandra", "epiteto": "mollis"},
    {"nome": "Stryphnodendron adstringens Mart.",  "familia": "Fabaceae",       "genero": "Stryphnodendron", "epiteto": "adstringens"},
    {"nome": "Qualea grandiflora Mart.",           "familia": "Vochysiaceae",   "genero": "Qualea",      "epiteto": "grandiflora"},
    {"nome": "Qualea parviflora Mart.",            "familia": "Vochysiaceae",   "genero": "Qualea",      "epiteto": "parviflora"},
    {"nome": "Vochysia tucanorum Mart.",           "familia": "Vochysiaceae",   "genero": "Vochysia",    "epiteto": "tucanorum"},
    {"nome": "Byrsonima crassa Nied.",             "familia": "Malpighiaceae",  "genero": "Byrsonima",   "epiteto": "crassa"},
    {"nome": "Kielmeyera coriacea Mart.",          "familia": "Calophyllaceae", "genero": "Kielmeyera",  "epiteto": "coriacea"},
    {"nome": "Erythroxylum suberosum A.St.-Hil.",  "familia": "Erythroxylaceae","genero": "Erythroxylum","epiteto": "suberosum"},
    {"nome": "Ouratea hexasperma (A.St.-Hil.) Baill.", "familia": "Ochnaceae", "genero": "Ouratea",     "epiteto": "hexasperma"},
    {"nome": "Roupala montana Aubl.",              "familia": "Proteaceae",     "genero": "Roupala",     "epiteto": "montana"},
    {"nome": "Davilla elliptica A.St.-Hil.",       "familia": "Dilleniaceae",   "genero": "Davilla",     "epiteto": "elliptica"},
    {"nome": "Terminalia fagifolia Mart.",         "familia": "Combretaceae",   "genero": "Terminalia",  "epiteto": "fagifolia"},
    {"nome": "Hymenaea stigonocarpa Mart.",        "familia": "Fabaceae",       "genero": "Hymenaea",    "epiteto": "stigonocarpa"},
    {"nome": "Annona coriacea Mart.",              "familia": "Annonaceae",     "genero": "Annona",      "epiteto": "coriacea"},
    {"nome": "Tabebuia aurea (Silva Manso)",       "familia": "Bignoniaceae",   "genero": "Tabebuia",    "epiteto": "aurea"},
    {"nome": "Handroanthus ochraceus (Cham.)",     "familia": "Bignoniaceae",   "genero": "Handroanthus","epiteto": "ochraceus"},
    {"nome": "Kippistia suffruticosa (Vell.)",     "familia": "Asteraceae",     "genero": "Kippistia",   "epiteto": "suffruticosa"},
    {"nome": "Palicourea coriacea (Cham.)",        "familia": "Rubiaceae",      "genero": "Palicourea",  "epiteto": "coriacea"},
]

taxons_criados = []
for t in taxonomias_dados:
    taxon, criado = Taxonomia.objects.get_or_create(
        nome_cientifico=t['nome'],
        defaults={"familia": t['familia'], "genero": t['genero'], "epiteto_especifico": t['epiteto'], "status_taxonomico": "Aceito"}
    )
    taxons_criados.append(taxon)
    if criado:
        print(f"   ✔ {t['nome']}")

# ==============================================================================
# 3. COLEÇÃO (garante que existe)
# ==============================================================================
print("\n[3/5] Verificando Coleção principal...")
colecao, _ = Colecao.objects.get_or_create(
    acronimo="HIFG",
    defaults={"nome_completo": "Herbário IF Goiano", "id_curador": pessoas_criadas[0]}
)
print(f"   ✔ Coleção: {colecao.nome_completo} ({colecao.acronimo})")

# ==============================================================================
# 4. REGISTROS DE COLETA & OCORRÊNCIAS
# ==============================================================================
print("\n[4/5] Inserindo registros de coleta e ocorrências...")

coletas_dados = [
    {"municipio": "Urutaí",        "estado": "GO", "localidade": "Campus IF Goiano - Urutaí, próximo ao viveiro",       "habitat": "Cerrado típico",   "lat": -17.4653, "lon": -48.2089, "data": date(2024, 6, 14)},
    {"municipio": "Pires do Rio",  "estado": "GO", "localidade": "Estrada vicinal GO-153, km 12",                      "habitat": "Cerradão",         "lat": -17.3012, "lon": -48.2844, "data": date(2024, 7, 22)},
    {"municipio": "Ipameri",       "estado": "GO", "localidade": "Fazenda São Bento, margem do Rio Corumbá",            "habitat": "Campo sujo",       "lat": -17.7234, "lon": -48.1587, "data": date(2024, 8, 5)},
    {"municipio": "Orizona",       "estado": "GO", "localidade": "Parque Municipal da Serra dos Pirineus",              "habitat": "Campo rupestre",   "lat": -17.0453, "lon": -48.2978, "data": date(2024, 9, 10)},
    {"municipio": "Vianópolis",    "estado": "GO", "localidade": "Reserva particular - Sítio Boa Vista",                "habitat": "Vereda",           "lat": -16.7421, "lon": -48.5137, "data": date(2024, 10, 3)},
    {"municipio": "Palmelo",       "estado": "GO", "localidade": "APP Córrego Palmelo, área de preservação",            "habitat": "Mata ciliar",      "lat": -17.3387, "lon": -48.4002, "data": date(2024, 10, 28)},
    {"municipio": "Santa Cruz",    "estado": "GO", "localidade": "Rodovia BR-153, km 843, trecho de cerrado preservado","habitat": "Cerrado típico",   "lat": -17.2241, "lon": -48.6723, "data": date(2024, 11, 15)},
    {"municipio": "Cristianópolis","estado": "GO", "localidade": "Fazenda Bom Jesus, próximo ao lago artificial",       "habitat": "Campo limpo úmido","lat": -17.1983, "lon": -48.7011, "data": date(2024, 12, 2)},
    {"municipio": "Urutaí",        "estado": "GO", "localidade": "Campus IF Goiano - Urutaí, fragmento de cerradão N2", "habitat": "Cerradão",         "lat": -17.4662, "lon": -48.2101, "data": date(2025, 2, 18)},
    {"municipio": "Caldas Novas",  "estado": "GO", "localidade": "RPPN Parque das Emas, área de transição",             "habitat": "Campo sujo",       "lat": -17.7401, "lon": -48.6218, "data": date(2025, 3, 7)},
    {"municipio": "Rio Verde",     "estado": "GO", "localidade": "Trilha da Cachoeirinha, reserva legal",               "habitat": "Mata de galeria",  "lat": -17.8012, "lon": -50.9168, "data": date(2025, 4, 12)},
    {"municipio": "Cristalina",    "estado": "GO", "localidade": "Campos abertos próximos à Pedra Chapéu do Sol",       "habitat": "Campo limpo",      "lat": -16.7645, "lon": -47.6183, "data": date(2025, 5, 20)},
    {"municipio": "Alto Paraíso",  "estado": "GO", "localidade": "PNCV - Trilha dos Saltos, trecho rochoso",            "habitat": "Campo rupestre",   "lat": -14.1678, "lon": -47.7942, "data": date(2025, 6, 15)},
    {"municipio": "Pirenópolis",   "estado": "GO", "localidade": "Reserva Vargem Grande, acesso principal",             "habitat": "Cerrado stricto sensu","lat": -15.8456, "lon": -48.9200, "data": date(2025, 8, 1)},
    {"municipio": "Goiânia",       "estado": "GO", "localidade": "Parque Estadual Altamiro de Moura Pacheco",           "habitat": "Mata seca",        "lat": -16.5923, "lon": -49.1234, "data": date(2025, 9, 10)},
    {"municipio": "Morrinhos",     "estado": "GO", "localidade": "Campus IF Goiano - Morrinhos, área de preservação",   "habitat": "Cerradão",         "lat": -17.7321, "lon": -49.1023, "data": date(2025, 10, 5)},
    {"municipio": "Buriti Alegre", "estado": "GO", "localidade": "Margem do Lago das Brisas",                           "habitat": "Mata ciliar",      "lat": -18.1402, "lon": -49.1415, "data": date(2025, 11, 22)},
]

digitador = pessoas_criadas[1]  # Carlos Faria (Aluno)
coletores_pool = pessoas_criadas

for i, (dados_coleta, taxon) in enumerate(zip(coletas_dados, taxons_criados)):
    num_tombo = f"HIFG-{str(i+1).zfill(3)}"
    num_coleta = f"CEFL-{str(i+1).zfill(3)}"

    if Ocorrencia.objects.filter(num_tombo=num_tombo).exists():
        print(f"   ➜ Já existe: {num_tombo}")
        continue

    # Cria o registro de coleta
    reg_coleta = RegistroColeta.objects.create(
        data_coleta=dados_coleta['data'], pais="Brasil",
        estado_provincia=dados_coleta['estado'], municipio=dados_coleta['municipio'],
        localidade=dados_coleta['localidade'], habitat=dados_coleta['habitat'],
        latitude=dados_coleta['lat'], longitude=dados_coleta['lon'],
    )

    # Cria a ocorrência com status APROVADO para aparecer no acervo público
    ocorrencia = Ocorrencia.objects.create(
        num_tombo=num_tombo, num_coleta=num_coleta,
        id_digitador=digitador, id_colecao=colecao,
        id_registro_coleta=reg_coleta,
        status_submissao='Aprovado',
    )

    # Adiciona coletor principal
    OcorrenciaColetor.objects.create(
        ocorrencia=ocorrencia,
        pessoa=coletores_pool[i % len(coletores_pool)],
        e_principal=True
    )

    # Cria histórico de identificação (conecta com a taxonomia)
    historico = HistoricoIdentificacao.objects.create(
        data_identificacao=dados_coleta['data'],
        id_ocorrencia=ocorrencia,
        id_taxon=taxon,
        id_identificador=pessoas_criadas[0],  # Ana (Curadora)
    )

    # Aponta a identificação atual da ocorrência para este histórico
    ocorrencia.id_identificacao_atual = historico
    ocorrencia.save()

    print(f"   ✔ {num_tombo} | {taxon.nome_cientifico} | {dados_coleta['municipio']}")

# ==============================================================================
# 5. RESUMO
# ==============================================================================
print("\n[5/5] Resumo final:")
print(f"   Pessoas:         {Pessoa.objects.count()}")
print(f"   Taxonomias:      {Taxonomia.objects.count()}")
print(f"   Colecoes:        {Colecao.objects.count()}")
print(f"   Reg. Coletas:    {RegistroColeta.objects.count()}")
print(f"   Ocorrencias:     {Ocorrencia.objects.count()}")
print(f"   Ocorr. Aprovadas:{Ocorrencia.objects.filter(status_submissao='Aprovado').count()}")

print("\nDados criados com sucesso")
