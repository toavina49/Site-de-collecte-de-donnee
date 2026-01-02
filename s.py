from flask import Flask, request, render_template_string, redirect, url_for
from tinydb import TinyDB
from datetime import datetime # Nouveau : pour la date automatique

app = Flask(__name__)
db = TinyDB('donne1.json') #j enregistre les donnes dans donne1.JSON
#corps de la page
HTML_PRO = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>COLLECTE DE DONNES</title>
    <style>
 @keyframes moveBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
body { 
            font-family: sans-serif; 
            background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
            background-size: 400% 400%;
            animation: moveBG 10s ease infinite;
            display: flex; justify-content: center; align-items: center;
            min-height: 100vh; margin: 0;
        }
.box { 
            background: rgba(255,255,255,0.95); padding: 30px; 
            border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            width: 95%; max-width: 650px;
     }
        input {
  width: 100%;
  padding: 12px;
  margin: 10px 0;
  border-radius: 8px;
  border: 1px solid #ccc;
  box-sizing: border-box; }
        input[type="submit"] { background: #1a73e8; color: white; cursor: pointer; border: none; font-weight: bold; font-size: 16px; }
        
 table { 
       width: 100%; border-collapse: collapse; margin-top: 20px; background: white; border-radius: 8px; overflow: hidden; }
 th, td {
     border-bottom: 1px solid #eee; padding: 12px; text-align: left; font-size: 14px; }
         th {
  background: #f8f9fa;
 color: #666; 
 }
        
   .btn-delete { color: #ff4d4d; text-decoration: none; font-weight: bold; font-size: 20px; padding: 0 10px; }
   .date-text { color: #888; font-size: 12px; }
 </style>
</head>
 

 
 <body>
    <div class="box">
<h1 style="text-align:center; color:#333; margin-top:0;">SAVE YOUR DATA</h1>
        
        <form action="/ajouter" method="POST">
 <input type="text" name="nom" placeholder="NAME " required>
  <input type="text" name="message" placeholder="about" required>
 <input type="submit" value="ENREGISTRER">
        </form>

        <h3>DATA RECORDED</h3>
        <table>
            <tr>
                <th>Date</th>
                <th>NAME</th>
                <th>ABOUT</th>
                <th>CLICK THERE FOR CLEANING</th>
            </tr>
            {% for d in liste %}
            <tr>
                <td class="date-text">{{ d.date }}</td>
                <td><b>{{ d.nom }}</b></td>
                <td>{{ d.message }}</td>
                <td>
                    <a href="/supprimer/{{ d.doc_id }}" class="btn-delete" title="Supprimer">Ã—</a>
                </td>
     </tr>
   {% endfor %}
 </table>
 </div>
</body>
</html>
"""

@app.route('/')
def index():
    donnees = []
    for item in db.all():
        item['doc_id'] = item.doc_id
        donnees.append(item)
    # j affiche les donnees ( mais ici c'est l'ordre d'insertion)
    return render_template_string(HTML_PRO, liste=donnees)

  

@app.route('/ajouter', methods=['POST'])
def ajouter():
    # On recupere la date et l'heure actuelle au format Jour/Mois/Annee Heure:Minute
    maintenant = datetime.now().strftime("%d/%m/%Y %H:%M")
    
  
  
#j envoie les donnes  inserees
 
    db.insert({
        'nom': request.form['nom'], 
        'message': request.form['message'],
        'date': maintenant # On enregistre la date ici
     })
    return redirect(url_for('index'))

 
 #je supprime les donnes envoyes
@app.route('/supprimer/<int:id_donnee>')
def supprimer(id_donnee):
    db.remove(doc_ids=[id_donnee])
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(port=8040, debug=True)
#MODE D EMPLOI juste copier ce lien associe au port
