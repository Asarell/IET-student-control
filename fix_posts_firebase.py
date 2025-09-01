import os
import re

def add_firebase_to_panel(filename, professor_name):
    """Agregar Firebase a un panel y migrar posts de localStorage a Firebase"""
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Agregar Firebase SDK después de FontAwesome
    firebase_sdk = '''  <!-- Firebase SDK -->
  <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-app-compat.js"></script>
  <script src="https://www.gstatic.com/firebasejs/10.12.0/firebase-firestore-compat.js"></script>'''
    
    content = re.sub(
        r'(<script src="https://kit\.fontawesome\.com/[^"]+" crossorigin="anonymous"></script>)',
        r'\1' + '\n' + firebase_sdk,
        content
    )
    
    # 2. Agregar Firebase config después de "Variables globales"
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
    
    content = re.sub(
        r'(// Variables globales)',
        firebase_config,
        content
    )
    
    # 3. Reemplazar localStorage.setItem con Firebase
    content = re.sub(
        r'localStorage\.setItem\([^)]+\);',
        '',
        content
    )
    
    # 4. Reemplazar localStorage.getItem con Firebase
    content = re.sub(
        r'const savedPosts = localStorage\.getItem\([^)]+\);',
        f'// Cargar posts desde Firebase',
        content
    )
    
    # 5. Reemplazar la función DOMContentLoaded completa
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
    
    # Buscar y reemplazar la función DOMContentLoaded
    pattern = r'// Cargar posts al iniciar\s+document\.addEventListener\('DOMContentLoaded', function\(\) \{.*?\}\);'
    content = re.sub(pattern, new_dom_loaded, content, flags=re.DOTALL)
    
    # 6. Actualizar createPost para usar Firebase
    new_create_post = f'''    function createPost(event) {{
      event.preventDefault();
      const content = document.getElementById('postContent').value.trim();
      if (!content) return;

      if (editingPostId) {{
        const postIndex = posts.findIndex(p => p.id === editingPostId);
        if (postIndex !== -1) {{
          const postToUpdate = posts[postIndex];
          postToUpdate.content = content;
          postToUpdate.image = selectedImage;
          postToUpdate.edited = true;
          postToUpdate.editTimestamp = new Date().toLocaleString('es-ES');
          
          db.collection('professor_posts').doc('{professor_name.lower()}').collection('posts').doc(postToUpdate.id.toString()).update({{
            content: content,
            image: selectedImage,
            edited: true,
            editTimestamp: new Date().toLocaleString('es-ES')
          }});
        }}
        editingPostId = null;
      }} else {{
        const postId = Date.now();
        const post = {{
          id: postId,
          content: content,
          image: selectedImage,
          timestamp: new Date().toLocaleString('es-ES'),
          author: '{professor_name}',
          likes: 0,
          liked: false,
          edited: false
        }};
        posts.unshift(post);
        db.collection('professor_posts').doc('{professor_name.lower()}').collection('posts').doc(postId.toString()).set(post);
      }}

      renderPosts();
      hidePostModal();
    }}'''
    
    # Buscar y reemplazar createPost
    pattern = r'function createPost\(event\) \{.*?\n\s+renderPosts\(\);\n\s+hidePostModal\(\);\n\s+\}'
    content = re.sub(pattern, new_create_post, content, flags=re.DOTALL)
    
    # 7. Actualizar deletePost para usar Firebase
    new_delete_post = f'''    function deletePost(postId) {{
      if (confirm('¿Estás seguro de que quieres eliminar esta publicación?')) {{
        posts = posts.filter(post => post.id !== postId);
        renderPosts();
        db.collection('professor_posts').doc('{professor_name.lower()}').collection('posts').doc(postId.toString()).delete();
      }}
    }}'''
    
    pattern = r'function deletePost\(postId\) \{.*?\n\s+\}'
    content = re.sub(pattern, new_delete_post, content, flags=re.DOTALL)
    
    # 8. Actualizar likePost para usar Firebase
    new_like_post = f'''    function likePost(postId) {{
      const post = posts.find(p => p.id === postId);
      if (post) {{
        if (post.liked) {{
          post.liked = false;
          post.likes = Math.max(0, post.likes - 1);
        }} else {{
          post.liked = true;
          post.likes = (post.likes || 0) + 1;
        }}
        
        renderPosts();
        db.collection('professor_posts').doc('{professor_name.lower()}').collection('posts').doc(postId.toString()).update({{
          likes: post.likes
        }});
      }}
    }}'''
    
    pattern = r'function likePost\(postId\) \{.*?\n\s+\}'
    content = re.sub(pattern, new_like_post, content, flags=re.DOTALL)
    
    # 9. Actualizar clearPosts para usar Firebase
    new_clear_posts = f'''    function clearPosts() {{
      if (confirm('¿Estás seguro de que quieres eliminar TODAS las publicaciones? Esta acción no se puede deshacer.')) {{
        posts.forEach(post => {{
          db.collection('professor_posts').doc('{professor_name.lower()}').collection('posts').doc(post.id.toString()).delete();
        }});
        posts = [];
        renderPosts();
      }}
    }}'''
    
    pattern = r'function clearPosts\(\) \{.*?\n\s+\}'
    content = re.sub(pattern, new_clear_posts, content, flags=re.DOTALL)
    
    # Guardar el archivo modificado
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {filename} actualizado con Firebase")

# Lista de paneles a actualizar
panels = [
    ('panel_blanca.html', 'Blanca'),
    ('panel_erwin.html', 'Erwin'),
    ('panel_jesus.html', 'Jesus'),
    ('panel_astrid.html', 'Astrid'),
    ('panel_patty.html', 'Patty')
]

# Aplicar cambios a todos los paneles
for filename, professor_name in panels:
    if os.path.exists(filename):
        add_firebase_to_panel(filename, professor_name)
    else:
        print(f"❌ {filename} no encontrado")

print("\n🎉 Migración completada. Todos los posts ahora se sincronizan con Firebase!")
