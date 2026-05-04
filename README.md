# ⚽ Football Scout

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)

O **Football Scout** é uma plataforma avançada de análise de dados destinada à identificação de talentos e análise de desempenho no futebol. Utilizando dados históricos do FIFA, a aplicação transforma estatísticas complexas em insights acionáveis para scouts, analistas e entusiastas.

---

## 📋 Índice
- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades Principais](#-funcionalidades-principais)
- [Stack Tecnológico](#-stack-tecnológico)
- [Estrutura de Diretórios](#-estrutura-de-diretórios)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Como Usar](#-como-usar)
- [Análise de Dados e ML](#-análise-de-dados-e-ml)

---

## 📖 Sobre o Projeto
A aplicação permite navegar por um vasto conjunto de dados de jogadores profissionais para descobrir "Wonderkids" (jovens promessas), analisar veteranos de alto nível, agrupar jogadores por estilos de jogo (arquétipos) e comparar a evolução histórica de atletas. Através de algoritmos de **Machine Learning** e **Similaridade de Cosseno**, o sistema oferece recomendações precisas de jogadores com perfis similares.

---

## ✨ Funcionalidades Principais

* **💎 Wonderkids (`/wonderkids`):** Identificação de jovens talentos com menos de 21 anos, potencial superior a 80 e valor de mercado acessível (até €20M).
* **👴 Veteranos (`/veterans`):** Filtro de jogadores experientes (29+ anos) que mantêm um alto nível competitivo (Overall 80+).
* **👯 Jogadores Similares (`/similar_players`):** Motor de busca que utiliza cálculo de similaridade para encontrar atletas com atributos técnicos equivalentes a um jogador de referência.
* **📊 Comparação de Jogadores (`/players_comparison`):** Ferramenta visual com gráficos interativos (Plotly) para comparar o desenvolvimento de dois jogadores ao longo das edições do FIFA.
* **🧩 Arquétipos de Jogadores (`/archetypes`):** Agrupamento inteligente de jogadores em clusters baseados no seu estilo de jogo real, utilizando o algoritmo KMeans.
* **🚀 Evolução (`/players_evolution`):** Visualização detalhada do crescimento dos atributos de um jogador específico ao longo do tempo.
* **💰 Outros Recursos:** Filtros por liga, busca por jogadores em promoção (*bargain players*) e identificação de "Late Bloomers" (jogadores que atingiram o auge tardiamente).

---

## 🛠 Stack Tecnológico

* **Backend:** Python 3.x / Flask
* **Frontend:** HTML5, CSS3, JavaScript
* **Processamento de Dados:** Pandas, NumPy
* **Machine Learning:** Scikit-learn (KMeans, Cosine Similarity, RandomForestRegressor)
* **Visualização:** Plotly

---

## 📂 Estrutura de Diretórios

```text
football-scout/
├── app.py                  # Aplicação Flask principal (rotas e inicialização)
├── funcs1.py               # Lógica de filtragem e análise de dados básica
├── funcs2.py               # Funções avançadas, visualizações e ML
├── data/
│   ├──male_players(legacy).csv # Dataset principal (necessário para execução)
├── templates/              # Ficheiros HTML (Jinja2)
│   ├── index.html
│   ├── wonderkids.html
│   ├── archetypes.html     # E outros templates...
└── static/                 # Recursos estáticos (CSS)
    ├── scout.css           # Estilo global
    └── index.css           # Estilos específicos por módulo
