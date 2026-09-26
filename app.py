¿from flask import Flask, jsonify, request
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
    responses:
      200:
        description: Lista de comentarios (GET)
      201:
        description: Comentario creado (POST)
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


@app.route("/comentarios/<int:comentario_id>", methods=["GET", "PUT", "DELETE"])
def comentario_detalle(comentario_id):
    """
    Consultar, editar o eliminar un comentario específico
    ---
    tags:
      - Comentarios
    parameters:
      - name: comentario_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Comentario obtenido o actualizado
      204:
        description: Comentario eliminado
      404:
        description: Comentario no encontrado
    """
    if request.method == "GET":
        respuesta = supabase.table("comentarios").select("*").eq("id", comentario_id).execute()
        if not respuesta.data:
            return jsonify({"error": "Comentario no encontrado"}), 404
        return jsonify(respuesta.data[0])

    if request.method == "PUT":
        datos = request.get_json()
        actualizado = {
            "nombre_cliente": datos.get("nombre_cliente"),
            "comentario": datos.get("comentario"),
            "calificacion": datos.get("calificacion"),
        }
        respuesta = supabase.table("comentarios").update(actualizado).eq("id", comentario_id).execute()
        if not respuesta.data:
            return jsonify({"error": "Comentario no encontrado"}), 404
        return jsonify(respuesta.data[0])

    if request.method == "DELETE":
        respuesta = supabase.table("comentarios").delete().eq("id", comentario_id).execute()
        return "", 204


if __name__ == "__main__":
    app.run()
