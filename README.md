# Projeto Pedra Branca

Este repositório organiza o material de portfólio do projeto de análise geoespacial dos processos erosivos nas trilhas do Parque Estadual da Floresta da Pedra Branca (RJ), a partir do trabalho de conclusão de curso de Carine Brum de Oliveira Silva, defendido em 2025 pela UFRRJ.

**70 pontos de campo · 144 fotografias · 3 trilhas · PostgreSQL/PostGIS · QGIS · Python · Power BI**

## Contexto

O projeto tem como foco o monitoramento e a classificação de risco de erosão nas trilhas do Parque Estadual da Floresta da Pedra Branca, localizado na Região Metropolitana do Rio de Janeiro. A base original do estudo foi consolidada em levantamento de campo com identificação de 70 pontos distribuídos em três trilhas.

| Trilha | Nome | Pontos | Fotos |
|---|---|---|---|
| `T01` | Pau da Fome | 35 | 57 |
| `T02` | Pedra Negra | 15 | 35 |
| `T03` | Morro dos Caboclos | 20 | 52 |
| | **Total** | **70** | **144** |

## Origem dos dados

O material de origem foi herdado do TCC de geologia ambiental e reorganizado em estrutura de portfólio, com foco em:

- Banco de dados geoespacial PostgreSQL + PostGIS;
- Organização de camadas e layouts em QGIS;
- Análise estatística dos dados de campo;
- Dashboard em Power BI;
- Publicação em GitHub como repositório de projeto.

---

## Como abrir o projeto QGIS

O repositório oferece dois caminhos. O **banco PostgreSQL é a fonte de verdade** do projeto; o GeoPackage é uma cópia congelada dele, publicada para quem só quer abrir e ver.

| | Opção A — GeoPackage | Opção B — PostGIS |
|---|---|---|
| Arquivo | `Projeto_QGIS_Pedra_Branca_GeoPackage.qgz` | `Projeto_QGIS_Pedra_Branca.qgz` |
| Precisa instalar | nada além do QGIS | PostgreSQL + PostGIS |
| Para que serve | visualizar, conferir, apresentar | trabalhar nos dados, editar, consultar |

---

### Opção A — só visualizar (não precisa instalar nada)

Abra `Projeto_QGIS_Pedra_Branca_GeoPackage.qgz`, na raiz do repositório.

Os dados vêm de `03_QGIS/pedra_branca.gpkg` — arquivo único, já incluído no repositório, com as 10 camadas e a simbologia embutidas. Não é preciso configurar conexão nenhuma.

> O `.gpkg` é uma **fotografia** do banco no momento da exportação. Se o banco for corrigido depois, esta cópia não sabe disso. Em caso de divergência, vale o que está no PostgreSQL.

---

### Opção B — trabalhar com o banco (fonte de verdade)

As camadas vêm de um banco PostgreSQL local. Para o arquivo do QGIS abrir com os dados, é preciso restaurar o banco antes.

#### 1. Restaurar o banco

Requisitos: **PostgreSQL 14+** com a extensão **PostGIS**.

Crie o banco e habilite a extensão:

```sql
CREATE DATABASE projetopedrabranca;
```

Conectado ao banco recém-criado:

```sql
CREATE EXTENSION postgis;
```

Restaure o dump:

```
pg_restore -U postgres -d projetopedrabranca 02_Banco_de_Dados/projetopedrabranca.dump
```

#### 2. Criar a conexão no QGIS

Em **Camada → Adicionar Camada → Adicionar Camada PostGIS → Nova conexão**:

| Campo | Valor |
|---|---|
| Nome | `projetopedrabranca` |
| Host | `localhost` |
| Porta | `5432` |
| Banco de dados | `projetopedrabranca` |

> O **nome da conexão precisa ser idêntico**. Se for diferente, o QGIS pede o caminho de cada camada ao abrir o projeto.

#### 3. Abrir

Abra `Projeto_QGIS_Pedra_Branca.qgz`, na raiz do repositório.

---

### Fotografias — vale para as duas opções

Ao passar o mouse sobre um ponto, aparece um balão com os atributos e a lista de fotografias. Ao clicar, o formulário mostra as fotos em miniatura, com botão para abrir o arquivo. Para isso funcionar a camada tem que estar habilitada no QGIS.

As imagens são lidas de `06_Fotos_Campo/` por **caminho relativo**, o que funciona em qualquer sistema operacional — desde que a estrutura de pastas do repositório seja mantida.

## Scripts Python

Os scripts em `04_Python/` leem as credenciais do banco de um arquivo `.env` na raiz do projeto, que **não é versionado** por conter senha. Crie o seu:

```
PGHOST=localhost
PGPORT=5432
PGDATABASE=projetopedrabranca
PGUSER=postgres
PGPASSWORD=sua_senha
```

Dependências:

```
pip install pandas sqlalchemy psycopg2-binary python-dotenv matplotlib seaborn jupyter
```

---

## Estrutura do projeto

```text
Projeto_Pedra_Branca/
├── 02_Banco_de_Dados      Scripts SQL e dump do banco
├── 03_QGIS                Camadas, layouts e pedra_branca.gpkg
├── 04_Python              Scripts de automação e análise
├── 05_PowerBI             Dashboard
├── 06_Fotos_Campo         144 fotografias, organizadas por trilha
├── Projeto_QGIS_Pedra_Branca.qgz              lê do PostGIS
└── Projeto_QGIS_Pedra_Branca_GeoPackage.qgz   lê do .gpkg
```

Os dois arquivos de projeto do QGIS ficam na **raiz**, para que os caminhos relativos das fotografias partam da mesma pasta que engloba todas as demais.

## Modelo de dados

```
projetopedrabranca
├── area_parque                    limite da unidade de conservação (POLYGON)
├── trilha_1_pau_da_fome           (LINESTRING)
├── trilha_2_pedra_negra           (LINESTRING)
├── trilha_3_morro_dos_caboclos    (LINESTRING)
├── pontos_trilha_1                35 registros (POINT)
├── pontos_trilha_2                15 registros (POINT)
├── pontos_trilha_3                20 registros (POINT)
├── fotos_trilha_1_stg             57 registros, 1:N com pontos_trilha_1
├── fotos_trilha_2_stg             35 registros, 1:N com pontos_trilha_2
└── fotos_trilha_3_stg             52 registros, 1:N com pontos_trilha_3
```

As fotografias ligam-se aos pontos pelo campo `id_ponto`, dentro de cada trilha. As views `v_pontos_trilha_1/2/3` entregam ponto e fotos numa consulta só, para uso em análise e no dashboard.

## Stack principal

- PostgreSQL / PostGIS
- QGIS
- Python
- Power BI
- Git / GitHub

## Dados e convenções

- Sistema de referência: SIRGAS 2000 / UTM zona 23S (EPSG:31983);
- Nomenclatura de pontos: T1P001 a T3P020;
- Identificação de fotos: padrão `P<NNN>_F<NNN>.png`, onde `P` é o número do ponto dentro da trilha e `F` o identificador global da foto;
- Caminho das fotos no banco: relativo à raiz do projeto, com barra normal (`06_Fotos_Campo/Trilha_01/P001_F001.png`);
- Escala de perigo: 1 a 5, de Muito Baixo a Muito Alto.

## Objetivo

Reconstituir um fluxo de trabalho geoespacial, conectando dados de campo, banco de dados, análise espacial, visualização e dashboard em uma solução reproduzível.

## Repositório

Este repositório tem caráter público e acadêmico. A publicação da versão completa pode incluir amostras e materiais curados, de forma a respeitar o volume e a origem dos dados.

## Licença

Os dados de origem são de natureza acadêmica e precisam ser tratados com licença e crédito adequados ao material do TCC e da instituição.
