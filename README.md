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
pg_restore -U postgres -d projetopedrabranca 02_Banco_de_Dados/projetopedrabranca.dump.sql
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

## Análise em Python

O notebook `04_Python/Notebook/analise_pedra_branca.ipynb` lê os 70 pontos direto do PostGIS e produz **8 figuras** e **18 tabelas** em `05_PowerBI/`.

O trabalho central é transformar texto livre de campo em categorias comparáveis. Os campos `sinais_erosao` e `obstaculos_riscos` foram preenchidos em prosa — 22 descrições distintas de erosão, 43 de evidências de instabilidade. Regras de reconhecimento por padrão textual, ordenadas da mais específica para a mais genérica, convertem isso em classes, sem nenhuma classificação manual: cada categoria vem de uma regra explícita no código, que qualquer pessoa pode ler, contestar ou reexecutar.

Todas as colunas derivadas **nascem no notebook** — não existem no banco. É por isso que o dashboard lê dos CSVs e não direto do PostgreSQL: a regra fica versionada num lugar só, em vez de duplicada em DAX.

O produto principal é o `05_PowerBI/Tabelas/pontos_completo.csv`: 70 linhas × 35 colunas, reunindo os atributos de campo, as classificações derivadas e as coordenadas em graus decimais. As demais 17 tabelas são cruzamentos já somados, para conferência e para o relatório escrito.

## Dashboard (Power BI)

`05_PowerBI/Dashboard/Pedra_Branca.pbix` — quatro páginas, alimentadas por `pontos_completo.csv` e `fotos_completo.csv`.

| Página | Pergunta que responde |
|---|---|
| **Visão geral** | Qual é o tamanho e o resultado do levantamento? |
| **Mapa de perigo** | Onde estão os pontos críticos? |
| **O que sustenta a nota de perigo** | Por que estes pontos são críticos? |
| **Terreno e processos erosivos** | Em que condições a erosão se instala — e ela gradua o perigo? |

A página de visão geral basta sozinha: quem abrir e não clicar em mais nada já sai sabendo o tamanho do levantamento e o achado principal. As outras três são profundidade.

No mapa, o tamanho do marcador cresce com o nível de perigo, além da cor — dois canais para a mesma informação. Selecionar um ponto abre os atributos e a fotografia daquele trecho, servidas por URL a partir de `06_Fotos_Campo/`.

A escala de perigo (azul → verde → amarelo → laranja → vermelho) é a mesma dos mapas do QGIS, para que carta e painel se leiam juntos.

## Principais achados

**Um terço da amostra é crítica.** 23 dos 70 pontos foram classificados em perigo 4 ou 5.

**O perigo mora na combinação, não em cada fator isolado.**

| Origem | Pontos | Perigo médio | % críticos |
|---|---|---|---|
| Declividade alta **+** instabilidade | 13 | 4,38 | **76,9%** |
| Evidências de instabilidade | 30 | 3,23 | 36,7% |
| Só declividade alta | 6 | 2,67 | 16,7% |
| Sem evidência registrada | 21 | 2,05 | **4,8%** |

Declividade alta sozinha quase não agrava; instabilidade do terreno pesa mais; juntas, três em cada quatro pontos viram críticos.

**Trecho sem nenhum registro é trecho seguro.** Cruzando as duas colunas de texto livre, 11 pontos não têm registro em nenhuma delas — e **nenhum é crítico**, com perigo médio 1,64. Os 59 com algum registro têm média 3,31 e concentram os 23 críticos.

**Árvore derrubada é efeito, não causa.** Separando os tipos de evidência, pontos com instabilidade do terreno registram 56,2% de críticos; pontos onde só há árvore caída, 16,7%. A queda é consequência do solapamento, e sozinha não indica trecho perigoso.

## Estrutura do projeto

```text
Projeto_Pedra_Branca/
├── 02_Banco_de_Dados      Scripts SQL e dump do banco
├── 03_QGIS                Camadas, layouts e pedra_branca.gpkg
├── 04_Python
│   ├── Notebook           analise_pedra_branca.ipynb
│   └── Scripts            vínculo automático das fotografias
├── 05_PowerBI
│   ├── Dashboard          Pedra_Branca.pbix e tema_pedra_branca.json
│   ├── Imagens            8 figuras geradas pelo notebook
│   └── Tabelas            18 tabelas geradas pelo notebook
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
- Escala de perigo: 1 a 5, de Muito Baixo a Muito Alto;
- O `pontos_completo.csv` carrega `longitude` e `latitude` em **graus decimais (EPSG:4326)**, calculadas na consulta com `ST_Transform` apenas para o visual de mapa do Power BI, que não entende sistema projetado. A geometria do banco permanece em EPSG:31983.

## Objetivo

Reconstituir um fluxo de trabalho geoespacial, conectando dados de campo, banco de dados, análise espacial, visualização e dashboard em uma solução reproduzível.

## Repositório

Este repositório tem caráter público e acadêmico. A publicação da versão completa pode incluir amostras e materiais curados, de forma a respeitar o volume e a origem dos dados.

## Licença

Os dados de origem são de natureza acadêmica e precisam ser tratados com licença e crédito adequados ao material do TCC e da instituição.
