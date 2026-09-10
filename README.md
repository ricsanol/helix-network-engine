# Helix Network Engine

O **Helix Network Engine** é um projeto em Python voltado para automação de redes multi-vendor, desenvolvido para transformar dados estruturados de serviços de rede em processos de validação, geração de configurações e preparação de implantação.

O projeto foi desenvolvido como parte do portfólio **OliveHex**, com foco em automação, padronização e redução de tarefas manuais em ambientes de redes.

## Objetivo

O objetivo do Helix Network Engine é criar uma camada de automação capaz de:

- Ler informações estruturadas de serviços de rede.
- Identificar equipamentos e fabricantes envolvidos.
- Validar informações antes da geração das configurações.
- Executar verificações de pré-check nos equipamentos.
- Selecionar automaticamente templates de acordo com o fabricante.
- Gerar configurações de forma padronizada.
- Organizar os resultados do processamento.
- Preparar a arquitetura para evolução de workflows de implantação.

## Arquitetura

O projeto foi organizado em módulos com responsabilidades separadas:

```text
helix/
├── core/          # Orquestração e regras principais
├── input/         # Leitura e mapeamento dos dados de entrada
├── models/        # Modelos de domínio
├── precheck/      # Validações e comunicação com equipamentos
└── templates/     # Seleção e renderização de templates

templates/
├── cisco/
└── huawei/

data/
├── helix_cluster_template.xlsx
└── helix_network_engine_template_mvp.xlsx
```

## Fluxo simplificado

```text
Dados de entrada
      ↓
Leitura e mapeamento
      ↓
Resolução do ambiente
      ↓
Pré-check
      ↓
Validação
      ↓
Decision Engine
      ↓
Seleção de template
      ↓
Geração da configuração
      ↓
Resultado
```

## Suporte multi-vendor

A arquitetura foi desenvolvida para trabalhar com diferentes fabricantes de equipamentos de rede.

Atualmente o projeto possui componentes para:

- Cisco
- Huawei

A estrutura permite evolução para novos fabricantes através da separação entre clientes, comandos, validadores e templates.

## Templates

A geração das configurações utiliza templates Jinja2 específicos para cada plataforma.

Exemplos disponíveis:

- Cisco IOS
- Cisco IOS XR
- Huawei VRP

Essa abordagem permite separar a lógica da aplicação da sintaxe específica de cada fabricante.

## Pré-check

Antes da geração ou preparação de uma configuração, o sistema possui uma camada de pré-check responsável por realizar verificações no ambiente.

Essa camada foi estruturada com:

- Clientes específicos por fabricante.
- Comandos de validação.
- Validadores.
- Tratamento de exceções.
- Geração de relatórios.
- Logging.

## Segurança

Credenciais reais não fazem parte deste repositório.

O projeto utiliza variáveis de ambiente para informações sensíveis, como:

```text
HELIX_SSH_USERNAME
HELIX_SSH_PASSWORD
```

O arquivo `.env.example` demonstra a estrutura esperada sem disponibilizar credenciais reais.

Os endereços IP, hostnames e demais informações presentes nos exemplos públicos são fictícios e destinados exclusivamente à demonstração do projeto.

Consulte também o arquivo `SECURITY.md`.

## Instalação

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual e instale as dependências:

```bash
pip install -r requirements.txt
```

Configure as variáveis de ambiente necessárias utilizando o arquivo `.env.example` como referência.

## Execução

O ponto de entrada principal do projeto é:

```bash
python main.py
```

## Tecnologias

- Python
- Jinja2
- Pandas / OpenPyXL
- SSH / Automação de redes
- Arquitetura modular
- Templates multi-vendor
- Git / GitHub

## Dados públicos

As planilhas e exemplos disponíveis neste repositório foram preparados exclusivamente para demonstração.

Eles utilizam dados fictícios e não representam equipamentos, endereços, credenciais ou topologias de uma rede de produção.

## Sobre o projeto

O Helix Network Engine é um projeto de portfólio desenvolvido para demonstrar conhecimentos em:

- Desenvolvimento Python.
- Automação de redes.
- Arquitetura de software.
- Processamento de dados.
- Integração multi-vendor.
- Validação de configurações.
- Geração automatizada de scripts.
- Boas práticas de segurança e versionamento.

## Autor

**Ricardo Oliveira**

Projeto desenvolvido como parte do portfólio **OliveHex**.

## Licença

Este repositório é disponibilizado publicamente para fins de demonstração e portfólio.

Nenhuma licença open source é concedida neste momento.