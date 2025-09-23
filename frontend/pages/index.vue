<template>
  <div class="h-full bg-gray-100 scroll-smooth text-gray-800">

    <header class="bg-white shadow-md sticky top-0 z-40">
      <div class="container mx-auto px-4">
        <div class="flex justify-between items-center py-3">
          <a href="#" @click.prevent="navigateTo('marketplace-view')" class="text-2xl font-bold text-indigo-600">INVESTIFY</a>
          <div class="flex items-center space-x-4">
            <div class="relative">
              <label for="role-switcher" class="text-sm font-medium sr-only">Rolle wechseln</label>
              <select id="role-switcher" @change="switchRole($event.target.value)" class="pl-3 pr-8 py-2 text-sm font-medium bg-gray-100 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option value="INVESTOR">Investor</option>
                <option value="COMPANY">Firma</option>
                <option value="ADMIN">Admin</option>
              </select>
            </div>
            <nav id="main-nav" class="hidden md:flex items-center space-x-2"></nav>
          </div>
        </div>
      </div>
    </header>

    <main id="app-container" class="container mx-auto p-4 md:p-6">
      
      <section id="marketplace-view" class="view active">
        <h1 class="text-3xl font-bold mb-6">Aktive Pitches</h1>
        <div id="pitch-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
      </section>

      <section id="pitch-detail-view" class="view"></section>

      <section id="company-dashboard-view" class="view"></section>
      
      <section id="investor-dashboard-view" class="view"></section>

      <section id="admin-dashboard-view" class="view">
        <h1 class="text-3xl font-bold mb-6">Admin Dashboard</h1>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h2 class="text-xl font-semibold mb-4">Neue Pitches & User pro Woche</h2>
            <canvas id="registrationsChart"></canvas>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h2 class="text-xl font-semibold mb-4">Investitionsvolumen pro Branche</h2>
            <canvas id="investmentChart"></canvas>
          </div>
        </div>
        <div class="mt-8 bg-white p-6 rounded-lg shadow-md">
          <h2 class="text-xl font-semibold mb-4">Neueste Pitches zur Moderation</h2>
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Pitch</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  <th class="px-6 py-3 text-center text-xs font-medium text-gray-500 uppercase">Aktionen</th>
                </tr>
              </thead>
              <tbody id="moderation-table" class="bg-white divide-y divide-gray-200"></tbody>
            </table>
          </div>
        </div>
      </section>

    </main>
    
    <div id="ai-analysis-modal" class="modal-overlay fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 hidden" @click="closeModal('ai-analysis-modal')">
      <div class="modal-container bg-white rounded-lg shadow-2xl w-full max-w-lg p-6 transform opacity-0 -translate-y-10" @click.stop>
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-2xl font-bold text-gray-900 flex items-center">
            <svg data-lucide="brain-circuit" class="mr-2 text-indigo-500"></svg>
            Pitch-Analyse
          </h2>
          <button @click="closeModal('ai-analysis-modal')" class="text-gray-400 hover:text-gray-600">&times;</button>
        </div>
        <div id="ai-analysis-content" class="text-gray-700 space-y-4">
          <p class="text-center py-8">Analysiere Pitch... <span class="animate-spin inline-block ml-2">.</span></p>
        </div>
      </div>
    </div>
    
    <div id="chat-modal" class="modal-overlay fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 hidden" @click="closeModal('chat-modal')">
      <div class="modal-container bg-white rounded-lg shadow-2xl w-full max-w-2xl h-[70vh] flex flex-col transform opacity-0 -translate-y-10" @click.stop>
        <div class="flex justify-between items-center p-4 border-b">
          <h2 id="chat-with-name" class="text-xl font-bold text-gray-900">Chat mit...</h2>
          <button @click="closeModal('chat-modal')" class="text-gray-400 hover:text-gray-600">&times;</button>
        </div>
        <div id="chat-messages" class="flex-1 p-4 overflow-y-auto custom-scrollbar space-y-4 bg-gray-50">
          <div class="flex justify-start">
            <div class="bg-gray-200 rounded-lg p-3 max-w-xs">Guten Tag, ich habe Ihren Pitch gesehen und bin sehr interessiert.</div>
          </div>
          <div class="flex justify-end">
            <div class="bg-indigo-500 text-white rounded-lg p-3 max-w-xs">Vielen Dank für Ihr Interesse! Was möchten Sie wissen?</div>
          </div>
          <div class="flex justify-start">
            <div class="bg-gray-200 rounded-lg p-3 max-w-xs">Können Sie mir mehr über Ihre Wachstumsstrategie für die nächsten 2 Jahre erzählen?</div>
          </div>
        </div>
        <div class="p-4 border-t bg-white">
          <div class="relative">
            <input type="text" placeholder="Nachricht schreiben..." class="w-full pl-4 pr-12 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <button class="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-full bg-indigo-500 text-white hover:bg-indigo-600">
              <svg data-lucide="send-horizontal"></svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, nextTick } from 'vue';
import Chart from 'chart.js/auto';
import lucide from 'lucide-dev';

// Application state
const state = reactive({
  currentRole: 'INVESTOR',
  pitches: [],
  users: [],
  bids: [],
  activePitchId: null,
});

// --- DATA SIMULATION ---
const generateMockData = () => {
  state.users = [
    { id: 1, name: 'EcoSolutions GmbH', role: 'COMPANY', profilePic: 'https://placehold.co/100x100/22c55e/ffffff?text=ES' },
    { id: 2, name: 'FutureTech AG', role: 'COMPANY', profilePic: 'https://placehold.co/100x100/3b82f6/ffffff?text=FT' },
    { id: 3, name: 'HealthInnovate', role: 'COMPANY', profilePic: 'https://placehold.co/100x100/ef4444/ffffff?text=HI' },
    { id: 4, name: 'QuantumLeap VC', role: 'INVESTOR' },
    { id: 5, name: 'Green Growth Capital', role: 'INVESTOR' },
  ];
  state.pitches = [
    { id: 101, companyId: 1, title: 'Nachhaltige Verpackungslösung', description: 'Revolutionäre, biologisch abbaubare Verpackung aus Algen. Reduziert Plastikmüll um 95%. Suchen Kapital für Skalierung der Produktion.', videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ', status: 'active', requiredCapital: 500000, industry: 'GreenTech' },
    { id: 102, companyId: 2, title: 'KI-gestützte Logistikplattform', description: 'Unsere KI optimiert Lieferketten in Echtzeit, senkt Kosten um 30% und CO2-Emissionen um 20%. Etablierte Kundenbasis im DACH-Raum.', videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ', status: 'active', requiredCapital: 1200000, industry: 'SaaS' },
    { id: 103, companyId: 3, title: 'Telemedizin-App für Senioren', description: 'Einfach bedienbare App, die Senioren mit Ärzten verbindet. Inklusive Medikamenten-Erinnerung und Notfall-Funktion.', videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ', status: 'funded', requiredCapital: 750000, industry: 'HealthTech' },
  ];
  state.bids = [
    { id: 1, pitchId: 101, investorId: 4, amount: 50000, equity: 5.0, status: 'pending' },
    { id: 2, pitchId: 101, investorId: 5, amount: 75000, equity: 7.0, status: 'pending' },
    { id: 3, pitchId: 102, investorId: 4, amount: 200000, equity: 10.0, status: 'accepted' },
  ];
};

// --- VIEW & NAVIGATION MANAGEMENT ---
const switchRole = (newRole) => {
  state.currentRole = newRole;
  updateNavigation();
  if (newRole === 'INVESTOR') navigateTo('marketplace-view');
  else if (newRole === 'COMPANY') navigateTo('company-dashboard-view');
  else if (newRole === 'ADMIN') navigateTo('admin-dashboard-view');
};

const updateNavigation = () => {
  const nav = document.getElementById('main-nav');
  const role = state.currentRole;
  let links = `<a href="#" @click.prevent="navigateTo('marketplace-view')" class="text-gray-700 hover:bg-gray-200 px-3 py-2 rounded-md text-sm font-medium">Marktplatz</a>`;
  if (role === 'INVESTOR') {
    links += `<a href="#" @click.prevent="navigateTo('investor-dashboard-view')" class="text-gray-700 hover:bg-gray-200 px-3 py-2 rounded-md text-sm font-medium">Dashboard</a>`;
  } else if (role === 'COMPANY') {
    links += `<a href="#" @click.prevent="navigateTo('company-dashboard-view')" class="text-gray-700 hover:bg-gray-200 px-3 py-2 rounded-md text-sm font-medium">Mein Pitch</a>`;
  } else if (role === 'ADMIN') {
    links += `<a href="#" @click.prevent="navigateTo('admin-dashboard-view')" class="text-gray-700 hover:bg-gray-200 px-3 py-2 rounded-md text-sm font-medium">Admin Panel</a>`;
  }
  nav.innerHTML = links;
  nextTick(() => {
    lucide.createIcons();
  });
};

const navigateTo = (viewId) => {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.getElementById(viewId).classList.add('active');
  window.scrollTo(0, 0);
};

// --- RENDER FUNCTIONS ---
const renderMarketplace = () => {
  const grid = document.getElementById('pitch-grid');
  grid.innerHTML = state.pitches
    .filter(p => p.status === 'active')
    .map(pitch => {
      const company = state.users.find(u => u.id === pitch.companyId);
      const bids = state.bids.filter(b => b.pitchId === pitch.id);
      const highestBid = bids.length ? Math.max(...bids.map(b => b.amount)) : 0;
      
      return `
        <div class="bg-white rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 cursor-pointer" @click="renderPitchDetail(${pitch.id})">
          <div class="p-5">
            <div class="flex items-center mb-4">
              <img src="${company.profilePic}" alt="Logo" class="w-12 h-12 rounded-full mr-4">
              <div>
                <h3 class="font-bold text-lg text-gray-900">${pitch.title}</h3>
                <p class="text-sm text-gray-500">${company.name}</p>
              </div>
            </div>
            <p class="text-gray-600 text-sm mb-4 h-16">${pitch.description.substring(0, 120)}...</p>
            <div class="flex justify-between items-center pt-4 border-t border-gray-100">
              <span class="text-sm text-gray-500">Höchstgebot</span>
              <span class="font-bold text-indigo-600 text-lg">$${highestBid.toLocaleString()}</span>
            </div>
          </div>
        </div>
      `;
    }).join('');

  document.querySelectorAll('#pitch-grid div').forEach(el => {
    const id = el.getAttribute('onclick').match(/\d+/)[0];
    el.addEventListener('click', () => renderPitchDetail(parseInt(id)));
    el.removeAttribute('onclick');
  });
};

const renderPitchDetail = (pitchId) => {
  state.activePitchId = pitchId;
  const pitch = state.pitches.find(p => p.id === pitchId);
  const company = state.users.find(u => u.id === pitch.companyId);
  const container = document.getElementById('pitch-detail-view');

  container.innerHTML = `
    <div class="bg-white p-6 md:p-8 rounded-lg shadow-lg">
      <div class="flex justify-between items-start mb-6">
        <div>
          <h1 class="text-3xl md:text-4xl font-extrabold text-gray-900">${pitch.title}</h1>
          <p class="text-lg text-gray-500 mt-1">von ${company.name}</p>
        </div>
        <button @click="navigateTo('marketplace-view')" class="text-indigo-600 hover:text-indigo-800 font-medium flex items-center">
          <svg data-lucide="arrow-left" class="w-4 h-4 mr-2"></svg>
          Zurück
        </button>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2">
          <div class="aspect-w-16 aspect-h-9 mb-6 rounded-lg overflow-hidden bg-black">
            <iframe src="${pitch.videoUrl}" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen class="w-full h-full"></iframe>
          </div>
          <h2 class="text-2xl font-bold mb-3">Ausführliche Beschreibung</h2>
          <p class="text-gray-700 leading-relaxed">${pitch.description}</p>
        </div>
        <div class="lg:col-span-1 space-y-6">
          <div class="bg-gray-50 p-5 rounded-lg">
            <h2 class="text-xl font-bold mb-4">Angebot abgeben</h2>
            ${state.currentRole === 'INVESTOR' ? getBidFormTemplate() : `<p class="text-sm text-center text-gray-500 p-4 bg-gray-100 rounded-md">Loggen Sie sich als Investor ein, um ein Gebot abzugeben.</p>`}
          </div>
          <div class="bg-gray-50 p-5 rounded-lg">
            <h2 class="text-xl font-bold mb-4">Aktuelle Gebote</h2>
            <div id="bids-list" class="space-y-3 max-h-96 overflow-y-auto custom-scrollbar pr-2">
              ${getBidsListTemplate(pitchId)}
            </div>
          </div>
        </div>
      </div>
    </div>
  `;
  navigateTo('pitch-detail-view');
  nextTick(() => {
    lucide.createIcons();
    if (state.currentRole === 'INVESTOR') {
      document.getElementById('bid-form').addEventListener('submit', handleBidSubmit);
    }
  });
};

const getBidFormTemplate = () => {
  return `
    <form id="bid-form" class="space-y-4">
      <div>
        <label for="amount" class="block text-sm font-medium text-gray-700">Investitionssumme ($)</label>
        <input type="number" id="amount" name="amount" required class="mt-1 w-full p-2 border rounded-md" placeholder="z.B. 50000">
      </div>
      <div>
        <label for="equity" class="block text-sm font-medium text-gray-700">Anteil (%)</label>
        <input type="number" id="equity" name="equity" step="0.1" required class="mt-1 w-full p-2 border rounded-md" placeholder="z.B. 5.5">
      </div>
      <button type="submit" class="w-full bg-indigo-600 text-white font-bold py-2 px-4 rounded-md hover:bg-indigo-700 transition-colors">Gebot abgeben</button>
    </form>
  `;
};

const getBidsListTemplate = (pitchId) => {
  const bids = state.bids.filter(b => b.pitchId === pitchId).sort((a,b) => b.amount - a.amount);
  if (!bids.length) return `<p class="text-sm text-center text-gray-500 p-4">Noch keine Gebote.</p>`;
  
  return bids.map(bid => {
    const investor = state.users.find(u => u.id === bid.investorId);
    return `
      <div class="bg-white p-3 rounded-md border">
        <div class="flex justify-between items-center text-sm">
          <p class="font-semibold text-gray-800">${investor.name}</p>
          <span class="text-xs text-gray-400">vor 5 Min.</span>
        </div>
        <p class="font-bold text-gray-900 mt-1">$${bid.amount.toLocaleString()} für ${bid.equity}%</p>
        <div class="text-right mt-1">
          <span class="px-2 py-0.5 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800">${bid.status}</span>
        </div>
      </div>
    `;
  }).join('');
};

const renderDashboards = () => {
  const companyPitch = state.pitches.find(p => p.companyId === 2);
  if (companyPitch) {
    const companyBids = state.bids.filter(b => b.pitchId === companyPitch.id);
    document.getElementById('company-dashboard-view').innerHTML = getCompanyDashboardTemplate(companyPitch, companyBids);
    nextTick(() => {
      const aiButton = document.querySelector('#company-dashboard-view button[onclick]');
      if (aiButton) {
        aiButton.addEventListener('click', openAiAnalysisModal);
      }
    });
  }
  const investorBids = state.bids.filter(b => b.investorId === 4);
  document.getElementById('investor-dashboard-view').innerHTML = getInvestorDashboardTemplate(investorBids);
  renderAdminDashboard();
};

const getCompanyDashboardTemplate = (pitch, bids) => {
  const highestBid = bids.length ? Math.max(...bids.map(b => b.amount)) : 0;
  return `
    <h1 class="text-3xl font-bold mb-6">Mein Pitch Dashboard</h1>
    <div class="bg-white p-6 rounded-lg shadow-md">
      <h2 class="text-2xl font-bold">${pitch.title}</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6 text-center">
        <div><p class="text-gray-500">Status</p><p class="font-bold text-2xl text-green-600">${pitch.status.toUpperCase()}</p></div>
        <div><p class="text-gray-500">Anz. Gebote</p><p class="font-bold text-2xl">${bids.length}</p></div>
        <div><p class="text-gray-500">Höchstgebot</p><p class="font-bold text-2xl text-indigo-600">$${highestBid.toLocaleString()}</p></div>
        <div class="flex items-center justify-center">
          <button @click="openAiAnalysisModal()" class="bg-indigo-100 text-indigo-700 font-semibold py-2 px-4 rounded-lg flex items-center hover:bg-indigo-200">
            <svg data-lucide="brain-circuit" class="w-5 h-5 mr-2"></svg>
            KI-Analyse starten
          </button>
        </div>
      </div>
    </div>
    <div class="mt-8">
      <h3 class="text-2xl font-bold mb-4">Eingegangene Gebote</h3>
      <div class="bg-white rounded-lg shadow-md p-4 space-y-3">
        ${bids.map(bid => {
          const investor = state.users.find(u => u.id === bid.investorId);
          return `
            <div class="border rounded-lg p-4 flex flex-col md:flex-row justify-between items-center">
              <div>
                <p class="font-bold text-lg">$${bid.amount.toLocaleString()} für ${bid.equity}%</p>
                <p class="text-sm text-gray-600">von ${investor.name}</p>
              </div>
              <div class="flex items-center space-x-2 mt-4 md:mt-0">
                <button @click="openChatModal('${investor.name}')" class="bg-gray-200 text-gray-700 px-3 py-1 rounded-md text-sm font-medium hover:bg-gray-300">Chat</button>
                <button class="bg-red-100 text-red-700 px-3 py-1 rounded-md text-sm font-medium hover:bg-red-200">Ablehnen</button>
                <button class="bg-green-100 text-green-700 px-3 py-1 rounded-md text-sm font-medium hover:bg-green-200">Annehmen</button>
              </div>
            </div>`;
        }).join('')}
      </div>
    </div>
  `;
};

const getInvestorDashboardTemplate = (bids) => {
  return `
    <h1 class="text-3xl font-bold mb-6">Investor Dashboard</h1>
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2">
        <h2 class="text-2xl font-bold mb-4">Meine abgegebenen Gebote</h2>
        <div class="bg-white rounded-lg shadow-md p-4 space-y-3">
          ${bids.map(bid => {
            const pitch = state.pitches.find(p => p.id === bid.pitchId);
            return `
              <div class="border rounded-lg p-4 flex justify-between items-center">
                <div>
                  <p class="font-bold text-lg">$${bid.amount.toLocaleString()} für ${bid.equity}%</p>
                  <p class="text-sm text-gray-600">auf "${pitch.title}"</p>
                </div>
                <span class="px-3 py-1 text-sm font-semibold rounded-full ${bid.status === 'accepted' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}">${bid.status}</span>
              </div>`;
          }).join('')}
        </div>
      </div>
      <div>
        <h2 class="text-2xl font-bold mb-4">KI-Empfehlungen</h2>
        <div class="bg-white rounded-lg shadow-md p-4 space-y-3">
          ${state.pitches.filter(p=>p.id !== 102).map(pitch => `
            <div class="border rounded-lg p-3 hover:bg-gray-50 cursor-pointer" @click="renderPitchDetail(${pitch.id})">
              <p class="font-bold">${pitch.title}</p>
              <p class="text-xs text-gray-500">${pitch.industry}</p>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
  `;
};

const renderAdminDashboard = () => {
  const tableBody = document.getElementById('moderation-table');
  tableBody.innerHTML = state.pitches.map(p => `
    <tr>
      <td class="px-6 py-4 whitespace-nowrap">
        <div class="font-medium text-gray-900">${p.title}</div>
        <div class="text-sm text-gray-500">${state.users.find(u=>u.id === p.companyId).name}</div>
      </td>
      <td class="px-6 py-4 whitespace-nowrap">
        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${p.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}">${p.status}</span>
      </td>
      <td class="px-6 py-4 whitespace-nowrap text-center text-sm font-medium space-x-2">
        <button class="text-indigo-600 hover:text-indigo-900">Ansehen</button>
        <button class="text-green-600 hover:text-green-900">Freigeben</button>
        <button class="text-red-600 hover:text-red-900">Sperren</button>
      </td>
    </tr>
  `).join('');
  initAdminCharts();
};

const handleBidSubmit = (event) => {
  event.preventDefault();
  const form = event.target;
  const newBid = {
    id: Date.now(),
    pitchId: state.activePitchId,
    investorId: 4,
    amount: parseFloat(form.amount.value),
    equity: parseFloat(form.equity.value),
    status: 'pending'
  };
  state.bids.push(newBid);
  nextTick(() => {
    const bidsList = document.getElementById('bids-list');
    if (bidsList) {
      bidsList.innerHTML = getBidsListTemplate(state.activePitchId);
    }
  });
  form.reset();
};

const openModal = (modalId) => {
  const modal = document.getElementById(modalId);
  modal.classList.remove('hidden');
  setTimeout(() => {
    modal.querySelector('.modal-container').classList.remove('opacity-0', '-translate-y-10');
  }, 10);
};

const closeModal = (modalId) => {
  const modal = document.getElementById(modalId);
  modal.querySelector('.modal-container').classList.add('opacity-0', '-translate-y-10');
  setTimeout(() => modal.classList.add('hidden'), 300);
};

const openAiAnalysisModal = () => {
  openModal('ai-analysis-modal');
  const content = document.getElementById('ai-analysis-content');
  content.innerHTML = `<p class="text-center py-8">Analysiere Pitch... <span class="animate-spin inline-block ml-2">.</span></p>`;
  
  setTimeout(() => {
    content.innerHTML = `
      <div class="space-y-3">
        <div class="flex items-start p-3 bg-green-50 border-l-4 border-green-500 rounded-r-lg">
          <svg data-lucide="check-circle-2" class="text-green-600 w-5 h-5 mr-3 mt-1 flex-shrink-0"></svg>
          <div><h4 class="font-semibold">Starke Einleitung</h4><p class="text-sm">Der erste Absatz beschreibt das Problem klar und verständlich.</p></div>
        </div>
        <div class="flex items-start p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded-r-lg">
          <svg data-lucide="alert-triangle" class="text-yellow-600 w-5 h-5 mr-3 mt-1 flex-shrink-0"></svg>
          <div><h4 class="font-semibold">Verbesserungsvorschlag</h4><p class="text-sm">Quantifizieren Sie den Markt. Fügen Sie konkrete Zahlen zur Marktgröße und zum Wachstumspotenzial hinzu.</p></div>
        </div>
        <div class="flex items-start p-3 bg-yellow-50 border-l-4 border-yellow-500 rounded-r-lg">
          <svg data-lucide="alert-triangle" class="text-yellow-600 w-5 h-5 mr-3 mt-1 flex-shrink-0"></svg>
          <div><h4 class="font-semibold">Verbesserungsvorschlag</h4><p class="text-sm">Heben Sie das Team stärker hervor. Beschreiben Sie kurz die Kernkompetenzen der Gründer.</p></div>
        </div>
      </div>
    `;
    lucide.createIcons();
  }, 1500);
};

const openChatModal = (partnerName) => {
  document.getElementById('chat-with-name').innerText = `Chat mit ${partnerName}`;
  openModal('chat-modal');
};

const initAdminCharts = () => {
  if (window.registrationsChartInstance) window.registrationsChartInstance.destroy();
  if (window.investmentChartInstance) window.investmentChartInstance.destroy();

  const regCtx = document.getElementById('registrationsChart').getContext('2d');
  window.registrationsChartInstance = new Chart(regCtx, {
    type: 'line',
    data: {
      labels: ['Woche -3', 'Woche -2', 'Letzte Woche', 'Diese Woche'],
      datasets: [
        { label: 'Neue Pitches', data: [5, 8, 12, 9], borderColor: 'rgb(75, 192, 192)', tension: 0.1 },
        { label: 'Neue User', data: [20, 25, 40, 32], borderColor: 'rgb(255, 99, 132)', tension: 0.1 }
      ]
    }
  });

  const invCtx = document.getElementById('investmentChart').getContext('2d');
  window.investmentChartInstance = new Chart(invCtx, {
    type: 'bar',
    data: {
      labels: ['GreenTech', 'SaaS', 'HealthTech', 'FinTech'],
      datasets: [{ label: 'Investitionsvolumen ($)', data: [575000, 1200000, 750000, 450000], backgroundColor: 'rgba(75, 192, 192, 0.6)' }]
    },
    options: { indexAxis: 'y' }
  });
};

const render = () => {
  updateNavigation();
  renderMarketplace();
  renderDashboards();
};

onMounted(() => {
  generateMockData();
  render();
  lucide.createIcons();
});
</script>

<style>
/* Custom styles for a polished look */
body {
  font-family: 'Inter', sans-serif;
}
@import url('https://rsms.me/inter/inter.css');

/* Smooth transitions for view switching */
.view {
  display: none;
  animation: fadeIn 0.5s ease-in-out;
}
.view.active {
  display: block;
}
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Modal styles */
.modal-overlay {
  transition: opacity 0.3s ease;
}
.modal-container {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

/* Custom scrollbar for chat */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f5f9;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #94a3b8;
  border-radius: 3px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #64748b;
}
</style>