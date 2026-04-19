import os
import re

# Configuration
BLOG_FILE = 'blog.html'
INDEX_FILE = 'index.html'

def publish_latest_blog():
    if not os.path.exists(BLOG_FILE):
        print(f"Error: {BLOG_FILE} introuvable.")
        return

    if not os.path.exists(INDEX_FILE):
        print(f"Error: {INDEX_FILE} introuvable.")
        return

    print("--- Synchronisation du blog ---")

    # 1. Lire blog.html
    with open(BLOG_FILE, 'r', encoding='utf-8') as f:
        blog_content = f.read()

    # 2. Extraire le premier article
    # Cherche la balise <article class="blog-card ...">...</article>
    # On utilise re.DOTALL pour que le point matche les retours à la ligne
    match = re.search(r'(<article.*?</article>)', blog_content, re.DOTALL)
    
    if not match:
        print("Erreur : Aucun article trouvé dans blog.html")
        return
    
    latest_article = match.group(1)
    # Ajouter un petit commentaire pour l'index
    latest_article = "\n                <!-- Cet article est synchronisé automatiquement depuis blog.html -->\n                " + latest_article + "\n            "

    # 3. Lire index.html
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_content = f.read()

    # 4. Remplacer le contenu du conteneur #main-blog-container
    pattern = r'(<div class="blog-grid" id="main-blog-container">).*?(</div>)'
    new_index_content = re.sub(pattern, r'\1' + latest_article + r'\2', index_content, flags=re.DOTALL)

    if new_index_content == index_content:
        print("Avertissement : Le conteneur #main-blog-container n'a pas été trouvé ou est déjà à jour.")
    else:
        # 5. Sauvegarder index.html
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(new_index_content)
        print("Succès : index.html mis à jour avec le dernier article !")

if __name__ == "__main__":
    publish_latest_blog()
