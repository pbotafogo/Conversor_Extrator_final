import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
import datetime
import gzip
import os
dt_arq = datetime.datetime.now().strftime("%Y-%m-%d_%H_%m")

dados_campos = {
    'GR-MATRICULA': 'siape',
    'IT-NU-IDEN-SERV-ORIGEM': 'siapecad',
    'IT-NO-SERVIDOR': 'nome',
    'IT-DA-NASCIMENTO': 'dt_nasc',
    'IT-NU-CPF': 'cpf',
    'IT-NU-PIS-PASEP': 'pis_pasep',
    'IT-IN-SUPRESSAO-PAGAMENTO': 'id_supr_pag',
    'IT-CO-SITUACAO-SERVIDOR': 'sit_serv',
    'IT-CO-GRUPO-OCOR-AFASTAMENTO': 'oco_afast_grp',
    'IT-DA-INICIO-OCOR-AFASTAMENTO': 'oco_afast_dt_ini',
    'IT-DA-TERMINO-OCOR-AFASTAMENTO': 'oco_afast_dt_term',
    'IT-CO-GRUPO-OCOR-EXCLUSAO': 'oco_exclu_grp',
    'IT-CO-UORG-LOTACAO-SERVIDOR': 'lot_uo',
    'IT-CO-ORGAO-REQUISITANTE': 'org_requisitante',
    'IT-CO-UORG-LOCALIZACAO-SERV': 'local_uo',
    'IT-CO-SEXO': 'sexo',
    'IT-DA-CADASTRAMENTO-SERVIDOR': 'dt_cad_serv',
    'IT-SG-REGIME-JURIDICO': 'sig_reg_jur',
    'IT-CO-OCOR-EXCLUSAO': 'oco_exclu_oco',
    'IT-DA-OCOR-EXCLUSAO-SERV': 'oco_exclu_dt',
    'IT-CO-GRUPO-OCOR-INGR-ORGAO': 'oco_ingorg_grp',
    'IT-CO-OCOR-INGR-ORGAO': 'oco_ingorg_oco',
    'IT-DA-OCOR-INGR-ORGAO-SERV': 'oco_ingorg_dt',
    'IT-SG-FUNCAO': 'funcao_sig',
    'IT-CO-NIVEL-FUNCAO': 'funcao_cod_nivel',
    'IT-SG-ESCOLARIDADE-FUNCAO': 'funcao_escol',
    'IT-DA-INGRESSO-FUNCAO': 'funcao_dt_ing',
    'IT-DA-SAIDA-FUNCAO': 'funcao_dt_saida',
    'IT-CO-UORG-FUNCAO': 'funcao_uo',
    'IT-SG-NOVA-FUNCAO': 'nova_funcao_sig',
    'IT-CO-NIVEL-NOVA-FUNCAO': 'nova_funcao_cod_nivel',
    'IT-SG-ESCOLARIDADE-NOVA-FUNCAO': 'nova_funcao_escol',
    'IT-DA-INGRESSO-NOVA-FUNCAO': 'nova_funcao_dt_ing',
    'IT-DA-SAIDA-NOVA-FUNCAO': 'nova_funcao_dt_saida',
    'IT-CO-UORG-NOVA-FUNCAO': 'nova_funcao_uo',
    'IT-CO-JORNADA-TRABALHO': 'jorn_trabalho',
    'IT-IDENTIFICACAO-UPAG': 'upag',
    'IT-SG-UF-UPAG': 'upag_uf',
    'IT-CO-UORG-EXERCICIO-SERV': 'uo_exerc',
    'IT-CO-GRUPO-POSTO-ETG': 'posto_etg_grp',
    'IT-CO-POSTO-ETG': 'posto_etg_cod',
    'GR-MATRICULA-SERV-DISPONIVEL': 'siape',
    'IT-CO-COR-ORIGEM-ETNICA': 'cor_cod',
    'IT-SG-GRUPO-SANGUINEO': 'fator_rh_grp',
    'IT-SG-FATOR-RH': 'fator_rh_cod',
    'IT-CO-GRUPO-DEFICIENCIA-FISICA': 'def_grp',
    'IT-CO-DEFICIENCIA-FISICA': 'def_cod',
    'IT-CO-GRUPO-OCOR-INATIVIDADE': 'oco_inat_grp',
    'IT-DA-SAIDA-CARGO-EMPREGO': 'cargemp_dt_saida',
    'IT-CO-ATIVIDADE-FUNCAO': 'funcao_ativ',
    'IT-CO-ATIVIDADE-NOVA-FUNCAO': 'nova_funcao_ativ',
    'IT-CO-ORGAO-ORIGEM': 'mud_org_org_origem',
    'IT-CO-UORG-EMISSAO': 'uorg_cod',
    'IT-SG-UF-UORG-EMISSAO': 'uorg_uf',
    'IT-DA-OBITO': 'reg_obito_dt',
    'IT-IN-STATUS-REGISTRO-TABELA': 'status_siape',
    'IT-CO-ORGAO': 'cod_orgao',
    'IT-NO-ORGAO': 'nm_orgao',
    'IT-SG-ORGAO': 'sg_orgao',
    'IT-CO-NATUREZA-JURIDICA': 'cod_nat_jur',
    'IT-CO-ORGAO-ATUAL': 'cod_org_atu',
    'IT-CO-ORGAO-VINCULACAO': 'cod_org_vinc',
    'IT-IN-ORGAO-SIAPE': 'in_org_siape',
    'IT-CO-ORGAO-SIORG': 'cod_org_SIORG',
    'IT-CO-VAGA': 'cod_vaga',
    'IT-CO-UNIDADE-ORGANIZACIONAL': 'cod_vaga_uo',
    'IT-CO-EXCLUSAO-VAGA': 'cod_vaga_exc',
    'IT-CO-GRUPO-CARGO-EMPREGO': 'cod_vaga_grp_cargem',
    'IT-CO-CARGO-EMPREGO': 'cod_vaga_cargem',
    'IT-CO-ORIGEM-VAGA': 'cod_ori_vaga',
    'IT-NO-ORIGEM-VAGA': 'nome_ori_vaga',
    'IT-DA-OCUPACAO-VAGA': 'dt_ocup_vaga',
    'IT-CO-AFASTAMENTO': 'COD_AFAST',
    'IT-SG-AFASTAMENTO': 'SG_AFAST',
    'IT-NO-AFASTAMENTO': 'DEN_AFAST',
    'IT-TP-AFASTAMENTO': 'TP_AFAST',
    'IT-NU-MAXIMO-DIAS-AFASTAMENTO': 'NU_MAX_DIAS_AFAST',
    'IT-CO-ABRANGENCIA-AFASTAMENTO': 'CO_ABR_ABRANGENCIA_AFAST',
    'GR-SITUACAO-FUNCIONAL(1)': 'GRP_SITFUN_AFAST',
    'IT-CO-OCOR-INATIVIDADE': 'oco_inat_oco',
    'IT-DA-OCOR-INATIVIDADE-SERV': 'oco_inat_dt',
    'IT-DA-OCUPACAO-CARGO-EMPREGO': 'dt_ocu_cargem',
    'GR-IDENTIFICACAO-UORG': 'lot_CodUORG_gr',
    'IT-NO-UNIDADE-ORGANIZACIONAL': 'lot_nUORG',
    'IT-SG-UNIDADE-ORGANIZACIONAL': 'lot_SiglaUORG',
    'IT-SG-UF': 'lot_UF',
    'GR-CEST-IDENTIFICACAO-UPAG': 'lot_CodUPAG',
    'IT-CO-CEST-UPAG-HIST': 'lot_CodUPAG_hist',
    'IT-CO-UNIDADE-GESTORA': 'lot_CodUG_UORG',
    'IT-CO-ORGAO-ATUAL-UORG': 'lot_CodOrg_UORG',
    'IT-CO-UORG-ATUAL': 'lot_CodUORG',
    'IT-CO-UG-PAGADORA': 'lot_CodUG_PAG',
    'IT-CO-GESTAO-PAGADORA': 'lot_CodGESTAO_PAG',
    'IT-CO-UORG-VINCULACAO': 'lot_UORG_PAI',
    'IT-CO-UG-RESPONSAVEL': 'lot_CodUG_RESP',
    'IT-CO-AREA-ATUACAO-UORG': 'cod_area_atua',
    'IT-NU-ATIVIDADE-PRINCIPAL': 'lot_nm_ativ_princ',
    'IT-CO-MUNICIPIO-UORG': 'lot_CodMunic',
    'IT-CO-UORG-SIORG': 'lot_CodUORG_SIORG'}


engine = create_engine("sqlite:///Banco_Rotinas.db")
with engine.connect() as connection:
    print("Conectado com sucesso")

#CONVERSÃO DOS ARQUIVOS GERADOS PELO EXTRATOR DE DADOS ESCREVER FLUXO

def read_gz(arquivo):
    linhas = []
    with gzip.open(arquivo,'r') as fin:
        for line in fin:
            linhas.append(line.decode("utf-8"))
            #linhas.append(str(line.decode("utf-8")).replace("\\r\\n'","").replace("b'",""))
    return linhas
        
# Função para conversão de datas para datetime:
def converte_data(data_string):
    try:
        d, m, a = data_string[0:2], data_string[2:4], data_string[4:9]
        data = datetime.date(int(a), int(m), int(d))
        return data
    except:
        return datetime.date(1, 1, 1)

def substituir_data_invalida(valor):
    if valor == datetime.date(1, 1, 1):
        return pd.NaT
    return valor

def converte_data_invert(data_string):
    try:
        a, m, d = data_string[0:4], data_string[4:6], data_string[6:9]
        data = datetime.date(int(a), int(m), int(d))
        return data
    except:
        return datetime.date(1, 1, 1)
        
def converter_extrator(referencia, dados, nome):
    texto = read_gz(referencia)
    lista = []
    colunas = []

    colunas.append("dt_atu")
    for i in range(len(texto)):
        if i == 0:
            col = texto[0][:40].strip()
            tipo = texto[0][40:41].strip()
            tam = int(texto[0][43:46].strip())
            ini = 0
            fim = tam
            lista.append([col,tipo,tam,ini,fim])
            try:
                colunas.append(dados_campos[col])
            except:
                colunas.append(col.replace("-","_"))
        else:
            col = texto[i][:40].strip()
            tipo = texto[i][40:41].strip()
            tam = int(texto[i][43:46].strip())
            ini = lista[-1][-1]
            fim = ini+tam
            lista.append([col,tipo,tam,ini,fim])
            try:
                colunas.append(dados_campos[col])
            except:
                colunas.append(col.replace("-","_"))

    dados_lista = read_gz(dados)

    dados_final = []
    timestamp = datetime.datetime.now()
    data = timestamp.date()
    #print(compet, converte_data(compet), converte_data_invert(compet))
    for linha in dados_lista:
        linha_dados = []
        linha_dados.append(data)
        for linha_lista in lista:
            ini = linha_lista[-2]
            #print("ini", ini)
            fim = linha_lista[-1]
            col = linha_lista[0]
            #print("fim", fim)
            if col[3:5] == "DA":
                linha_dados.append(converte_data_invert(linha[ini:fim].strip()))
            elif col[3:5] == "QT":
                linha_dados.append(int(linha[ini:fim].strip()))
            else:
                linha_dados.append(linha[ini:fim].strip())
        dados_final.append(linha_dados)
    df = pd.DataFrame(dados_final,columns=colunas)
    try:
        df = df.applymap(substituir_data_invalida)
    except:
        None
    try:    
        df['siape'] = df['siape'].astype(str).str.slice(start=5, stop=12)
    except:
        None
    try:
        df['upag'] = df['upag'].astype(str).str.slice(start=5, stop=14)
    except:
        None
    try:
        df['lot_CodUORG_gr'] = df['lot_CodUORG_gr'].astype(str).str.slice(start=5, stop=14)
    except:
        None
    try:
        df['lot_CodUPAG'] = df['lot_CodUPAG'].astype(str).str.slice(start=5, stop=14)
    except:
        None
    try:
        df['lot_UORG_PAI'] = df['lot_UORG_PAI'].astype(str).str.slice(start=5, stop=14)
    except:
        None
    nome_arquivo = os.path.splitext(os.path.basename(nome))[0]
    #df.to_sql(nome_arquivo, con=engine, index=False, if_exists="replace")
    df.to_csv(f"{nome}_{dt_arq}.csv", index=False)
    print(f"Relatório {nome_arquivo} concluído")
    return dados_final, lista



def getDirDetails(path=os.getcwd()):
    fileList = []

    pathExists = os.path.exists(path)
    isFile = os.path.isfile(path)
    isDir = os.path.isdir(path)
    arquivos = []
    if pathExists and isDir:
        for root, dirs, files in os.walk(path):
            for file in files:
                arquivos.append({file.replace(".gz",""): os.path.join(root, file)})
    return arquivos




arq = getDirDetails(r"D:\Users\DGPI\Python_Scripts\EXTRATOR_DADOS\FLUXO_MENSAL\Novos")
for linha in arq:
    for nome in linha:
        if nome.split(".")[-1] == "REF":
            ref = linha[nome]
            dados = linha[nome].replace('.REF.gz','.TXT.gz')
            arquivo = linha[nome].replace('.REF.gz','')
            converter_extrator(ref, dados, arquivo)

