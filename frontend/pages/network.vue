<template>
  <section id="page-network">
    <div style="display:flex;justify-content:space-between;align-items:center; margin-bottom: 24px;">
      <div>
        <h2>Network & Feed</h2>
        <div class="muted">Finde Co-Investoren & Partner und verfolge die neuesten Updates.</div>
      </div>
      <div style="display:flex;gap:8px">
        <input 
          v-model="searchQuery" 
          placeholder="Suche Profile..." 
          style="padding:10px;border-radius:10px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.02);color:#fff" 
          @keyup.enter="filterProfiles"
        />
        <button class="btn ghost" @click="filterProfiles">Suchen</button>
      </div>
    </div>

    <div class="feed-container">
      
      <div class="posts-feed">
        <!-- Nachricht verfassen -->
        <div class="card create-post">
          <div class="post-header">
            <img :src="currentUserAvatar" class="avatar">
            <div style="flex: 1;">
              <textarea 
                v-model="newPostContent" 
                placeholder="Was gibt's Neues? Teile Updates mit deinem Netzwerk..."
                rows="3"
                style="width: 100%; padding: 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: white; font-family: inherit; resize: vertical;"
              ></textarea>
            </div>
          </div>
          <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
            <div style="display: flex; gap: 8px;">
              <button class="btn ghost" @click="alert('Bild hochladen (Demo)')">
                📷 Bild
              </button>
              <button class="btn ghost" @click="alert('Link einfügen (Demo)')">
                🔗 Link
              </button>
            </div>
            <button 
              class="btn primary" 
              @click="simulatePost"
              :disabled="!newPostContent.trim()"
            >
              Posten
            </button>
          </div>
        </div>

        <!-- Feed Posts -->
        <div v-for="post in posts" :key="post.id" class="card post">
          <div class="post-header">
            <img :src="getProfileByAuthor(post.author)?.img" class="avatar">
            <div>
              <strong>{{ post.author }}</strong>
              <div class="muted">{{ getProfileByAuthor(post.author)?.role }} · {{ post.timestamp }}</div>
            </div>
          </div>
          <p class="post-content">{{ post.content }}</p>
          <img v-if="post.image" :src="post.image" class="post-image">
          <div class="post-actions">
            <a class="action-item" @click="alert('Gefällt mir ')">
              <span>👍</span>
              <span>Gefällt mir </span>
            </a>

            <a class="action-item" @click="alert('Kommentar ')">
              <span>💬</span>
              <span>Kommentar </span>
            </a>

            <a class="action-item" @click="alert('Teilen ')">
              <span>🔗</span>
              <span>Teilen </span>
            </a>
          </div>
        </div>
      </div>
      
      <aside>
        <div class="card">
          <strong>Wichtige Profile</strong>
          <div class="muted" style="margin-top:4px; margin-bottom: 16px;">Rollenspezifische Matches:</div>
          
          <div class="sidebar-profiles">
            <div v-for="p in filteredProfiles" :key="p.id" class="sidebar-profile card">
            
            <img :src="p.img" class="avatar-rounded">

            <div class="profile-details">
              
              <div>
                <strong>{{ p.name }}</strong>
                <div class="muted">{{ p.role }} · {{ p.type }}</div>
              </div>

              <div class="tags" style="margin-top: 8px;">
                <div v-for="s in p.skills.slice(0, 2)" :key="s" class="tag">{{ s }}</div>
              </div>
              
              <div class="button-wrapper">
                <button class="btn ghost" @click="alert('Kontaktanfrage ')">Kontakt</button>
              </div>

            </div>
          </div>
          </div>
        </div>
      </aside>

    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

// Demo-Daten sind direkt im Code, um Fehler zu vermeiden
const alert = (msg) => window.alert(msg);

// Aktueller User (wird vom Backend geladen)
const currentUser = ref({ 
  username: '', 
  email: '', 
  role: ''
});

// Avatar URL basierend auf Username (wie auf Profil-Seite)
const currentUserAvatar = computed(() => {
  const seed = currentUser.value.username || 'user';
  return `https://api.dicebear.com/7.x/avataaars/svg?seed=${seed}`;
});

const currentUserName = computed(() => currentUser.value.username || 'Du');

// Neuer Post Content
const newPostContent = ref('');

const profiles = ref([
  { id: 1, name: 'EcoLogistics', img: 'https://picsum.photos/seed/ecologistics/200', role: 'Founder', type: 'Startup', bio: 'Logistikoptimierung für lokale Lieferketten.', skills: ['Logistics', 'SaaS', 'Sustainability'] },
  { id: 2, name: 'Anna Müller', img: 'https://picsum.photos/seed/annamueller/200', role: 'Angel', type: 'Investor', bio: 'Investiert in ClimateTech & Health.', skills: ['ClimateTech', 'Health', 'Seed'] },
  { id: 3, name: 'M&A Partner', img: 'https://picsum.photos/seed/mapartner/200', role: 'Advisor', type: 'Advisor', bio: 'Berät bei M&A & Transaktionen.', skills: ['M&A', 'Legal'] },
  { id: 4, name: 'FoodoraX', img: 'https://picsum.photos/seed/foodorax/200', role: 'Founder', type: 'Startup', bio: 'D2C Plattform für Food Brands.', skills: ['Marketing', 'D2C'] },
  { id: 5, name: 'SmartHome Energy', img: 'https://picsum.photos/seed/smarthome/200', role: 'Founder', type: 'Startup', bio: 'Energiemanagement für dein Zuhause.', skills: ['IoT', 'Energy', 'Hardware'] }
]);

const posts = ref([
  { id: 1, author: 'Anna Müller', timestamp: 'vor 2h', content: 'Habe gerade Medico kontaktiert! Ihr Fixed Deal ist sehr interessant.', image: null },
  { id: 2, author: 'SmartHome Energy', timestamp: 'vor 4h', content: 'Wir suchen einen Head of Sales in der DACH-Region! 🚀 Jetzt bewerben!', image: null}
]);

const searchQuery = ref('');

const filteredProfiles = computed(() => {
  const q = searchQuery.value.toLowerCase();
  if (!q) {
    return profiles.value;
  }
  return profiles.value.filter(p => 
    (p.name + p.bio + p.skills.join(' ')).toLowerCase().includes(q)
  );
});

const getProfileByAuthor = (authorName) => {
  return profiles.value.find(p => p.name === authorName);
};

function filterProfiles() {
  console.log('Profilsuche ausgeführt für:', searchQuery.value);
}

// User-Daten beim Laden der Seite holen
onMounted(async () => {
  const token = localStorage.getItem('access_token');
  if (token) {
    try {
      const res = await fetch('http://127.0.0.1:8000/api/users/me/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        currentUser.value.username = data.username || '';
        currentUser.value.email = data.email || '';
        currentUser.value.role = data.profile?.role || '';
      }
    } catch (e) {
      console.warn('Failed to load user data', e);
    }
  }
});

// Simuliert das Posten einer Nachricht
function simulatePost() {
  if (!newPostContent.value.trim()) return;
  
  // Neuen Post am Anfang der Liste hinzufügen
  posts.value.unshift({
    id: Date.now(),
    author: currentUserName.value,
    timestamp: 'Gerade eben',
    content: newPostContent.value,
    image: null
  });
  
  // Eingabefeld leeren
  newPostContent.value = '';
}
</script>

<style scoped>
/* Create Post Card */
.create-post {
  margin-bottom: 24px;
  background: linear-gradient(135deg, rgba(94, 234, 212, 0.05), rgba(168, 85, 247, 0.05));
  border: 1px solid rgba(94, 234, 212, 0.2);
}

.create-post textarea {
  transition: all 0.2s;
}

.create-post textarea:focus {
  outline: none;
  border-color: var(--accent);
  background: rgba(255, 255, 255, 0.08);
}

.create-post .btn.primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Feed Container */
.feed-container {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  align-items: start;
}

.posts-feed {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Post Styles */
.post {
  padding: 20px;
}

.post-header {
  display: flex;
  gap: 12px;
  align-items: center;
  margin-bottom: 12px;
}

.avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--accent);
}

.post-content {
  margin: 12px 0;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.post-image {
  width: 100%;
  border-radius: 12px;
  margin-top: 12px;
  max-height: 400px;
  object-fit: cover;
}

.post-actions {
  display: flex;
  gap: 16px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.action-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--muted);
  font-size: 0.9rem;
}

.action-item:hover {
  background: rgba(255, 255, 255, 0.05);
  color: white;
}

/* Sidebar Profiles */
.sidebar-profiles {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.sidebar-profile {
  display: flex;
  gap: 12px;
  padding: 12px;
  transition: all 0.2s;
}

.sidebar-profile:hover {
  background: rgba(255, 255, 255, 0.03);
  transform: translateX(4px);
}

.avatar-rounded {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  object-fit: cover;
  border: 2px solid var(--accent);
}

.profile-details {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.tag {
  padding: 4px 10px;
  background: rgba(94, 234, 212, 0.1);
  border: 1px solid rgba(94, 234, 212, 0.3);
  border-radius: 12px;
  font-size: 0.75rem;
  color: var(--accent);
}

.button-wrapper {
  margin-top: auto;
}

/* Responsive */
@media (max-width: 968px) {
  .feed-container {
    grid-template-columns: 1fr;
  }
  
  aside {
    order: -1;
  }
}
</style>