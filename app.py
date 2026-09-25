from flask import Flask, jsonify, request
from supabase import create_client
from flasgger import Swagger
import os

app = Flask(__name__)
swagger = Swagger(app)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route("/comentarios", methods=["GET", "POST"])
def comentarios():
    """
    Consultar o agregar comentarios de clientes
    ---
    tags:
      - Comentarios
    parameters:
      - name: body
        in: body
        required: false
        schema:
          type: object
          properties:
            nombre_cliente:
              type: string
              example: Laura
            comentario:
              type: string
              example: Excelente atención
            calificacion:
              type: integer
              example: 5
    responses:
      200:
        description: Lista de comentarios (GET)
      201:
        description: Comentario creado (POST)
      400:
        description: Faltan datos obligatorios
    """
    if request.method == "POST":
        datos = request.get_json()

        if not datos or not datos.get("nombre_cliente") or not datos.get("comentario"):
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        nuevo = {
            "nombre_cliente": datos.get("nombre_cliente"),
            "comentario": datos.get("comentario"),
            "calificacion": datos.get("calificacion", 5),
        }
        respuesta = supabase.table("comentarios").insert(nuevo).execute()
        return jsonify(respuesta.data), 201

    respuesta = supabase.table("comentarios").select("*").order("id", desc=True).execute()
    return jsonify(respuesta.data)


if __name__ == "__main__":
    app.run()
