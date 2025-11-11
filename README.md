# Conversor de Arquivos Extrator SIAPE

Ferramenta para converter arquivos compactados (.gz) do Extrator SIAPE em arquivos CSV estruturados e tratados.

## 📋 Funcionalidades

- ✅ **Conversão Individual**: Selecione arquivo REF.gz e TXT.gz manualmente
- ✅ **Conversão em Lote**: Processe todos os arquivos de uma pasta automaticamente
- ✅ Interface gráfica intuitiva com Tkinter
- ✅ Log detalhado do processamento em tempo real
- ✅ Tratamento automático de datas e campos especiais
- ✅ Mapeamento de campos SIAPE para nomes amigáveis
- ✅ Exportação em CSV com encoding UTF-8

## 🚀 Como usar

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/Conversor_Extrator_Final.git
cd Conversor_Extrator_Final
```

2. Execute o script de configuração:
```bash
setup.bat
```

Isso irá:
- Criar um ambiente virtual Python
- Instalar todas as dependências necessárias

### Executar o programa

```bash
run.bat
```

Ou manualmente:
```bash
venv\Scripts\activate
python src\conversor_extrator.py
```

## 📖 Modos de Operação

### Modo Individual
1. Clique em "📄 Converter Arquivo Individual"
2. Selecione o arquivo de referência (.REF.gz)
3. Selecione o arquivo de dados (.TXT.gz)
4. Escolha onde salvar o CSV resultante
5. Aguarde o processamento

### Modo Lote (Pasta)
1. Clique em "📁 Converter Pasta (Lote)"
2. Selecione a pasta contendo os arquivos
3. Os arquivos devem ter nomes correspondentes:
   - `nome_arquivo.REF.gz`
   - `nome_arquivo.TXT.gz`
4. Todos os arquivos serão processados automaticamente
5. CSVs serão salvos na mesma pasta dos originais

## 📦 Dependências

- Python 3.7+
- pandas
- sqlalchemy
- mysql-connector-python
- tkinter (incluído no Python)

## 🔧 Estrutura do Projeto

```
Conversor_Extrator_Final/
│
├── src/
│   └── conversor_extrator.py  # Código principal com interface
│
├── venv/                       # Ambiente virtual (não versionado)
│
├── requirements.txt            # Dependências Python
├── README.md                   # Este arquivo
├── .gitignore                  # Arquivos ignorados pelo Git
├── LICENSE                     # Licença MIT
├── setup.bat                   # Script de configuração
├── run.bat                     # Script de execução
└── deploy.bat                  # Script de deploy GitHub
```

## 📤 Deploy no GitHub

Para subir o projeto no GitHub:

1. Crie um repositório no GitHub (https://github.com/new)
2. Execute:
```bash
deploy.bat
```
3. Siga as instruções do script

## 🗺️ Mapeamento de Campos

O conversor mapeia automaticamente campos do formato SIAPE para nomes mais amigáveis:

- `GR-MATRICULA` → `siape`
- `IT-NO-SERVIDOR` → `nome`
- `IT-DA-NASCIMENTO` → `dt_nasc`
- `IT-NU-CPF` → `cpf`
- E muitos outros...

## 📝 Formato de Arquivos

### Arquivo de Referência (.REF.gz)
Contém a estrutura e metadados dos campos:
- Nome do campo (40 caracteres)
- Tipo de dado (1 caractere)
- Tamanho do campo (3 caracteres)

### Arquivo de Dados (.TXT.gz)
Contém os dados propriamente ditos em formato posicional fixo.

## ⚙️ Tratamentos Aplicados

- ✅ Conversão de datas (formato AAAAMMDD para datetime)
- ✅ Substituição de datas inválidas por NaT
- ✅ Ajuste de campos SIAPE (remoção de prefixos)
- ✅ Tratamento de campos numéricos
- ✅ Encoding UTF-8 com BOM para compatibilidade

## 🐛 Solução de Problemas

### Erro ao abrir arquivos .gz
- Verifique se os arquivos não estão corrompidos
- Certifique-se de que são arquivos .gz válidos

### Erro de encoding
- Os arquivos CSV são salvos em UTF-8 com BOM
- Abra no Excel ou LibreOffice com encoding UTF-8

### Campos não aparecem
- Verifique se o arquivo .REF.gz corresponde ao .TXT.gz
- Os arquivos devem ser da mesma extração

## 📝 Licença

MIT License - Veja o arquivo LICENSE para detalhes

## 👤 Autor

Desenvolvido para processamento de arquivos do Extrator SIAPE
