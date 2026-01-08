// composables/useDemoData.js

// Importiert Nuxt's State Management (wichtig für useRole)
import { useState } from '#app'; 

// ------------------------------------
// --- GLOBAL STATE & UTILITIES (EXPORTS) ---
// ------------------------------------

/**
 * Globaler State für die aktuelle Benutzerrolle ('startup' oder 'investor').
 * Verwendung: const currentRole = useRole();
 */
export const useRole = () => useState('currentRole', () => 'startup'); 

/**
 * Kapitalisiert den ersten Buchstaben eines Strings.
 */
export const capitalize = (s) => s.charAt(0).toUpperCase() + s.slice(1);

/**
 * Dummy-Funktion zur Simulation von API-Aufrufen.
 */
export function dummyApi(endpoint){
  alert('Dummy API Call: ' + endpoint);
  console.log('Dummy API ->', endpoint);
}


// DEMO DATEN FÜR STARTUPS, PROFILE, EVENTS

export const startups = [
  { 
    id:'s1', 
    title:'SmartHome Energy', 
    sector:'Energy', 
    stage:'Seed', 
    desc:'Dezentrale Energieoptimierung für Privathaushalte mittels Edge-AI und Lastverschiebung.', 
    img:'https://picsum.photos/seed/s1/900/480', 
    kpis:{revenue:'420k€ TTM', growth:'+72% YoY', customers:'1.2k', valuation:'5M€'}, 
    traction:'Pilot in 3 Städten', 
    market:'DACH', 
    goal:'400k€', 
    equity:'8%'
  },
  { 
    id:'s2', 
    title:'GreenCharge', 
    sector:'AI', 
    stage:'Series A', 
    desc:'Batterie-Management für EV-Flotten mit optimierter Ladeplanung und Flotten-Analytics.', 
    img:'https://picsum.photos/seed/s2/900/480', 
    kpis:{revenue:'1.1M€ TTM', growth:'+120% YoY', customers:'35 fleets', valuation:'20M€'}, 
    traction:'Verträge mit 2 großen Flottenbetreibern', 
    market:'EU', 
    goal:'2.5M€', 
    equity:'12%'
  },
  { 
    id:'s3', 
    title:'Medico', 
    sector:'Health', 
    stage:'Seed', 
    desc:'Telehealth für chronisch Kranke mit KI-Triage & Adhärenz-Programmen.', 
    img:'https://picsum.photos/seed/s3/900/480', 
    kpis:{revenue:'320k€ TTM', growth:'+48% YoY', customers:'4k', valuation:'4.5M€'}, 
    traction:'Pilot mit Klinikgruppe; 85% Retention', 
    market:'EU', 
    goal:'500k€', 
    equity:'6%'
  },
  { 
    id:'s4', 
    title:'OrbitSense', 
    sector:'SpaceTech', 
    stage:'Pre-Seed', 
    desc:'Low-cost Sensor-Satellites zur Erfassung von Luftqualität & Emissionen.', 
    img:'https://picsum.photos/seed/s4/900/480', 
    kpis:{revenue:'—', growth:'—', customers:'2 research projects', valuation:'5.3M€'}, 
    traction:'1 Test-Sat in LEO erfolgreich', 
    market:'Global', 
    goal:'800k€', 
    equity:'15%'
  }
];

export const profiles = [
  { id:'p1', type:'Startup', name:'EcoLogistics', role:'Founder', img:'https://picsum.photos/seed/p1/240/240', bio:'Logistikoptimierung für lokale Lieferketten.', skills:['Logistics','SaaS','Sustainability']},
  { id:'p2', type:'Investor', name:'Anna Müller', role:'Angel', img:'https://picsum.photos/seed/p2/240/240', bio:'Investiert in ClimateTech & Health.', skills:['ClimateTech','Health','Seed']},
  { id:'p3', type:'Advisor', name:'M&A Partner', role:'Advisor', img:'https://picsum.photos/seed/p3/240/240', bio:'Berät bei M&A & Transaktionen.', skills:['M&A','Legal']},
  { id:'p4', type:'Startup', name:'FoodoraX', role:'Founder', img:'https://picsum.photos/seed/p4/240/240', bio:'D2C Plattform für Food Brands.', skills:['Marketing','D2C']}
];

export const events = [
  { id:'e1', title:'Pitch Night — Green Tech', date:'Mi, 08.10 · 18:00', platform:'Zoom', img:'https://picsum.photos/seed/e1/900/480', hosts:['Founders Club'], desc:'Live Pitches von 6 GreenTech Startups — Q&A.'},
  { id:'e2', title:'MedTech Deep Dive', date:'Do, 09.10 · 14:00', platform:'MS Teams', img:'https://picsum.photos/seed/e2/900/480', hosts:['HealthInvest'], desc:'Panel: Regulierung & Markteintritt.'}
];