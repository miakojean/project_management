<template>
  <article class="card">
    <div class="card__header">
      <span class="badge" :class="badgeClass">{{ typeClient }}</span>
    </div>

    <div class="card__body">
      <div class="company-logo">
        <span>{{ initiales }}</span>
      </div>

      <div class="content">
        <h4 class="company-name" :title="customerName">{{ customerName }}</h4>
        
        <div class="info-group">
          <div class="info-item">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon">
              <path d="M5.625 1.5c-1.036 0-1.875.84-1.875 1.875v17.25c0 1.035.84 1.875 1.875 1.875h12.75c1.035 0 1.875-.84 1.875-1.875V12.75A3.75 3.75 0 0016.5 9h-1.875a1.875 1.875 0 01-1.875-1.875V5.25A3.75 3.75 0 009 1.5H5.625z" />
              <path d="M12.971 1.816A5.23 5.23 0 0114.25 5.25v1.875c0 .207.168.375.375.375H16.5a5.23 5.23 0 013.434 1.279 9.768 9.768 0 00-6.963-6.963z" />
            </svg>
            <span class="info-text">{{ description }}</span>
          </div>
          
          <div class="info-item" v-if="location">
             <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon">
              <path fill-rule="evenodd" d="M11.54 22.351l.07.04.028.016a.76.76 0 00.723 0l.028-.015.071-.041a16.975 16.975 0 001.144-.742 19.58 19.58 0 002.683-2.282c1.944-1.99 3.963-4.98 3.963-8.827a8.25 8.25 0 00-16.5 0c0 3.846 2.02 6.837 3.963 8.827a19.58 19.58 0 002.682 2.282 16.975 16.975 0 001.145.742zM12 13.5a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd" />
            </svg>
            <span class="info-text">{{ location }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="card__footer">
      
      <button class="btn-primary" @click="emitClick">
        Ouvrir le dossier
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="btn-icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
        </svg>
      </button>
    </div>
  </article>
</template>

<script>
export default {
  name: 'LegalEntityCard',
  props: {
    customerName: {
      type: String,
      default: 'Tech Solutions SAS'
    },
    description: {
      type: String,
      default: 'SIREN: 892 102 921'
    },
    location: {
      type: String,
      default: 'Paris, France'
    },
    typeClient: {
      type: String,
      default: 'Entreprise'
    }
  },

  // Déclaration de l'événement
  emits: ['handleCustomer'],

  computed: {
    initiales() {
      return this.customerName
        .split(' ')
        .map(n => n[0])
        .slice(0, 2)
        .join('')
        .toUpperCase();
    },
    badgeClass() {
      return this.typeClient.toLowerCase() === 'particulier' ? 'badge-purple' : 'badge-blue';
    }
  },

  methods: {
    // 3. La méthode qui envoie le signal au parent
    emitClick() {
      this.$emit('handleCustomer');
    },
    openFolder() {
      // Logique future pour ouvrir le dossier directement
      console.log('Ouverture du dossier...');
    }
  }
}
</script>

<style scoped>
/* Variables locales */
.card {
  --primary: #0b79d0;
  --primary-dark: #074e8c;
  --bg-soft: #f8fafc;
  --text-main: #1e293b;
  --text-muted: #64748b;
  
  width: 100%;
  max-width: 380px; 
  background: #ffffff;
  border: 1px solid #e2e8f0; 
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;
  
  /* 4. IMPORTANT : Indiquer que la carte est cliquable */
  cursor: pointer;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 20px -3px rgba(0, 0, 0, 0.1);
  border-color: #cbd5e1;
}

/* HEADER */
.card__header {
  padding: 1.25rem 1.5rem 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.badge {
  display: inline-flex;
  padding: 0.35rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 700;
  border-radius: 99px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.badge-blue {
  background: #e0f2fe;
  color: #0369a1;
}
.badge-purple {
  background: #f3e8ff;
  color: #7e22ce;
}

/* BODY */
.card__body {
  padding: 0.5rem 1.5rem 1.5rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.company-logo {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  color: var(--text-muted);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.company-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-main);
  margin: 0;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.info-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.icon {
  width: 18px;
  height: 18px;
  color: #94a3b8; 
}

/* FOOTER */
.card__footer {
  padding: 1rem 1.5rem;
  background: var(--bg-soft);
  border-top: 1px solid #f1f5f9;
  display: flex;
  justify-content: end; 
  align-items: center;
  gap: 1rem;
}

/* BOUTONS */
button {
  cursor: pointer;
  font-family: inherit;
  transition: all 0.2s;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 0.5rem;
}

.btn-ghost {
  background: transparent;
  border: none;
  color: var(--text-muted);
  padding: 0.5rem 0; 
}
.btn-ghost:hover {
  color: var(--text-main);
  text-decoration: underline;
}

.btn-primary {
  background: var(--primary);
  border: none;
  color: white;
  padding: 0.6rem 1.2rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 2px 4px rgba(11, 121, 208, 0.2);
}

.btn-primary:hover {
  background: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(11, 121, 208, 0.3);
}

.btn-icon {
  width: 16px;
  height: 16px;
}
</style>