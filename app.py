from flask import Flask, request, render_template, url_for, redirect
from models import pysql
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/transacoes")
def transacoes():
    return render_template("form_transacao.html")

@app.route("/dashboards")
def dashboard():
    # 1. buscar transações no banco
    db = pysql()
    rows = db.search(
        "select data_transac, valor_transac "
        "from tbtransacao "
        "order by data_transac"
    )

    # se rows for lista de tuplas (data, valor)
    labels = [str(r[0]) for r in rows]
    valores = [float(r[1]) for r in rows]

    # converter para JSON para inserir no JS do template
    labels_json = json.dumps(labels)
    valores_json = json.dumps(valores)

    return render_template("dashboard.html", labels=labels_json, valores=valores_json)

@app.route("/salvar", methods=["post"])
def dados():
    botao = request.form.get("botao")

    match botao:
        case "Registrar":
            tipo = request.form["tipo"]
            valor = request.form["valor"]
            data = request.form["data"]
            categoria = request.form["categoria"]
            desc = request.form["descricao"]

            db = pysql()
            db.execute(
                "insert into tbtransacao (tipo_transac, valor_transac, data_transac, categoria_transac, desc_transac) "
                "values (%s, %s, %s, %s, %s)",
                (tipo, valor, data, categoria, desc)
            )

            return ("<script>"
                    "alert('Transação salva com sucesso!');"
                    "window.location = '/';"
                    "</script>")

        case "Gerar dashboard":
            return redirect(url_for("dashboard"))

        case _:
            return redirect(url_for("home"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)