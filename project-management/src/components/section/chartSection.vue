<template>
  <section class="chart-card">
    <div class="chart-header">
      <h3>Statistiques Mensuelles</h3>
      <div class="chart-controls">
        <select v-model="selectedYear" @change="loadData" class="year-select">
          <option v-for="year in availableYears" :key="year" :value="year">
            {{ year }}
          </option>
        </select>
        <button @click="loadData" class="refresh-btn" :disabled="loading">
          ⟳
        </button>
      </div>
    </div>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    <div v-if="loading" class="loading-indicator">
      <div class="spinner"></div>
      <span>Chargement des données...</span>
    </div>
    
    <div v-else class="chart-container">
      <canvas ref="combinedChart"></canvas>
    </div>
    
    <div v-if="!loading && hasData" class="stats-summary">
      <div class="stat-group">
        <h4>Clients</h4>
        <div class="stat-item">
          <span class="stat-label">Total annuel</span>
          <span class="stat-value">{{ store.totalClients }} clients</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Ce mois-ci</span>
          <span class="stat-value">{{ store.currentMonthClients }} clients</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Moyenne</span>
          <span class="stat-value">{{ Math.round(store.totalClients / 12) }} clients/mois</span>
        </div>
      </div>
      
      <div class="stat-divider"></div>
      
      <div class="stat-group">
        <h4>Dossiers</h4>
        <div class="stat-item">
          <span class="stat-label">Total annuel</span>
          <span class="stat-value">{{ store.totalDossiers }} dossiers</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Ce mois-ci</span>
          <span class="stat-value">{{ store.currentMonthDossiers }} dossiers</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Moyenne</span>
          <span class="stat-value">{{ Math.round(store.totalDossiers / 12) }} dossiers/mois</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, computed } from 'vue';
import { Chart, registerables } from 'chart.js';
import { useChartStore } from '@/stores/chartStore';

Chart.register(...registerables);

const combinedChart = ref(null);
const chartInstance = ref(null);
const selectedYear = ref(new Date().getFullYear());

const store = useChartStore();
const { loading, error } = store;

const availableYears = ref([
  new Date().getFullYear() - 2,
  new Date().getFullYear() - 1,
  new Date().getFullYear()
]);

const hasData = computed(() => {
  return store.clientRegistrations.values.length > 0 || store.dossierStats.values.length > 0;
});

const loadData = async () => {
  await Promise.all([
    store.fetchClientMonthlyRegistrations(selectedYear.value),
    store.fetchDossierMonthlyStats(selectedYear.value)
  ]);
};

onMounted(async () => {
  await loadData();
  if (hasData.value) {
    renderChart();
  }
});

onBeforeUnmount(() => {
  if (chartInstance.value) {
    chartInstance.value.destroy();
  }
});

watch(
  () => [store.clientRegistrations, store.dossierStats],
  () => {
    if (chartInstance.value && hasData.value) {
      updateChart();
    }
  },
  { deep: true }
);

const renderChart = () => {
  if (!combinedChart.value) return;
  
  const ctx = combinedChart.value.getContext('2d');
  
  // Utiliser les labels communs (priorité aux clients, sinon dossiers)
  const labels = store.clientRegistrations.labels.length > 0 
    ? store.clientRegistrations.labels 
    : store.dossierStats.labels;
  
  chartInstance.value = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Nouveaux Clients',
          data: store.clientRegistrations.values,
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          borderColor: 'rgb(59, 130, 246)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: 'rgb(59, 130, 246)',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          yAxisID: 'y'
        },
        {
          label: 'Dossiers',
          data: store.dossierStats.values,
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          borderColor: 'rgb(16, 185, 129)',
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: 'rgb(16, 185, 129)',
          pointBorderColor: '#fff',
          pointBorderWidth: 2,
          pointRadius: 5,
          yAxisID: 'y1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false
      },
      plugins: {
        legend: {
          display: true,
          position: 'top',
          labels: {
            usePointStyle: true,
            pointStyle: 'circle',
            padding: 20
          }
        },
        tooltip: {
          mode: 'index',
          intersect: false,
          callbacks: {
            label: (context) => {
              const datasetLabel = context.dataset.label || '';
              const value = context.parsed.y;
              const suffix = datasetLabel.includes('Clients') ? ' clients' : ' dossiers';
              return `${datasetLabel}: ${value}${suffix}`;
            }
          }
        }
      },
      scales: {
        x: {
          grid: {
            display: false
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45
          }
        },
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          title: {
            display: true,
            text: 'Clients',
            color: 'rgb(59, 130, 246)',
            font: {
              weight: 'bold'
            }
          },
          grid: {
            drawOnChartArea: false
          },
          ticks: {
            callback: (value) => value
          }
        },
        y1: {
          type: 'linear',
          display: true,
          position: 'right',
          title: {
            display: true,
            text: 'Dossiers',
            color: 'rgb(16, 185, 129)',
            font: {
              weight: 'bold'
            }
          },
          grid: {
            drawOnChartArea: false
          },
          ticks: {
            callback: (value) => value
          }
        }
      },
      elements: {
        line: {
          tension: 0.3 // Légèrement plus lissé
        }
      }
    }
  });
};

const updateChart = () => {
  if (!chartInstance.value) return;
  
  const labels = store.clientRegistrations.labels.length > 0 
    ? store.clientRegistrations.labels 
    : store.dossierStats.labels;
  
  chartInstance.value.data.labels = labels;
  chartInstance.value.data.datasets[0].data = store.clientRegistrations.values;
  chartInstance.value.data.datasets[1].data = store.dossierStats.values;
  chartInstance.value.update();
};
</script>

<style scoped>
.chart-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 24px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.chart-header h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.25rem;
  font-weight: 600;
}

.chart-controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.year-select {
  padding: 6px 10px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  background: white;
  font-size: 14px;
}

.refresh-btn {
  padding: 6px 10px;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.refresh-btn:hover:not(:disabled) {
  background: #2563eb;
}

.refresh-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
}

.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
  margin: 20px 0;
}

.stats-summary {
  display: flex;
  justify-content: space-between;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e5e7eb;
}

.stat-group {
  flex: 1;
  padding: 0 16px;
}

.stat-group:first-child {
  padding-left: 0;
}

.stat-group:last-child {
  padding-right: 0;
}

.stat-group h4 {
  margin: 0 0 12px 0;
  color: #1f2937;
  font-size: 16px;
  font-weight: 600;
}

.stat-item {
  margin-bottom: 10px;
}

.stat-item:last-child {
  margin-bottom: 0;
}

.stat-label {
  display: block;
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 4px;
}

.stat-value {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #1f2937;
}

.stat-divider {
  width: 1px;
  background: #e5e7eb;
  margin: 0 16px;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 400px;
  color: #6b7280;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-message {
  background: #fee2e2;
  color: #dc2626;
  padding: 12px 16px;
  border-radius: 6px;
  margin: 20px 0;
  border-left: 4px solid #dc2626;
}

@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .chart-container {
    height: 300px;
  }
  
  .stats-summary {
    flex-direction: column;
    gap: 24px;
  }
  
  .stat-group {
    padding: 0;
  }
  
  .stat-divider {
    display: none;
  }
}
</style>