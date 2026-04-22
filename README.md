# pdf-merge

API simple en FastAPI para unir multiples PDFs remotos en un solo archivo.

## Endpoints

- GET /health
	- Retorna estado de servicio.
- POST /merge
	- Recibe JSON con URLs de PDF y retorna el archivo combinado.

Swagger UI disponible en /docs.

Ejemplo de body:

```json
{
	"pdf_urls": [
		"https://example.com/a.pdf",
		"https://example.com/b.pdf"
	]
}
```

## Correr local

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8080
```

## Deploy en Railway

1. Sube este repo a GitHub.
2. En Railway, crea un nuevo proyecto desde GitHub y selecciona este repo.
3. Railway detecta el Dockerfile automaticamente.
4. Despliega y usa la URL publica que Railway te entrega.
5. Verifica salud en /health.

## Prueba con curl

```bash
curl -X POST "https://tu-app.up.railway.app/merge" \
	-H "Content-Type: application/json" \
	-d '{"pdf_urls":["https://example.com/a.pdf","https://example.com/b.pdf"]}' \
	--output merged.pdf
```

## Consumo desde agente (simple)

- Request: POST JSON con `pdf_urls`.
- Response: binario PDF (`application/pdf`).
- Recomendacion: guardar la respuesta como archivo (por ejemplo `merged.pdf`).