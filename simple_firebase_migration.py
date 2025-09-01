import os

def migrate_panel_to_firebase(filename, professor_name):
    """Migrar un panel de localStorage a Firebase"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Agregar Firebase SDK
    if 'firebase-app-compat.js' not in content:
        firebase_sdk = '''  <!-- Firebase SDK -->
  <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore-compat.js"></script>'''
        
        content = content.replace(
            '<script src="https://kit.fontawesome.com/a2f1a4d5e1.js" crossorigin="anonymous"></script>',
            '<script src="https://kit.fontawesome.com/a2f1a4d5e1.js" crossorigin="anonymous"></script>\n' + firebase_sdk
        )
    
    # 2. Agregar Firebase config
    if 'firebase.initializeApp' not in content:
        firebase_config = f'''    // Firebase configuration
    const firebaseConfig = {{
      apiKey: "AIzaSyAbS_UCnlfw3P2loqpTl6Oh8A2Xswz3rPY",
      authDomain: "iet-student-control.firebaseapp.com",
      projectId: "iet-student-control",
      storageBucket: "iet-student-control.firebasestorage.app",
      messagingSenderId: "635566809825",
      appId: "1:635566809825:web:696842a0cb60356ed10da0"
    }};
    
    // Initialize Firebase
    firebase.initializeApp(firebaseConfig);
    const db = firebase.firestore();
    
    // Variables globales'''
        
        content = content.replace('// Variables globales', firebase_config)
    
    # 3. Reemplazar localStorage con Firebase
    content = content.replace(f'localStorage.setItem(\'{professor_name.lower()}_posts\', JSON.stringify(posts));', '')
    content = content.replace(f'localStorage.removeItem(\'{professor_name.lower()}_posts\');', '')
    
    # 4. Reemplazar DOMContentLoaded
    old_dom_loaded = f'''    // Cargar posts al iniciar
    document.addEventListener('DOMContentLoaded', function() {{
      const savedPosts = localStorage.getItem('{professor_name.lower()}_posts');
      if (savedPosts) {{
        posts = JSON.parse(savedPosts);
        // Asegurar que los posts tengan las propiedades necesarias
        posts.forEach(post => {{
          if (!post.hasOwnProperty('likes')) post.likes = 0;
          if (!post.hasOwnProperty('liked')) post.liked = false;
          if (!post.hasOwnProperty('edited')) post.edited = false;
        }});
      }} else {{
        // Solo crear post de ejemplo si no hay posts guardados
        const examplePost = {{
          id: Date.now(),
          content: '¡Hola! Este es un post de ejemplo con botones de editar y eliminar ✨',
          image: null,
          timestamp: new Date().toLocaleString('es-ES'),
          author: '{professor_name}',
          likes: 0,
          liked: false,
          edited: false
        }};
        posts.push(examplePost);
        localStorage.setItem('{professor_name.lower()}_posts', JSON.stringify(posts));
      }}
      
      renderPosts();
      
      // Cerrar emoji picker al hacer clic fuera
      document.addEventListener('click', function(e) {{
        const picker = document.getElementById('emojiPicker');
        const emojiBtn = e.target.closest('button[onclick="toggleEmojiPicker()"]');
        if (!picker.contains(e.target) && !emojiBtn) {{
          picker.classList.add('hidden');
        }}
      }});
    }});'''
    
    new_dom_loaded = f'''    // Cargar posts al iniciar
    document.addEventListener('DOMContentLoaded', function() {{
      // Cargar posts desde Firebase
      db.collection('professor_posts').doc('{professor_name.lower()}').collection('posts')
        .orderBy('timestamp', 'desc')
        .get()
        .then((querySnapshot) => {{
          posts = [];
          querySnapshot.forEach((doc) => {{
            const post = doc.data();
            if (!post.hasOwnProperty('likes')) post.likes = 0;
            if (!post.hasOwnProperty('liked')) post.liked = false;
            if (!post.hasOwnProperty('edited')) post.edited = false;
            posts.push(post);
          }});
          
          if (posts.length === 0) {{
            const examplePost = {{
              id: Date.now(),
              content: '¡Hola! Este es un post de ejemplo con botones de editar y eliminar ✨',
              image: null,
              timestamp: new Date().toLocaleString('es-ES'),
              author: '{professor_name}',
              likes: 0,
              liked: false,
              edited: false
            }};
            posts.push(examplePost);
            db.collection('professor_posts').doc('{professor_name.lower()}').collection('posts').doc(examplePost.id.toString()).set(examplePost);
          }}
          
          renderPosts();
        }})
        .catch((error) => {{
          console.error("Error cargando posts:", error);
          renderPosts();
        }});
      
      document.addEventListener('click', function(e) {{
        const picker = document.getElementById('emojiPicker');
        const emojiBtn = e.target.closest('button[onclick="toggleEmojiPicker()"]');
        if (!picker.contains(e.target) && !emojiBtn) {{
          picker.classList.add('hidden');
        }}
      }});
    }});'''
    
    content = content.replace(old_dom_loaded, new_dom_loaded)
    
    # 5. Actualizar createPost
    old_create_post = f'''      renderPosts();
      hidePostModal();
      
      // Guardar en localStorage
      localStorage.setItem('{professor_name.lower()}_posts', JSON.stringify(posts));'''
    
    new_create_post = f'''      renderPosts();
      hidePostModal();'''
    
    content = content.replace(old_create_post, new_create_post)
    
    # 6. Actualizar deletePost
    old_delete_post = f'''    function deletePost(postId) {{
      if (confirm('¿Estás seguro de que quieres eliminar esta publicación?')) {{
        posts = posts.filter(post => post.id !== postId);
        renderPosts();
        localStorage.setItem('{professor_name.lower()}_posts', JSON.stringify(posts));
      }}
    }}'''
    
    new_delete_post = f'''    function deletePost(postId) {{
      if (confirm('¿Estás seguro de que quieres eliminar esta publicación?')) {{
        posts = posts.filter(post => post.id !== postId);
        renderPosts();
        db.collection('professor_posts').doc('{professor_name.lower()}').collection('posts').doc(postId.toString()).delete();
      }}
    }}'''
    
    content = content.replace(old_delete_post, new_delete_post)
    
    # 7. Actualizar likePost
    old_like_post = f'''        renderPosts();
        localStorage.setItem('{professor_name.lower()}_posts', JSON.stringify(posts));'''
    
    new_like_post = f'''        renderPosts();
        db.collection('professor_posts').doc('{professor_name.lower()}').collection('posts').doc(postId.toString()).update({{
          likes: post.likes
        }});'''
    
    content = content.replace(old_like_post, new_like_post)
    
    # 8. Actualizar clearPosts
    old_clear_posts = f'''    function clearPosts() {{
      localStorage.removeItem('{professor_name.lower()}_posts');
      posts = [];
      renderPosts();
    }}'''
    
    new_clear_posts = f'''    function clearPosts() {{
      if (confirm('¿Estás seguro de que quieres eliminar TODAS las publicaciones? Esta acción no se puede deshacer.')) {{
        posts.forEach(post => {{
          db.collection('professor_posts').doc('{professor_name.lower()}').collection('posts').doc(post.id.toString()).delete();
        }});
        posts = [];
        renderPosts();
      }}
    }}'''
    
    content = content.replace(old_clear_posts, new_clear_posts)
    
    # Guardar el archivo
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {filename} migrado a Firebase")

# Migrar los paneles restantes
panels = [
    ('panel_erwin.html', 'Erwin'),
    ('panel_jesus.html', 'Jesus'),
    ('panel_astrid.html', 'Astrid'),
    ('panel_patty.html', 'Patty')
]

for filename, professor_name in panels:
    if os.path.exists(filename):
        migrate_panel_to_firebase(filename, professor_name)
    else:
        print(f"❌ {filename} no encontrado")

print("\n🎉 Migración completada!")
