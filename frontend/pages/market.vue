<template>
  <section id="page-market">
    <div style="display:flex;justify-content:space-between;align-items:center;gap:12px">
      <div>
        <h2>Marktplatz</h2>
        <div class="muted">Vollständige Listings mit KPIs & Aktionen (Demo-Daten).</div>
      </div>
      <div style="display:flex;gap:8px;align-items:center">
        <input 
          v-model="searchTerm" 
          placeholder="Suchen nach Name, Branche..." 
          style="padding:10px;border-radius:10px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.02);color:#fff" 
          @keyup.enter="filterList"
        />
        <button class="btn ghost" @click="filterList">Suchen</button>
      </div>
    </div>

    <div style="margin-top:14px">
      <div class="list">
        <div v-for="s in filteredStartups" :key="s.id" class="pitch">
          <div class="meta">
            <div>
              <strong>{{ s.title }}</strong>
              <div class="muted">{{ s.sector }} · {{ s.stage }}</div>
            </div>
            <div style="text-align:right">
              <div class="tag">{{ s.equity }} · {{ s.goal }}</div>
            </div>
          </div>
          <img :src="s.img" :alt="s.title">
          <div style="display:flex;justify-content:space-between;align-items:center;gap:12px">
            <div class="muted" style="flex:1">{{ s.desc }}</div>
            <div style="flex-basis:220px;text-align:right">
              <div class="muted">Valuation: {{ s.kpis?.valuation || '—' }}</div>
            </div>
          </div>
          <div style="display:flex;gap:8px;margin-top:8px;justify-content:flex-end">
            <NuxtLink :to="`/detail/${s.id}`" class="btn ghost">Details</NuxtLink>
            <button class="btn primary" @click="dummyApi('/api/action?startup=' + s.id + '&role=' + currentRole)">
              {{ actionLabel }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue';
import { startups, useRole, dummyApi } from '~/composables/useDemoData';

const currentRole = useRole();
const searchTerm = ref('');

const filteredStartups = computed(() => {
  const term = searchTerm.value.toLowerCase();
  return startups.filter(s => 
    (s.title + s.desc + s.sector + s.stage).toLowerCase().includes(term)
  );
});

const actionLabel = computed(() => {
  return currentRole.value === 'investor' ? 'Investieren' : 'Pitch bearbeiten';
});

function filterList() {
  console.log('Suche ausgeführt für:', searchTerm.value);
}

useHead({
  title: 'Marktplatz - investify'
});
</script>