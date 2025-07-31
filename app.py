from flask import Flask, render_template, request, redirect, session, send_file
from datetime import datetime
from firebase_config import db
from exportador import exportar_excel
import os

app = Flask(__name__)
app.secret_key = "chave-secreta"

BASES = {
    "bage": "senha1",
    "uruguaiana": "senha2"
}

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        base = request.form["base"].lower()
        senha = request.form["senha"]
        if BASES.get(base) == senha:
            session["base"] = base
            return redirect("/dashboard")
        else:
            return render_template("login.html", erro="Login inválido.")
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "base" not in session:
        return redirect("/")
    base = session["base"]

    # Novo registro
    if request.method == "POST":
        novo = {
            "data": request.form["data"],
            "hora": datetime.now().strftime("%H:%M:%S"),
            "onibus": request.form["onibus"],
            "litros": float(request.form["litros"]),
            "responsavel": request.form["responsavel"],
            "base": base
        }
        db.collection("abastecimentos").add(novo)
        return redirect("/dashboard")

    # Filtros
    filtro_data = request.args.get("filtro_data")
    filtro_onibus = request.args.get("filtro_onibus", "").lower()

    # Carregar registros da base do usuário
    docs = db.collection("abastecimentos").where("base", "==", base).stream()
    dados = []
    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id
        dados.append(d)

    if filtro_data:
        dados = [d for d in dados if d["data"] == filtro_data]
    if filtro_onibus:
        dados = [d for d in dados if filtro_onibus in d["onibus"].lower()]

    dados.sort(key=lambda x: (x["data"], x["hora"]), reverse=True)
    total_litros = sum(d["litros"] for d in dados)

    return render_template("dashboard.html", dados=dados, base=base, total_litros=total_litros)

@app.route("/editar/<id>", methods=["GET", "POST"])
def editar(id):
    if "base" not in session:
        return redirect("/")
    doc_ref = db.collection("abastecimentos").document(id)
    doc = doc_ref.get()
    if not doc.exists:
        return "Registro não encontrado", 404
    registro = doc.to_dict()

    if request.method == "POST":
        registro["data"] = request.form["data"]
        registro["onibus"] = request.form["onibus"]
        registro["litros"] = float(request.form["litros"])
        registro["responsavel"] = request.form["responsavel"]
        doc_ref.set(registro)
        return redirect("/dashboard")

    return render_template("editar.html", registro=registro, index=id)

@app.route("/excluir/<id>")
def excluir(id):
    if "base" not in session:
        return redirect("/")
    db.collection("abastecimentos").document(id).delete()
    return redirect("/dashboard")

@app.route("/exportar")
def exportar():
    if "base" not in session:
        return redirect("/")
    base = session["base"]
    docs = db.collection("abastecimentos").where("base", "==", base).stream()
    dados = [doc.to_dict() for doc in docs]
    caminho_excel = exportar_excel(base, dados)
    return
