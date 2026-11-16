# Heart Disease App — ML III / Aula 10

Aplicação didática que integra **Streamlit → FastAPI → modelo de Machine Learning**. O mesmo repositório será usado para publicar o backend no Render e o frontend no Streamlit Community Cloud.

> **Uso exclusivamente educacional. Não é um instrumento de diagnóstico médico.**

## Estrutura

```text
heart-disease-app/
├── app.py                    # Interface Streamlit
├── api.py                    # Backend FastAPI
├── train_model.py            # Treinamento (opcional: modelo já incluído)
├── requirements.txt          # Dependências Python
├── data/Heart_disease_cleveland.csv
├── models/heart_model.joblib # Modelo já treinado
├── models/metadata.json
├── .gitignore
└── README.md
```

## 1. Criar o repositório Git do zero

1. Descompacte o ZIP. Abra **a pasta `heart-disease-app`** no VS Code.
2. Confira `git --version` no terminal. O Git é instalado no Windows, separadamente do Python/Conda.
3. Source Control → **Initialize Repository** (ou `git init -b main`).
4. Faça **Stage All Changes** → **Commit**, com mensagem `Primeira versão pronta para publicação`.
5. Clique em **Publish to GitHub** → repositório **público** `heart-disease-app`. Autorize o GitHub, se solicitado.
6. Confirme no navegador que `app.py`, `api.py`, `models/` e `README.md` estão no repositório.

> Não há pasta `.git` neste ZIP: cada aluno inicia seu próprio histórico.

## 2. Testar localmente (opcional)

No terminal do VS Code, com o ambiente Python adequado ativado:

```bash
pip install -r requirements.txt
```

Terminal 1:

```bash
python -m uvicorn api:app --reload
```

Teste `http://127.0.0.1:8000/docs`.

Terminal 2:

```bash
python -m streamlit run app.py
```

Acesse `http://localhost:8501`. Sem configuração adicional, a interface chama a API local.

O modelo já está treinado. Para refazer o treinamento (não necessário para o deploy):

```bash
python train_model.py
```

## 3. Publicar a API no Render

1. Acesse https://dashboard.render.com e crie um **Web Service**.
2. Conecte o GitHub e selecione o repositório `heart-disease-app` e a branch `main`.
3. Selecione a opção gratuita, caso disponível.
4. Configure:

   **Build Command**

   ```bash
   pip install -r requirements.txt
   ```

   **Start Command**

   ```bash
   uvicorn api:app --host 0.0.0.0 --port $PORT
   ```

5. Aguarde o deploy. Abra `https://NOME-DO-SERVICO.onrender.com/docs` e teste `/predict` no Swagger.
6. Copie a URL pública do backend para a próxima etapa.

**Por que `0.0.0.0` e `$PORT`?** O servidor precisa aceitar conexões externas e usar a porta fornecida pela plataforma.

## 4. Publicar a interface no Streamlit Community Cloud

1. Acesse https://share.streamlit.io e conecte sua conta GitHub.
2. Crie um app selecionando repositório `heart-disease-app`, branch `main` e arquivo `app.py`.
3. Em **App settings → Secrets**, configure a URL da API, usando o endereço real do Render:

   ```toml
   API_URL = "https://NOME-DO-SERVICO.onrender.com/predict"
   ```

4. Salve as configurações e reinicie/reimplante o app se necessário.
5. Acesse a URL `*.streamlit.app`, preencha o formulário e clique em **Realizar previsão**.

A interface lê `API_URL` da configuração da nuvem, ou de variável de ambiente do sistema; na ausência de ambas, usa a API local.

## 5. Atualizações após a publicação

No VS Code: editar → salvar → Stage → Commit → Push. As plataformas conectadas ao GitHub podem iniciar um novo deploy automaticamente; acompanhe o status e os logs.

## 6. Problemas frequentes

- **Erro de conexão:** confira se a URL em Secrets termina em `/predict` e se o Render está ativo.
- **Primeira requisição lenta:** o plano gratuito do Render pode suspender o serviço quando ocioso; aguarde a inicialização.
- **Falha ao iniciar API:** confira os logs, o comando `api:app` e os arquivos `models/` no GitHub.
- **Erro de bibliotecas:** confira `requirements.txt` e logs de instalação.
- **Erro 405 ao abrir `/predict` no navegador:** esse endpoint recebe **POST**; teste pelo `/docs`.
- **Mudanças não apareceram:** verifique se fez **Push** e se o deploy terminou.

## Arquitetura

```text
Navegador do usuário
         ↓
Streamlit Community Cloud (app.py)
         ↓ HTTPS / JSON
Render (api.py / FastAPI)
         ↓
models/heart_model.joblib
         ↓
Resposta JSON → Streamlit → usuário
```

**Observação:** serviços gratuitos podem ter limitações, suspensão por inatividade e alterações nas condições de uso.
