"""
Vínculo automático das fotografias.

Cruza os arquivos de 06_Fotos_Campo/ com as tabelas fotos_trilha_N_stg
do banco pedra_branca, reporta divergências e (opcionalmente) grava a
coluna `caminho` com o caminho relativo à raiz do projeto.

Uso:
    python vincular_fotografias.py            # só confere, não altera nada
    python vincular_fotografias.py --aplicar  # confere e grava o caminho
"""

import os
import re
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

# --------------------------------------------------------------------------
# Configuração
# --------------------------------------------------------------------------

# Scripts/ -> 04_Python/ -> raiz do projeto
RAIZ_PROJETO = Path(__file__).resolve().parents[2]
PASTA_FOTOS = RAIZ_PROJETO / "06_Fotos_Campo"

TRILHAS = {
    "Trilha_01": {"prefixo": "T1", "tabela": "fotos_trilha_1_stg"},
    "Trilha_02": {"prefixo": "T2", "tabela": "fotos_trilha_2_stg"},
    "Trilha_03": {"prefixo": "T3", "tabela": "fotos_trilha_3_stg"},
}

# P001_F001.png -> ('P001', 'F001')
PADRAO_ARQUIVO = re.compile(r"^(P\d{3})_(F\d{3})\.png$", re.IGNORECASE)


def conectar():
    """Monta a conexão a partir do .env da raiz do projeto."""
    load_dotenv(RAIZ_PROJETO / ".env")
    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST", "localhost"),
        port=int(os.getenv("PGPORT", 5432)),
        database=os.getenv("PGDATABASE", "pedra_branca"),
    )
    return create_engine(url)


# --------------------------------------------------------------------------
# Leitura
# --------------------------------------------------------------------------

def ler_disco():
    """Percorre 06_Fotos_Campo/ e devolve o que existe em disco."""
    registros = []
    fora_do_padrao = []

    for pasta, cfg in TRILHAS.items():
        diretorio = PASTA_FOTOS / pasta
        if not diretorio.is_dir():
            print(f"  ! pasta não encontrada: {diretorio}")
            continue

        for arquivo in sorted(diretorio.iterdir()):
            if not arquivo.is_file():
                continue

            achado = PADRAO_ARQUIVO.match(arquivo.name)
            if not achado:
                fora_do_padrao.append(f"{pasta}/{arquivo.name}")
                continue

            ponto, foto = achado.groups()
            registros.append({
                "id_foto": foto.upper(),
                "arquivo_disco": arquivo.name,
                "pasta_disco": pasta,
                "id_ponto_disco": cfg["prefixo"] + ponto.upper(),
                "caminho_correto": f"06_Fotos_Campo/{pasta}/{arquivo.name}",
            })

    return pd.DataFrame(registros), fora_do_padrao


def ler_banco(engine):
    """Lê as três tabelas de fotos e empilha num DataFrame só."""
    partes = []
    for pasta, cfg in TRILHAS.items():
        consulta = f"""
            SELECT id_foto, id_ponto, arquivo, caminho
            FROM public.{cfg['tabela']}
        """
        parte = pd.read_sql(consulta, engine)
        parte["tabela"] = cfg["tabela"]
        parte["pasta_esperada"] = pasta
        partes.append(parte)

    banco = pd.concat(partes, ignore_index=True)
    banco["id_foto"] = banco["id_foto"].str.strip().str.upper()
    banco["id_ponto"] = banco["id_ponto"].str.strip().str.upper()
    return banco


# --------------------------------------------------------------------------
# Conferência
# --------------------------------------------------------------------------

def relatar(disco, banco, fora_do_padrao):
    """Imprime o relatório e devolve o número de problemas encontrados."""
    cruzado = disco.merge(banco, on="id_foto", how="outer", indicator=True)
    problemas = 0

    def bloco(titulo, linhas):
        nonlocal problemas
        print(f"\n{titulo}")
        print("-" * len(titulo))
        if not linhas:
            print("  nenhum")
        else:
            problemas += len(linhas)
            for linha in linhas:
                print(f"  - {linha}")

    bloco(
        "1. Arquivos fora do padrao de nome",
        fora_do_padrao,
    )

    bloco(
        "2. Fotos em disco sem registro no banco",
        [f"{r.pasta_disco}/{r.arquivo_disco}"
         for r in cruzado[cruzado._merge == "left_only"].itertuples()],
    )

    bloco(
        "3. Registros no banco sem arquivo em disco",
        [f"{r.tabela}: {r.id_foto} (ponto {r.id_ponto}, arquivo '{r.arquivo}')"
         for r in cruzado[cruzado._merge == "right_only"].itertuples()],
    )

    ambos = cruzado[cruzado._merge == "both"]

    bloco(
        "4. Prefixo do arquivo nao corresponde ao id_ponto do banco",
        [f"{r.arquivo_disco} sugere {r.id_ponto_disco}, "
         f"mas o banco registra {r.id_ponto}"
         for r in ambos[ambos.id_ponto_disco != ambos.id_ponto].itertuples()],
    )

    bloco(
        "5. Foto gravada em pasta de trilha diferente da do seu ponto",
        [f"{r.arquivo_disco} esta em {r.pasta_disco}, "
         f"mas o ponto {r.id_ponto} pertence a {r.pasta_esperada}"
         for r in ambos[ambos.pasta_disco != ambos.pasta_esperada].itertuples()],
    )

    bloco(
        "6. Coluna 'arquivo' diferente do nome real do arquivo",
        [f"{r.tabela}: banco diz '{r.arquivo}', disco tem '{r.arquivo_disco}'"
         for r in ambos[ambos.arquivo != ambos.arquivo_disco].itertuples()],
    )

    return ambos, problemas


# --------------------------------------------------------------------------
# Gravação
# --------------------------------------------------------------------------

def aplicar_caminhos(engine, ambos):
    """Grava a coluna `caminho` apenas onde ela esta diferente do correto."""
    pendentes = ambos[ambos.caminho != ambos.caminho_correto]

    if pendentes.empty:
        print("\nNada a atualizar - todos os caminhos ja estao corretos.")
        return

    print(f"\nAtualizando {len(pendentes)} registro(s)...")
    with engine.begin() as conexao:
        for r in pendentes.itertuples():
            conexao.execute(
                text(f"UPDATE public.{r.tabela} "
                     f"SET caminho = :caminho WHERE id_foto = :id_foto"),
                {"caminho": r.caminho_correto, "id_foto": r.id_foto},
            )
    print("Concluido.")


# --------------------------------------------------------------------------

def main():
    aplicar = "--aplicar" in sys.argv

    print(f"Raiz do projeto: {RAIZ_PROJETO}")
    print(f"Pasta de fotos:  {PASTA_FOTOS}")

    disco, fora_do_padrao = ler_disco()
    engine = conectar()
    banco = ler_banco(engine)

    print(f"\nFotos em disco: {len(disco)}")
    print(f"Registros no banco: {len(banco)}")

    ambos, problemas = relatar(disco, banco, fora_do_padrao)

    print(f"\n{'=' * 60}")
    print(f"Total de divergencias: {problemas}")

    if aplicar:
        aplicar_caminhos(engine, ambos)
    else:
        print("Modo confererencia. Para gravar os caminhos, rode com --aplicar")


if __name__ == "__main__":
    main()
