import { defineStore } from "pinia";
import { ref, computed, watch } from "vue"; // <-- watch est importé ici
import api from "@/_services/api";

// =================================================================
// LOGIQUE DE CACHE POUR LE HOT RELOAD
// =================================================================

const CACHE_KEY = 'dossierStoreCache';

/**
 * Charge l'état du store depuis localStorage.
 * @returns {object} L'état ou un objet vide si échec.
 */
function loadStateFromCache() {
    try {
        const cachedState = localStorage.getItem(CACHE_KEY);
        if (cachedState) {
            // Retourne les données parsées.
            return JSON.parse(cachedState);
        }
    } catch (e) {
        console.error("Erreur lors du chargement du cache:", e);
    }
    return {};
}

/**
 * Sauvegarde l'état partiel du store dans localStorage.
 * @param {object} state - L'objet contenant les valeurs à mettre en cache.
 */
function saveStateToCache(state) {
    try {
        localStorage.setItem(CACHE_KEY, JSON.stringify(state));
    } catch (e) {
        console.error("Erreur lors de la sauvegarde du cache:", e);
    }
}


export const useDossierStore = defineStore('dossier', () => {
    
    const cached = loadStateFromCache(); // <-- Chargement du cache au départ

    // State (Initialisation avec le cache si disponible)
    const customerDossier = ref(cached.customerDossier || []);
    const dossiers = ref(cached.dossiers || []); // <-- Initialisé avec le cache
    const currentDossier = ref(cached.currentDossier || null); // <-- Initialisé avec le cache
    const currentDossierDocuments = ref(cached.currentDossierDocuments || []);
    const loading = ref(false);
    const error = ref(null);
    const stats = ref(cached.stats || {}); // <-- Initialisé avec le cache
    const categories = ref(cached.categories || []);
    const dossiersArchives = ref(cached.dossiersArchives || []);

    // Getters
    const totalDossiers = computed(() => dossiers.value.length);
    const getCurrentDossier = computed(()=>currentDossier.value)
    // ... (autres getters inchangés) ...
    function attachAffair(affair){
        currentDossier.value = affair;
        console.log('Dossier selectionné', affair);
        return currentDossier;
    }
    
    const dossiersActifs = computed(() => 
        dossiers.value.filter(d => 
            ['NOUVEAU', 'EN_COURS', 'EN_ATTENTE'].includes(d.statut)
        )
    );
    
    const dossiersEnRetard = computed(() => 
        dossiers.value.filter(d => d.est_en_retard)
    );
    
    const dossiersParStatut = computed(() => {
        const grouped = {};
        dossiers.value.forEach(dossier => {
            if (!grouped[dossier.statut]) {
                grouped[dossier.statut] = [];
            }
            grouped[dossier.statut].push(dossier);
        });
        return grouped;
    });

    // Actions
    // ... (Toutes les actions restent inchangées) ...

    async function fetchCategories () {
        try {
            const response = await api.get(`/manager/category`);
            // ... (votre logique existante) ...
            const formattedCategories = response.data.map(category => ({
                id: category.id,
                nom: category.nom,
                code: category.code,
                couleur: category.couleur,
                icone: category.icone,
                est_fondamentale: category.est_fondamentale || false
            }));
            
            categories.value = formattedCategories;
            return formattedCategories;
        } catch(err) {
            error.value = err.response?.data?.error || "Erreur lors de la récupération";
            throw err;
        }
    }

    async function fetchDossiers(params = {}) {
        loading.value = true;
        error.value = null;
        
        try {
            const response = await api.get(`/manager/affairs`, { params });
            dossiers.value = response.data.data.dossiers;
            stats.value = response.data.data.metadata;
            // ... (logique existante) ...
            return response.data;
        } catch (err) {
            error.value = err.response?.data?.error || 'Erreur lors du chargement des dossiers'; 
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function fetchArchivesDossiers(){
        try {
            const response = await api.get(`/manager/affairs?est_archive=true`)
            dossiersArchives.value = response.data.data.dossiers
            console.log('Documents archivés', dossiersArchives)
        } catch (err) {
            error.value = err.response?.data?.error || "Un problème est lors de la réccupération des archives"
            console.error(error)
        }   
    }

    async function fetchDossierById(id) {
        loading.value = true;
        error.value = null;
        
        try {
            const response = await api.get(`/manager/affairs/details/${id}/`);
            currentDossier.value = response.data;
            // ... (logique existante) ...
            return response.data;
        } catch (err) {
            error.value = err.response?.data?.error || 'Erreur lors du chargement du dossier';
            console.error('Une erreur est intervenue lors de la récupération du dossier');
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function fetchDossiersByClient(clientId) {
        loading.value = true;
        error.value = null;
        
        try {
            const response = await api.get(`manager/affairs?client_id=${clientId}`);
            customerDossier.value = response.data.data.dossiers
            // ... (logique existante) ...
            return response.data;
        } catch (err) {
            error.value = err.response?.data?.error || 'Erreur lors du chargement des dossiers du client';
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function createDossier(dossierData) {
        // ... (logique existante) ...
        loading.value = true;
        error.value = null;
        try {
            const response = await api.post('/manager/dossier/create/', dossierData);
            dossiers.value.unshift(response.data);
            return response.data;
        } catch (err) {
            error.value = err.response?.data?.error || 'Erreur lors de la création du dossier';
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function updateDossier(id, dossierData, partial = false) {
        // ... (logique existante) ...
        loading.value = true;
        error.value = null;
        
        try {
            const method = partial ? 'patch' : 'put';
            const response = await api[method](`/manager/affairs/details/${id}/`, dossierData);
            
            // Mettre à jour dans la liste
            const index = dossiers.value.findIndex(d => d.id === id);
            if (index !== -1) {
                dossiers.value[index] = response.data;
            }
            
            // Mettre à jour le dossier courant si c'est le même
            if (currentDossier.value && currentDossier.value.id === id) {
                currentDossier.value = response.data;
            }
            
            return response.data;
        } catch (err) {
            error.value = err.response?.data?.error || 'Erreur lors de la mise à jour du dossier';
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function deleteDossier(id) {
        // ... (logique existante) ...
        loading.value = true;
        error.value = null;
        
        try {
            await api.delete(`/manager/affairs/details/${id}/`);
            
            // Retirer de la liste
            const index = dossiers.value.findIndex(d => d.id === id);
            if (index !== -1) {
                dossiers.value.splice(index, 1);
            }
            
            // Vider le dossier courant si c'est le même
            if (currentDossier.value && currentDossier.value.id === id) {
                currentDossier.value = null;
            }
            
            return true;
        } catch (err) {
            error.value = err.response?.data?.error || 'Erreur lors de la suppression du dossier';
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function fetchDossierStats() {
        // ... (logique existante) ...
        loading.value = true;
        error.value = null;
        
        try {
            const response = await api.get('/manager/affairs');
            stats.value = response.data;
            return response.data;
        } catch (err) {
            error.value = err.response?.data?.error || 'Erreur lors du chargement des statistiques';
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function updateDossierStatus(id, newStatus) {
        return await updateDossier(id, { statut: newStatus }, true);
    }

    async function updateDossierPriority(id, newPriority) {
        return await updateDossier(id, { priorite: newPriority }, true);
    }

    async function addCollaboratorToDossier(id, collaboratorId) {
        try {
            const dossier = await fetchDossierById(id);
            const currentCollaborateurs = dossier.collaborateurs || [];
            
            if (!currentCollaborateurs.includes(collaboratorId)) {
                const updatedCollaborateurs = [...currentCollaborateurs, collaboratorId];
                return await updateDossier(id, { collaborateurs: updatedCollaborateurs });
            }
            
            return dossier;
        } catch (err) {
            error.value = err.response?.data?.error || 'Erreur lors de l\'ajout du collaborateur';
            throw err;
        }
    }

    async function removeCollaboratorFromDossier(id, collaboratorId) {
        try {
            const dossier = await fetchDossierById(id);
            const currentCollaborateurs = dossier.collaborateurs || [];
            
            const updatedCollaborateurs = currentCollaborateurs.filter(collabId => collabId !== collaboratorId);
            return await updateDossier(id, { collaborateurs: updatedCollaborateurs });
        } catch (err) {
            error.value = err.response?.data?.error || 'Erreur lors de la suppression du collaborateur';
            throw err;
        }
    }

    // Reset state
    function resetCurrentDossier() {
        currentDossier.value = null;
    }

    function resetError() {
        error.value = null;
    }

    function reset() {
        dossiers.value = [];
        currentDossier.value = null;
        stats.value = {};
        error.value = null;
        // Optionnel : Vider le cache lors d'un reset complet
        localStorage.removeItem(CACHE_KEY); 
    }

    // =================================================================
    // WATCHER POUR CACHE - DÉCLENCHÉ À CHAQUE CHANGEMENT
    // =================================================================
    watch(
        [dossiers, currentDossier, stats, customerDossier, categories, dossiersArchives], 
        ([newDossiers, newCurrentDossier, newStats, newCustomerDossier, newCategories, newDossiersArchives]) => {
        saveStateToCache({
            dossiers: newDossiers,
            currentDossier: newCurrentDossier,
            stats: newStats,
            customerDossier: newCustomerDossier,
            categories: newCategories,
            dossiersArchives: newDossiersArchives,
        });
    }, 
    { deep: true, immediate: false });


    return {
        // State
        dossiers,
        currentDossier,
        currentDossierDocuments,
        loading,
        error,
        stats,
        customerDossier,
        categories,
        dossiersArchives,

        // Getters
        totalDossiers,
        dossiersActifs,
        dossiersEnRetard,
        dossiersParStatut,
        getCurrentDossier,

        // Attach Affair
        attachAffair,
        
        // Actions
        fetchCategories,
        fetchDossiers,
        fetchDossierById,
        fetchDossiersByClient,
        fetchArchivesDossiers,
        createDossier,
        updateDossier,
        deleteDossier,
        fetchDossierStats,
        updateDossierStatus,
        updateDossierPriority,
        addCollaboratorToDossier,
        removeCollaboratorFromDossier,
        resetCurrentDossier,
        resetError,
        reset
    };
});