# Projeto Pedra Branca

Este repositório organiza o material de portfólio do projeto de análise geoespacial dos processos erosivos nas trilhas do Parque Estadual da Floresta da Pedra Branca (RJ), a partir do trabalho de conclusão de curso de Carine Brum de Oliveira Silva, defendido em 2025 pela UFRRJ.

## Contexto

O projeto tem como foco o monitoramento e a classificação de risco de erosão nas trilhas do Parque Estadual da Floresta da Pedra Branca, localizado na Região Metropolitana do Rio de Janeiro. A base original do estudo foi consolidada em levantamento de campo com identificação de 70 pontos distribuídos em três trilhas.

## Origem dos dados

O material de origem foi herdado do TCC de geologia ambiental e reorganizado em estrutura de portfólio, com foco em:

- Banco de dados geoespacial PostgreSQL + PostGIS;
- Organização de camadas e layouts em QGIS;
- Automação em Python para vinculação entre pontos e fotografias;
- Análise estatística dos dados de campo;
- Dashboard em Power BI;
- Publicação em GitHub como repositório de projeto.

## Estrutura do projeto

```text
Projeto_Pedra_Branca/
├── 00_Documentação
├── 01_Dados_Brutos
├── 02_Banco_de_Dados
├── 03_QGIS
├── 04_Python
├── 05_PowerBI
└── 06_Fotos_Campo
```

## Stack principal

- PostgreSQL / PostGIS
- QGIS
- Python
- Power BI
- Git / GitHub

## Dados e convenções

- Sistema de referência: SIRGAS 2000 / UTM zona 23S (EPSG:31983);
- Nomenclatura de pontos: T1P001 a T3P020;
- Identificação de fotos: padrão P<NNN>_F<NNN>.png;
- Escala de perigo: 1 a 5.

## Objetivo

Reconstituir um fluxo de trabalho geoespacial, conectando dados de campo, banco de dados, análise espacial, visualização e dashboard em uma solução reproduzível.

## Repositório

Este repositório tem caráter público e acadêmico. A publicação da versão completa pode incluir amostras e materiais curados, de forma a respeitar o volume e a origem dos dados.

## Licença

Os dados de origem são de natureza acadêmica e precisam ser tratados com licença e crédito adequados ao material do TCC e da instituição.
