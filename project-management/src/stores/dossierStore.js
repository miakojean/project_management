import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/_services/api";

export const useDossierStore = defineStore('dossier', () => {
    // State
    const customerDossier = ref([]);
    const dossiers = ref([]);
    const currentDossier = ref(null);
    const currentDossierDocuments = ref([]);
    const loading = ref(false);
    const error = ref(null);
    const stats = ref({});
    const categories = ref([]);
    const dossiersArchives = ref([]);

    // Getters
    const totalDossiers = computed(() => dossiers.value.length);
    const getCurrentDossier = computed(()=>currentDossier.value)

    // Attach Affair
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

    // Dans dossierStore.js - ajoutez ceci à la fonction fetchCategories
    async function fetchCategories () {
        try {
            const response = await api.get(`/manager/category`);
            console.log("Listes des catégories", response.data);
            
            // Formater les catégories pour les rendre utilisables dans les selects
            const formattedCategories = response.data.map(category => ({
                id: category.id,
                nom: category.nom,
                code: category.code,
                couleur: category.couleur,
                icone: category.icone,
                est_fondamentale: category.est_fondamentale || false
            }));
            
            categories.value = formattedCategories;
            return formattedCategories; // Retourner les catégories formatées
        } catch(err) {
            error.value = err.response?.data?.error || "Erreur lors de la récupération";
            throw err; // Propager l'erreur
        }
    }

    async function fetchDossiers(params = {}) {
        loading.value = true;
        error.value = null;
        
        try {
            const response = await api.get(`/manager/affairs`, { params });
            dossiers.value = response.data.data.dossiers;
            stats.value = response.data.data.metadata;
            console.log("Les statistiques", stats.value);
            console.log("Les dossiers chargés", dossiers.value);
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
            console.log('Les données réçues sont', response.data);
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
            console.log('Données du dossier du client', customerDossier.value)
            return response.data;
        } catch (err) {
            error.value = err.response?.data?.error || 'Erreur lors du chargement des dossiers du client';
            throw err;
        } finally {
            loading.value = false;
        }
    }

    // Dans votre store
    async function createDossier(dossierData) {
        console.log("🔄 STORE: Début de createDossier");
        console.trace("Stack trace du store"); // ← TRÈS IMPORTANT
        
        loading.value = true;
        error.value = null;
        try {
            console.log("📡 STORE: Envoi requête API vers /manager/dossier/create/");
            const response = await api.post('/manager/dossier/create/', dossierData);
            
            console.log("✅ STORE: Réponse reçue", response.data);
            dossiers.value.unshift(response.data);
            return response.data;
        } catch (err) {
            console.error("❌ STORE: Erreur", err);
            error.value = err.response?.data?.error || 'Erreur lors de la création du dossier';
            throw err;
        } finally {
            loading.value = false;
            console.log("🏁 STORE: Fin de createDossier");
        }
    }

    async function updateDossier(id, dossierData, partial = false) {
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
        loading.value = true;
        error.value = null;
        
        try {
            await api.delete(`/dossiers/${id}/`);
            
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
    }

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