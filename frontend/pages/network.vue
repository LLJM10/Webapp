<template>
  <section id="page-network">
    <div style="display:flex;justify-content:space-between;align-items:center">
      <div>
        <h2>Networking</h2>
        <div class="muted">Finde Co-Investoren, Berater & Partner — Profile rollenbasiert hervorgehoben.</div>
      </div>
      <div style="display:flex;gap:8px">
        <input 
          v-model="searchQuery" 
          placeholder="Suche..." 
          style="padding:10px;border-radius:10px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.02);color:#fff" 
          @keyup.enter="filterProfiles"
        />
        <button class="btn ghost" @click="filterProfiles">Suchen</button>
      </div>
    </div>

    <div style="margin-top:12px" class="profiles">
      <div v-for="p in filteredProfiles" :key="p.id" class="card" :style="{ border: getHighlightStyle(p.type) }">
        <div style="display:flex;gap:12px;align-items:center">
          <img :src="p.img" style="width:64px;height:64px;border-radius:8px;object-fit:cover">
          <div style="flex:1">
            <strong>{{ p.name }}</strong>
            <div class="muted">{{ p.role }} · {{ p.type }}</div>
            <div class="muted" style="margin-top:6px">{{ p.bio }}</div>
            <div style="margin-top:8px;display:flex;gap:8px;flex-wrap:wrap">
              <div v-for="s in p.skills" :key="s" class="tag">{{ s }}</div>
            </div>
          </div>
          <div style="display:flex;flex-direction:column;gap:8px">
            <button class="btn ghost" @click="dummyApi('/api/contact?to='+p.id)">Kontakt</button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue';
import { profiles, useRole, dummyApi } from '~/composables/useDemoData';

const currentRole = useRole();
const searchQuery = ref('');

const filteredProfiles = computed(() => {
  const q = searchQuery.value.toLowerCase();
  return profiles.filter(p => 
    (p.name + p.bio + p.skills.join(' ')).toLowerCase().includes(q)
  );
});

// Logik für die Rollen-basierte Hervorhebung
const getHighlightStyle = (profileType) => {
  const highlight = (currentRole.value === 'investor' && profileType === 'Startup') || 
                    (currentRole.value === 'startup' && profileType === 'Investor');
  return highlight ? '1px solid rgba(96,165,250,0.25)' : '1px solid rgba(255,255,255,0.02)';
};

function filterProfiles() {
  console.log('Suche im Netzwerk ausgeführt für:', searchQuery.value);
}
</script>