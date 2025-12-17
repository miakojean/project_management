import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/_services/api";

export const useChartStore = defineStore("chartStore", () => {
    const loading = ref(false);
    const error = ref(null);
    const selectedYear = ref(new Date().getFullYear());
    
    // Données pour différents graphiques
    const salesData = ref({
        labels: [],
        values: []
    });
    
    const clientRegistrations = ref({
        labels: [],
        rawLabels: [], // Pour conserver les labels originaux si besoin
        values: []
    });
    
    const dossierStats = ref({
        labels: [],
        values: [],
        types: [] // Pour différencier les types de dossiers si nécessaire
    });
    
    // Getters communs
    const totalClients = computed(() => {
        return clientRegistrations.value.values.reduce((sum, value) => sum + value, 0);
    });
    
    const totalDossiers = computed(() => {
        return dossierStats.value.values.reduce((sum, value) => sum + value, 0);
    });
    
    const currentMonthClients = computed(() => {
        if (clientRegistrations.value.values.length === 0) return 0;
        const currentMonth = new Date().getMonth(); // 0-indexed
        return clientRegistrations.value.values[currentMonth] || 0;
    });
    
    const currentMonthDossiers = computed(() => {
        if (dossierStats.value.values.length === 0) return 0;
        const currentMonth = new Date().getMonth();
        return dossierStats.value.values[currentMonth] || 0;
    });
    
    // Fonction utilitaire pour formater les mois
    const formatMonthLabel = (dateString) => {
        const [year, month] = dateString.split('-');
        const monthNames = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun', 
                           'Jul', 'Aoû', 'Sep', 'Oct', 'Nov', 'Déc'];
        return `${monthNames[parseInt(month) - 1]} ${year}`;
    };
    
    // Actions pour récupérer les données
    async function fetchClientMonthlyRegistrations(year = null) {
        loading.value = true;
        error.value = null;
        
        try {
            const params = {};
            if (year) {
                params.year = year;
            }
            
            const response = await api.get('manager/clients/stats/monthly/', { params });
            
            if (response.data.success) {
                clientRegistrations.value = {
                    labels: response.data.labels.map(label => formatMonthLabel(label)),
                    rawLabels: response.data.labels, // Conservation des labels originaux
                    values: response.data.data
                };
            } else {
                throw new Error(response.data.message || 'Erreur lors du chargement des données');
            }
            
            return response.data;
        } catch (err) {
            error.value = err.message || 'Erreur lors du chargement des inscriptions clients';
            console.error('Erreur fetchClientMonthlyRegistrations:', err);
            
            // Données fictives pour le développement
            if (process.env.NODE_ENV === 'development') {
                clientRegistrations.value = generateMockClientData();
            }
        } finally {
            loading.value = false;
        }
    }
    
    async function fetchDossierMonthlyStats(year = null) {
        loading.value = true;
        error.value = null;
        
        try {
            const params = {};
            if (year) {
                params.year = year;
            }
            
            const response = await api.get('manager/affairs/stats/monthly/', { params });
            
            if (response.data.success) {
                dossierStats.value = {
                    labels: response.data.labels.map(label => formatMonthLabel(label)),
                    rawLabels: response.data.labels, // Conservation des labels originaux
                    values: response.data.data,
                    types: response.data.types || [] // Si l'API retourne des types
                };
            } else {
                throw new Error(response.data.message || 'Erreur lors du chargement des données');
            }
            
            return response.data;
        } catch (err) {
            error.value = err.message || 'Erreur lors du chargement des statistiques de dossiers';
            console.error('Erreur fetchDossierMonthlyStats:', err);
            
            // Données fictives pour le développement
            if (process.env.NODE_ENV === 'development') {
                dossierStats.value = generateMockDossierData();
            }
        } finally {
            loading.value = false;
        }
    }
    
    async function fetchSalesMonthlyStats(year = null) {
        loading.value = true;
        error.value = null;
        
        try {
            const params = {};
            if (year) {
                params.year = year;
            }
            
            // Adaptez cette URL à votre endpoint réel pour les ventes
            const response = await api.get('/sales/stats/monthly/', { params });
            
            if (response.data.success) {
                salesData.value = {
                    labels: response.data.labels.map(label => formatMonthLabel(label)),
                    rawLabels: response.data.labels, // Conservation des labels originaux
                    values: response.data.data
                };
            } else {
                throw new Error(response.data.message || 'Erreur lors du chargement des données');
            }
            
            return response.data;
        } catch (err) {
            error.value = err.message || 'Erreur lors du chargement des statistiques de ventes';
            console.error('Erreur fetchSalesMonthlyStats:', err);
            
            // Données fictives pour le développement
            if (process.env.NODE_ENV === 'development') {
                salesData.value = generateMockSalesData();
            }
        } finally {
            loading.value = false;
        }
    }
    
    // Récupérer toutes les statistiques
    async function fetchAllMonthlyStats(year = null) {
        loading.value = true;
        error.value = null;
        
        try {
            await Promise.all([
                fetchClientMonthlyRegistrations(year),
                fetchDossierMonthlyStats(year),
                fetchSalesMonthlyStats(year)
            ]);
        } catch (err) {
            error.value = err.message || 'Erreur lors du chargement des statistiques';
            console.error('Erreur fetchAllMonthlyStats:', err);
        } finally {
            loading.value = false;
        }
    }
    
    // Fonctions pour générer des données fictives (développement uniquement)
    function generateMockClientData() {
        const labels = [];
        const rawLabels = [];
        const values = [];
        const currentYear = selectedYear.value || new Date().getFullYear();
        
        for (let i = 0; i < 12; i++) {
            const month = (i + 1).toString().padStart(2, '0');
            const rawLabel = `${currentYear}-${month}`;
            rawLabels.push(rawLabel);
            labels.push(formatMonthLabel(rawLabel));
            values.push(Math.floor(Math.random() * 50) + 20); // Entre 20 et 70 clients
        }
        
        return { labels, rawLabels, values };
    }
    
    function generateMockDossierData() {
        const labels = [];
        const rawLabels = [];
        const values = [];
        const currentYear = selectedYear.value || new Date().getFullYear();
        
        for (let i = 0; i < 12; i++) {
            const month = (i + 1).toString().padStart(2, '0');
            const rawLabel = `${currentYear}-${month}`;
            rawLabels.push(rawLabel);
            labels.push(formatMonthLabel(rawLabel));
            values.push(Math.floor(Math.random() * 100) + 50); // Entre 50 et 150 dossiers
        }
        
        return { labels, rawLabels, values, types: [] };
    }
    
    function generateMockSalesData() {
        const labels = [];
        const rawLabels = [];
        const values = [];
        const currentYear = selectedYear.value || new Date().getFullYear();
        
        for (let i = 0; i < 12; i++) {
            const month = (i + 1).toString().padStart(2, '0');
            const rawLabel = `${currentYear}-${month}`;
            rawLabels.push(rawLabel);
            labels.push(formatMonthLabel(rawLabel));
            values.push(Math.floor(Math.random() * 50000) + 20000); // Entre 20k et 70k
        }
        
        return { labels, rawLabels, values };
    }
    
    // Réinitialiser les données
    function resetChartData() {
        clientRegistrations.value = { labels: [], rawLabels: [], values: [] };
        dossierStats.value = { labels: [], rawLabels: [], values: [], types: [] };
        salesData.value = { labels: [], rawLabels: [], values: [] };
        loading.value = false;
        error.value = null;
    }
    
    // Exporter les données (pour téléchargement CSV par exemple)
    function exportClientsData(format = 'csv') {
        const data = clientRegistrations.value.labels.map((label, index) => ({
            Mois: label,
            'Nouveaux Clients': clientRegistrations.value.values[index]
        }));
        
        if (format === 'csv') {
            // Implémentez la conversion CSV ici
            return data;
        }
        
        return data;
    }
    
    return {
        // States
        loading,
        error,
        selectedYear,
        clientRegistrations,
        dossierStats,
        salesData,
        
        // Getters
        totalClients,
        totalDossiers,
        currentMonthClients,
        currentMonthDossiers,
        
        // Actions
        fetchClientMonthlyRegistrations,
        fetchDossierMonthlyStats,
        fetchSalesMonthlyStats,
        fetchAllMonthlyStats,
        resetChartData,
        exportClientsData,
        formatMonthLabel
    };
});