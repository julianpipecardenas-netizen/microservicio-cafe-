from flask import Flask, jsonify
from supabase import create_client
import os

app = Flask(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/comentarios")
def comentarios():
    respuesta = supabase.table("comentarios").select("*").execute()
    return jsonify(respuesta.data)

if __name__ == "__main__":
    app.run()