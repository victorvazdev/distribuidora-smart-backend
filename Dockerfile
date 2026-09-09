# Usa a versão slim para reduzir a superfície de ataque e o tamanho final da imagem
FROM python:3.14.7-slim

WORKDIR /app

# Copia apenas o arquivo de dependências primeiro para aproveitar o cache de camadas do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["flask", "run", "--host=0.0.0.0", "--port=8000"]