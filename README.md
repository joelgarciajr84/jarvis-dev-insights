# Jarvis Dev Insights

https://fastmcp.cloud/app/jarvis-tech-lead

Um Simples MCP Server Para code Review:

- Scan do repositório (arquivos, linguagens, CI/tests)
- Busca de TODO/FIXME
- Sumário de Markdown
- Code Review estático para JS/TS/Python

## Instalação

```bash
pip install fastmcp
```

## Rodando local

```bash
export PYTHONPATH=.
python src/presentation/server.py
# ou com CLI
fastmcp run src/presentation/server.py
```

## Uso

No VS Code (Agent Mode), basta conversar naturalmente, por exemplo:

> "Revise meu código"

O host (VS Code) chamará automaticamente a tool `review_code`.

## Licença

MIT
