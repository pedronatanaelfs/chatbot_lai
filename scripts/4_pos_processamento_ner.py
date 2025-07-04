import pandas as pd
import os

def limpar_entidades(df):
    # Conjunto ampliado de entidades e rótulos genéricos para descartar
    descartar = {
         # Estrutura e marcadores legais
        "SS", "Lei", "lei", "Leis", "Art.", "PREAMBULO", "Vide Lei", "Vigencia", "Vigencia)", "Redacao dada pela Lei",
        "Art. 4o", "Lei: CAPITULO I DISPOSICOES GERAIS", "Lei: I", "Lei; II",
        "ARTIGO_4]", "ARTIGO_116",
        "Secao II", "Secao III Da Protecao", "Secao IV", "Secao V",
        "Capitulo", "Capitulo IV do Titulo IV da Lei",

        # Artigos e capítulos
        *{f"ARTIGO_{i}" for i in range(1, 48)},
        "CAPITULO II",
        "CAPITULO III DO PROCEDIMENTO DE ACESSO",
        "CAPITULO IV DAS RESTRICOES DE ACESSO",
        "CAPITULO V DAS RESPONSABILIDADES",
        "Capitulo IV do Titulo IV da Lei",
        "Secao II do Capitulo III",

        # Incisos e termos legais repetidos
        "inciso XXXIII", "inciso II do SS 3o", "inciso I", "inciso II",
        "inciso III", "inciso IV", "inciso V", "Pais; V",
        "inciso I", "inciso II", "inciso III", "inciso IV", "inciso V", "inciso II do",
        "Mensagem de veto Vigencia Regulamento Regula", "tornar-se-a", "modificacoes", "Grau", "Prazos de Sigilo",
        "Grupo-Direcao", "ma-fe", "Das Informacoes Pessoais",

        # Entradas truncadas ou irrelevantes
        "Pais; V", "infracoes", "Ministros", "Republica", "Estara"

        # Ruídos e termos irrelevantes
        "Mensagem de veto Vigencia Regulamento Regula",
        "tornar-se-a", "modificacoes", "Grau", "Prazos de Sigilo",
        "Grupo-Direcao", "ma-fe", "Das Informacoes Pessoais"
    }

    # Filtragem por nome
    df = df[~df["ENTIDADE"].isin(descartar)]

    # Remover entidades muito curtas ou vazias
    df = df[df["ENTIDADE"].notnull() & df["ENTIDADE"].str.strip().ne("")]
    df = df[df["ENTIDADE"].str.len() > 3]

    # Correção de rótulos problemáticos ou mal atribuídos
    correcoes_label = {
        "Presidencia da Republica": "ORG",
        "Casa Civil Subchefia para Assuntos Juridicos LEI": "ORG",
        "Controladoria-Geral da Uniao": "ORG",
        "Comissao Mista de Reavaliacao de Informacoes": "ORG",
        "Congresso Nacional": "ORG",
        "Poder Executivo Federal": "ORG",
        "Poder Executivo": "ORG",
        "Poder Judiciario": "ORG",
        "Ministerio das Relacoes Exteriores": "ORG",
        "Gabinete de Seguranca Institucional da Presidencia da Republica": "ORG",
        "Decreto Legislativo": "ORG",
        "Assessoramento Superiores": "ORG",
        "SS 2o": "O",
        "SS 1o": "O",
        "SS 5o": "O",
        "SS 3o Regulamento": "O",

        # Pessoas
        "Presidente da Republica": "PER",
        "Presidente": "PER",
        "Vice-Presidente da Republica": "PER",

        # Localidades
        "Estados": "LOC",
        "Municipios": "LOC",
        "Distrito Federal": "LOC",
        "Republica Federativa do Brasil": "LOC",

        # Legislação
        "Lei de Responsabilidade Fiscal": "LEGISLACAO",

        # Ruídos sem rótulo útil
        "administracao": "O",
        "solicitacoes": "O",
        "ARTIGO_3": "O"
    }

    # Aplicar correções
    df["LABEL"] = df.apply(lambda row: correcoes_label.get(row["ENTIDADE"], row["LABEL"]), axis=1)

    # Remover rótulos marcados como "O" (omitidos)
    df = df[df["LABEL"] != "O"]

    # Eliminar duplicações
    df = df.drop_duplicates(subset=["ENTIDADE", "LABEL"])

    return df

def main():
    # Garantir que o diretório data/processed existe
    os.makedirs("data/processed", exist_ok=True)
    
    print("[*] Lendo arquivo 'entidades_ner.txt'...")
    df = pd.read_csv("data/processed/entidades_ner.txt", sep="\t")

    print("[*] Iniciando limpeza e normalização das entidades...")
    df_limpo = limpar_entidades(df)

    print("[*] Salvando entidades filtradas...")
    df_limpo.to_csv("data/processed/entidades_filtradas.txt", sep="\t", index=False)

    print("[*] Gerando ranking de frequência...")
    freq = df_limpo["ENTIDADE"].value_counts().reset_index()
    freq.columns = ["ENTIDADE", "FREQUENCIA"]
    freq.to_csv("data/processed/entidades_frequentes.csv", index=False)

    print("[*] Salvando versão final com correções...")
    df_limpo.to_csv("data/processed/entidades_corrigidas.csv", index=False)

    print("[✓] Pós-processamento concluído com sucesso!")

if __name__ == "__main__":
    main()
