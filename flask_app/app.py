from flask import Flask, render_template, send_file
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

def create_plot():
    # Rastgele sayı oluşturma
    nokta_sayisi = 500
    x = np.random.randint(0, 1000, nokta_sayisi)
    y = np.random.randint(0, 1000, nokta_sayisi)

    # DataFrame'e kaydetme
    cerceve = pd.DataFrame({"x": x, "y": y})

    # Koordinatları 200'lük kısımlara bölme
    bolum_boyutu = 200
    cerceve["bolum_x"] = (cerceve["x"] // bolum_boyutu) * bolum_boyutu
    cerceve["bolum_y"] = (cerceve["y"] // bolum_boyutu) * bolum_boyutu

    # Bölümleri tek bir kimlik ile birleştirme
    cerceve["bolum_id"] = cerceve["bolum_x"] + cerceve["bolum_y"]

    # Bölümleri görselleştirme
    plt.figure(figsize=(10, 10))
    farkli_bolum = cerceve[["bolum_x", "bolum_y", "bolum_id"]].drop_duplicates()
    colors = plt.cm.jet(np.linspace(0, 1, len(farkli_bolum["bolum_id"].unique())))

    for i, bolum_id in enumerate(farkli_bolum["bolum_id"].unique()):
        nokta_bolumleri = cerceve[cerceve["bolum_id"] == bolum_id]
        plt.scatter(nokta_bolumleri["x"], nokta_bolumleri["y"], color=colors[i])

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Rastgele Nokta {bolum_boyutu}x{bolum_boyutu} Bolumler')
    plt.legend()
    plt.grid(True)
    plt.savefig('static/kordinatlar_foto.jpeg')
    plt.close()

@app.route('/')
def index():
    create_plot()
    return render_template('index.html')

@app.route('/update_plot')
def update_plot():
    create_plot()
    return send_file('static/kordinatlar_foto.jpeg', mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)
