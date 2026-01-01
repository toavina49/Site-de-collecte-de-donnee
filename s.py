from flask import Flask, request, redirect # J'ai ajoute 'redirect'
from tinydb import TinyDB

app = Flask(__name__)
db = TinyDB('donne1.json')

# 1. LA PAGE D'ACCUEIL (Le Formulaire)
@app.route('/')
def accueil():
    return '''
    <html>
        <head><title>Mon Interface Pro</title></head>
        <body style="font-family: sans-serif; padding: 20px;">
            <h1>Ajouter une donnée</h1>
            <form action="/api/ajouter" method="POST">
                <label>Nom :</label><br>
                <input type="text" name="nom" required><br><br>
                
                <label>Message :</label><br>
                <input type="text" name="message" required><br><br>
                
                <input type="submit" value="Enregistrer dans la base">
            </form>
        </body>
    </html>
    '''

# 2. LE TRAITEMENT (Bilingue : JSON ou Formulaire)
@app.route('/api/ajouter', methods=['POST'])
def ajouter_donne():
    # Si c'est un formulaire Web (navigateur)
    if request.form:
        nom = request.form.get('nom')
        message = request.form.get('message')
        # On enregistre
        db.insert({'nom': nom, 'message': message})
        return f"<h1>Succès !</h1><p>Merci {nom}, message enregistré.</p><a href='/'>Retour</a>"
    
    # Si c'est du JSON (curl ou API externe)
    elif request.is_json:
        donnees = request.get_json()
        db.insert(donnees)
        return {"status": "Succès via JSON"}
    
    return "Erreur : Format non reconnu"

if __name__ == "__main__":
    app.run(port=8000, debug=True)
