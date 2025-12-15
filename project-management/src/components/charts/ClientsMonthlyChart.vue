<template>
  <div class="clients-monthly-chart">
    <canvas ref="chartCanvas" aria-label="Clients inscrits par mois" role="img"></canvas>
  </div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, ref, watch } from 'vue';
import { useCustomerStore } from '@/stores/custumerStore';
import Chart from 'chart.js/auto';

const chartCanvas = ref(null);
let chartInstance = null;

const customerStore = useCustomerStore();

async function initChart() {
  try {
    await customerStore.fetchCustomersMonthlyStats();
    const labels = customerStore.getMonthlyStats.labels || [];
    const data = customerStore.getMonthlyStats.data || [];

    const ctx = chartCanvas.value.getContext('2d');
    chartInstance = new Chart(ctx, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Clients inscrits',
            data,
            backgroundColor: 'rgba(54, 162, 235, 0.5)'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { title: { display: true, text: 'Mois' } },
          y: { title: { display: true, text: 'Nombre de clients' }, beginAtZero: true }
        }
      }
    });
  } catch (err) {
    console.error('Erreur initialisation chart clients monthly:', err);
  }
}

// Re-render when monthly stats change
watch(() => customerStore.getMonthlyStats, (newVal) => {
  if (!chartInstance) return;
  chartInstance.data.labels = newVal.labels || [];
  chartInstance.data.datasets[0].data = newVal.data || [];
  chartInstance.update();
}, { deep: true });

onMounted(() => {
  initChart();
});

onBeforeUnmount(() => {
  if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }
});
</script>

<style scoped>
.clients-monthly-chart {
  width: 100%;
  height: 320px;
}
canvas {
  width: 100% !important;
  height: 100% !important;
}
</style>
