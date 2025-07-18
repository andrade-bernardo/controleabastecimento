from flask import Flask, render_template, request, redirect, session, send_file
from datetime import datetime
import json
import os
from exportador import exportar_excel

app = Flask(__name__)
app.secret_key = "chave-secreta"

DADOS_ARQUIVO = "abastecimentos.json"
BASES = {
    "bage": "senha1",
    "uruguaiana": "senha2"
}

def carregar_dados():
    if os.path.exists(DADOS_ARQUIVO):
        with open(DADOS_ARQUIVO, "r") as f:
            return json.load(f)
    return []

def salvar_dados(dados):
    with open(DADOS_ARQUIVO, "w") as f:
        json.dump(dados, f, indent=2)

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
    dados = carregar_dados()

    # Registro novo
    if request.method == "POST":
        novo = {
            "data": request.form["data"],
            "hora": datetime.now().strftime("%H:%M:%S"),
            "onibus": request.form["onibus"],
            "litros": float(request.form["litros"]),
            "responsavel": request.form["responsavel"],
            "base": base
        }
        dados.append(novo)
        salvar_dados(dados)
        return redirect("/dashboard")

    # Filtros
    filtro_data = request.args.get("filtro_data")
    filtro_onibus = request.args.get("filtro_onibus", "").lower()

    filtrados = [d for d in dados if d["base"] == base]

    if filtro_data:
        filtrados = [d for d in filtrados if d["data"] == filtro_data]

    if filtro_onibus:
        filtrados = [d for d in filtrados if filtro_onibus in d["onibus"].lower()]

    filtrados.sort(key=lambda x: (x["data"], x["hora"]), reverse=True)

    return render_template("dashboard.html", dados=filtrados, base=base)

@app.route("/editar/<int:index>", methods=["GET", "POST"])
def editar(index):
    if "base" not in session:
        return redirect("/")
    dados = carregar_dados()
    base = session["base"]

    # Filtrar apenas os dados dessa base
    dados_base = [d for d in dados if d["base"] == base]

    if index >= len(dados_base):
        return "Registro não encontrado", 404

    # Encontrar o índice real no JSON (original)
    real_index = [i for i, d in enumerate(dados) if d["base"] == base][index]
    registro = dados[real_index]

    if request.method == "POST":
        registro["data"] = request.form["data"]
        registro["onibus"] = request.form["onibus"]
        registro["litros"] = float(request.form["litros"])
        registro["responsavel"] = request.form["responsavel"]
        salvar_dados(dados)
        return redirect("/dashboard")

    return render_template("editar.html", registro=registro, index=index)

@app.route("/excluir/<int:index>")
def excluir(index):
    if "base" not in session:
        return redirect("/")
    dados = carregar_dados()
    base = session["base"]

    dados_base = [d for d in dados if d["base"] == base]

    if index >= len(dados_base):
        return "Registro não encontrado", 404

    real_index = [i for i, d in enumerate(dados) if d["base"] == base][index]
    dados.pop(real_index)
    salvar_dados(dados)
    return redirect("/dashboard")

@app.route("/exportar")
def exportar():
    if "base" not in session:
        return redirect("/")
    caminho_excel = exportar_excel(session["base"], carregar_dados())
    return send_file(caminho_excel, as_attachment=True)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
