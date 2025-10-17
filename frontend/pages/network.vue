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
            <a class="action-item" @click="alert('Gefällt mir (Demo)')">
              <span>👍</span>
              <span>Gefällt mir (Demo)</span>
            </a>

            <a class="action-item" @click="alert('Kommentar (Demo)')">
              <span>💬</span>
              <span>Kommentar (Demo)</span>
            </a>

            <a class="action-item" @click="alert('Teilen (Demo)')">
              <span>🔗</span>
              <span>Teilen (Demo)</span>
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
                <button class="btn ghost" @click="alert('Kontaktanfrage (Demo)')">Kontakt</button>
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
import { ref, computed } from 'vue';

// Demo-Daten sind direkt im Code, um Fehler zu vermeiden
const alert = (msg) => window.alert(msg);

const profiles = ref([
  { id: 1, name: 'EcoLogistics', img: null, role: 'Founder', type: 'Startup', bio: 'Logistikoptimierung für lokale Lieferketten.', skills: ['Logistics', 'SaaS', 'Sustainability'] },
  { id: 2, name: 'Anna Müller', img: null, role: 'Angel', type: 'Investor', bio: 'Investiert in ClimateTech & Health.', skills: ['ClimateTech', 'Health', 'Seed'] },
  { id: 3, name: 'M&A Partner', img: null, role: 'Advisor', type: 'Advisor', bio: 'Berät bei M&A & Transaktionen.', skills: ['M&A', 'Legal'] },
  { id: 4, name: 'FoodoraX', img: null, role: 'Founder', type: 'Startup', bio: 'D2C Plattform für Food Brands.', skills: ['Marketing', 'D2C'] },
  { id: 5, name: 'SmartHome Energy', img: null, role: 'Founder', type: 'Startup', bio: 'Energiemanagement für dein Zuhause.', skills: ['IoT', 'Energy', 'Hardware'] }
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
</script>