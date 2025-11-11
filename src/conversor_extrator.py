import datetime
import gzip
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

import pandas as pd
from sqlalchemy import create_engine

dt_arq = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M")

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
    'IT-CO-UORG-SIORG': 'lot_CodUORG_SIORG'
}


# ============== FUNÇÕES CORE ==============

def read_gz(arquivo):
    """Lê arquivo .gz e retorna linhas decodificadas."""
    linhas = []
    with gzip.open(arquivo, 'r') as fin:
        for line in fin:
            linhas.append(line.decode("utf-8"))
    return linhas


def converte_data(data_string):
    """Converte string de data formato DDMMAAAA para datetime."""
    try:
        d, m, a = data_string[0:2], data_string[2:4], data_string[4:9]
        data = datetime.date(int(a), int(m), int(d))
        return data
    except:
        return datetime.date(1, 1, 1)


def substituir_data_invalida(valor):
    """Substitui datas inválidas por NaT."""
    if valor == datetime.date(1, 1, 1):
        return pd.NaT
    return valor


def converte_data_invert(data_string):
    """Converte string de data formato AAAAMMDD para datetime."""
    try:
        a, m, d = data_string[0:4], data_string[4:6], data_string[6:9]
        data = datetime.date(int(a), int(m), int(d))
        return data
    except:
        return datetime.date(1, 1, 1)


def converter_extrator(referencia, dados, nome_saida=None):
    """
    Converte arquivos do extrator para CSV.

    Args:
        referencia: Caminho do arquivo .REF.gz
        dados: Caminho do arquivo .TXT.gz
        nome_saida: Nome do arquivo de saída (opcional)

    Returns:
        DataFrame com os dados processados
    """
    log_mensagem(f"Processando: {os.path.basename(referencia)}")

    # Lê estrutura do arquivo de referência
    texto = read_gz(referencia)
    lista = []
    colunas = ["dt_atu"]

    for i in range(len(texto)):
        if i == 0:
            col = texto[0][:40].strip()
            tipo = texto[0][40:41].strip()
            tam = int(texto[0][43:46].strip())
            ini = 0
            fim = tam
            lista.append([col, tipo, tam, ini, fim])
            try:
                colunas.append(dados_campos[col])
            except:
                colunas.append(col.replace("-", "_"))
        else:
            col = texto[i][:40].strip()
            tipo = texto[i][40:41].strip()
            tam = int(texto[i][43:46].strip())
            ini = lista[-1][-1]
            fim = ini + tam
            lista.append([col, tipo, tam, ini, fim])
            try:
                colunas.append(dados_campos[col])
            except:
                colunas.append(col.replace("-", "_"))

    log_mensagem(f"Estrutura lida: {len(colunas)} colunas")

    # Lê arquivo de dados
    dados_lista = read_gz(dados)
    log_mensagem(f"Registros encontrados: {len(dados_lista)}")

    # Processa dados
    dados_final = []
    timestamp = datetime.datetime.now()
    data = timestamp.date()

    for linha in dados_lista:
        linha_dados = [data]
        for linha_lista in lista:
            ini = linha_lista[-2]
            fim = linha_lista[-1]
            col = linha_lista[0]

            if col[3:5] == "DA":
                linha_dados.append(
                    converte_data_invert(linha[ini:fim].strip()))
            elif col[3:5] == "QT":
                try:
                    linha_dados.append(int(linha[ini:fim].strip()))
                except:
                    linha_dados.append(0)
            else:
                linha_dados.append(linha[ini:fim].strip())
        dados_final.append(linha_dados)

    # Cria DataFrame
    df = pd.DataFrame(dados_final, columns=colunas)

    # Substitui datas inválidas
    try:
        df = df.applymap(substituir_data_invalida)
    except:
        df = df.apply(lambda x: x.map(substituir_data_invalida)
                      if x.dtype == 'object' else x)

    # Ajusta campos específicos
    try:
        df['siape'] = df['siape'].astype(str).str.slice(start=5, stop=12)
    except:
        pass
    try:
        df['upag'] = df['upag'].astype(str).str.slice(start=5, stop=14)
    except:
        pass
    try:
        df['lot_CodUORG_gr'] = df['lot_CodUORG_gr'].astype(str).str.slice(
            start=5, stop=14)
    except:
        pass
    try:
        df['lot_CodUPAG'] = df['lot_CodUPAG'].astype(str).str.slice(
            start=5, stop=14)
    except:
        pass
    try:
        df['lot_UORG_PAI'] = df['lot_UORG_PAI'].astype(str).str.slice(
            start=5, stop=14)
    except:
        pass

    # Salva arquivo
    if nome_saida:
        nome_arquivo = f"{nome_saida}_{dt_arq}.csv"
        df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig', sep=';')
        log_mensagem(f"✓ Arquivo salvo: {nome_arquivo}")

    return df


def getDirDetails(path=os.getcwd()):
    """Retorna lista de arquivos em um diretório."""
    arquivos = []
    pathExists = os.path.exists(path)
    isDir = os.path.isdir(path)

    if pathExists and isDir:
        for root, dirs, files in os.walk(path):
            for file in files:
                arquivos.append({file.replace(".gz", ""):
                                 os.path.join(root, file)})
    return arquivos


# ============== INTERFACE GRÁFICA ==============

def log_mensagem(msg):
    """Exibe mensagens na caixa de log."""
    txt_log.insert(tk.END, msg + "\n")
    txt_log.see(tk.END)
    root.update_idletasks()


def selecionar_arquivo_individual():
    """Permite selecionar arquivo REF.gz e TXT.gz individualmente."""
    log_mensagem("\n" + "="*50)
    log_mensagem("CONVERSÃO INDIVIDUAL DE ARQUIVOS")
    log_mensagem("="*50)

    # Seleciona arquivo REF
    ref_file = filedialog.askopenfilename(
        title="Selecione o arquivo de REFERÊNCIA (.REF.gz)",
        filetypes=[("Arquivo Referência", "*.REF.gz"), ("Todos", "*.*")]
    )

    if not ref_file:
        log_mensagem("✗ Operação cancelada pelo usuário")
        return

    log_mensagem(f"Referência: {os.path.basename(ref_file)}")

    # Seleciona arquivo TXT
    txt_file = filedialog.askopenfilename(
        title="Selecione o arquivo de DADOS (.TXT.gz)",
        filetypes=[("Arquivo Dados", "*.TXT.gz"), ("Todos", "*.*")]
    )

    if not txt_file:
        log_mensagem("✗ Operação cancelada pelo usuário")
        return

    log_mensagem(f"Dados: {os.path.basename(txt_file)}")

    # Solicita local de salvamento
    nome_base = os.path.splitext(os.path.basename(ref_file))[0].replace(
        '.REF', '')
    save_path = filedialog.asksaveasfilename(
        title="Salvar arquivo CSV",
        defaultextension=".csv",
        initialfile=f"{nome_base}_{dt_arq}.csv",
        filetypes=[("CSV", "*.csv"), ("Todos", "*.*")]
    )

    if not save_path:
        log_mensagem("✗ Operação cancelada pelo usuário")
        return

    # Remove extensão e timestamp do nome (será adicionado pela função)
    save_name = save_path.replace(f"_{dt_arq}.csv", "").replace(".csv", "")

    try:
        df = converter_extrator(ref_file, txt_file, save_name)
        log_mensagem(f"✓ Conversão concluída com sucesso!")
        log_mensagem(f"Total de registros: {len(df)}")
        messagebox.showinfo("Sucesso",
                            f"Arquivo convertido com sucesso!\n{len(df)} registros processados")
    except Exception as e:
        log_mensagem(f"✗ ERRO: {str(e)}")
        messagebox.showerror("Erro", f"Erro ao converter arquivo:\n{str(e)}")


def selecionar_pasta_batch():
    """Processa todos os arquivos em uma pasta."""
    log_mensagem("\n" + "="*50)
    log_mensagem("CONVERSÃO EM LOTE (PASTA)")
    log_mensagem("="*50)

    # Seleciona pasta de origem
    pasta_origem = filedialog.askdirectory(
        title="Selecione a pasta ORIGEM com arquivos REF.gz e TXT.gz"
    )

    if not pasta_origem:
        log_mensagem("✗ Operação cancelada pelo usuário")
        return

    log_mensagem(f"Pasta origem: {pasta_origem}")

    # Busca arquivos
    arq = getDirDetails(pasta_origem)

    if not arq:
        log_mensagem("✗ Nenhum arquivo encontrado na pasta")
        messagebox.showwarning("Aviso", "Nenhum arquivo encontrado na pasta")
        return

    # Conta quantos arquivos REF existem
    total_ref = sum(1 for linha in arq for nome in linha if nome.split(".")[-1] == "REF")
    
    if total_ref == 0:
        log_mensagem("✗ Nenhum arquivo .REF.gz encontrado")
        messagebox.showwarning("Aviso", "Nenhum arquivo .REF.gz encontrado na pasta")
        return

    log_mensagem(f"Arquivos .REF.gz encontrados: {total_ref}")

    # Seleciona pasta de destino
    pasta_destino = filedialog.askdirectory(
        title="Selecione a pasta DESTINO para salvar os arquivos CSV"
    )

    if not pasta_destino:
        log_mensagem("✗ Operação cancelada pelo usuário")
        return

    log_mensagem(f"Pasta destino: {pasta_destino}")
    log_mensagem("\nIniciando processamento...\n")

    processados = 0
    erros = []

    for linha in arq:
        for nome in linha:
            if nome.split(".")[-1] == "REF":
                ref = linha[nome]
                dados = linha[nome].replace('.REF.gz', '.TXT.gz')

                if not os.path.exists(dados):
                    log_mensagem(f"✗ Arquivo TXT não encontrado: {nome}")
                    erros.append(nome)
                    continue

                # Gera caminho de saída na pasta destino
                nome_arquivo_base = os.path.basename(linha[nome]).replace('.REF.gz', '')
                arquivo_saida = os.path.join(pasta_destino, nome_arquivo_base)

                try:
                    converter_extrator(ref, dados, arquivo_saida)
                    processados += 1
                except Exception as e:
                    log_mensagem(f"✗ Erro ao processar {nome}: {str(e)}")
                    erros.append(nome)

    log_mensagem("\n" + "="*50)
    log_mensagem(f"PROCESSAMENTO CONCLUÍDO")
    log_mensagem(f"Arquivos processados: {processados}")
    log_mensagem(f"Arquivos com erro: {len(erros)}")
    log_mensagem("="*50)

    if erros:
        messagebox.showwarning("Processamento Concluído com Avisos",
                               f"Processados: {processados}\nErros: {len(erros)}")
    else:
        messagebox.showinfo("Sucesso",
                            f"Todos os arquivos foram processados!\nTotal: {processados}")


def limpar_log():
    """Limpa a caixa de log."""
    txt_log.delete(1.0, tk.END)
    log_mensagem("Log limpo. Pronto para nova operação.")


# ============== CONFIGURAÇÃO DA JANELA ==============

root = tk.Tk()
root.title("Conversor de Arquivos Extrator SIAPE")
root.geometry("900x600")
root.resizable(True, True)

# Frame superior com botões
frame_botoes = tk.Frame(root, bg="#f0f0f0", pady=10)
frame_botoes.pack(fill=tk.X, padx=10, pady=5)

# Título
lbl_titulo = tk.Label(
    frame_botoes,
    text="Conversor de Arquivos Extrator SIAPE",
    font=("Arial", 14, "bold"),
    bg="#f0f0f0"
)
lbl_titulo.pack(pady=5)

# Frame para botões principais
frame_btns_principais = tk.Frame(frame_botoes, bg="#f0f0f0")
frame_btns_principais.pack(pady=5)

btn_individual = tk.Button(
    frame_btns_principais,
    text="📄 Converter Arquivo Individual",
    command=selecionar_arquivo_individual,
    font=("Arial", 11),
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=10,
    cursor="hand2"
)
btn_individual.pack(side=tk.LEFT, padx=5)

btn_pasta = tk.Button(
    frame_btns_principais,
    text="📁 Converter Pasta (Lote)",
    command=selecionar_pasta_batch,
    font=("Arial", 11),
    bg="#2196F3",
    fg="white",
    padx=20,
    pady=10,
    cursor="hand2"
)
btn_pasta.pack(side=tk.LEFT, padx=5)

btn_limpar = tk.Button(
    frame_btns_principais,
    text="🗑️ Limpar Log",
    command=limpar_log,
    font=("Arial", 11),
    bg="#FF9800",
    fg="white",
    padx=20,
    pady=10,
    cursor="hand2"
)
btn_limpar.pack(side=tk.LEFT, padx=5)

# Frame para log
frame_log = tk.Frame(root)
frame_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

lbl_log = tk.Label(frame_log, text="Log de Processamento:",
                   font=("Arial", 10, "bold"))
lbl_log.pack(anchor=tk.W)

txt_log = scrolledtext.ScrolledText(
    frame_log,
    width=100,
    height=25,
    font=("Consolas", 9),
    bg="#1e1e1e",
    fg="#00ff00"
)
txt_log.pack(fill=tk.BOTH, expand=True)

# Mensagem inicial
log_mensagem("="*50)
log_mensagem("CONVERSOR DE ARQUIVOS EXTRATOR SIAPE")
log_mensagem("="*50)
log_mensagem("Escolha uma opção:")
log_mensagem("  📄 Converter Arquivo Individual - Selecione REF.gz e TXT.gz")
log_mensagem(
    "  📁 Converter Pasta (Lote) - Processa todos os arquivos de uma pasta")
log_mensagem("="*50 + "\n")

# Rodapé
frame_rodape = tk.Frame(root, bg="#f0f0f0", pady=5)
frame_rodape.pack(fill=tk.X, side=tk.BOTTOM)

lbl_rodape = tk.Label(
    frame_rodape,
    text="Desenvolvido para processamento de arquivos do Extrator SIAPE | v2.0",
    font=("Arial", 8),
    bg="#f0f0f0",
    fg="#666"
)
lbl_rodape.pack()

# Inicia interface
root.mainloop()
