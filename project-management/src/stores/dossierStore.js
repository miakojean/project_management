import { defineStore } from "pinia";
import { ref, computed, watch } from "vue";
import api from "@/_services/api";

// =================================================================
// LOGIQUE DE CACHE POUR LE HOT RELOAD
// =================================================================

const CACHE_KEY = 'dossierStoreCache';

function loadStateFromCache() {
    try {
        const cachedState = localStorage.getItem(CACHE_KEY);
        if (cachedState) {
            return JSON.parse(cachedState);
        }
    } catch (e) {
        //console.error("Erreur lors du chargement du cache:", e);
    }
    return {};
}

function saveStateToCache(state) {
    try {
        localStorage.setItem(CACHE_KEY, JSON.stringify(state));
    } catch (e) {
        //console.error("Erreur lors de la sauvegarde du cache:", e);
    }
}

export const useDossierStore = defineStore('dossier', () => {
    
    const cached = loadStateFromCache();

    // State (Initialisation avec le cache si disponible)
    const customerDossier = ref(cached.customerDossier || []);
    const dossiers = ref(cached.dossiers || []);
    const currentDossier = ref(cached.currentDossier || null);
    const currentDossierDocuments = ref(cached.currentDossierDocuments || []);
    const loading = ref(false);
    const error = ref(null);
    const stats = ref(cached.stats || {});
    const categories = ref(cached.categories || []);
    const dossiersArchives = ref(cached.dossiersArchives || []);
    
    // =================================================================
    // NOUVEAU : ÉTAT POUR LES COMMENTAIRES
    // =================================================================
    const commentaires = ref(cached.commentaires || []);
    const currentCommentaire = ref(cached.currentCommentaire || null);
    const reponses = ref(cached.reponses || []);
    const commentairesLoading = ref(false);
    const commentairesError = ref(null);

    // Getters
    const totalDossiers = computed(() => dossiers.value.length);
    const getCurrentDossier = computed(() => currentDossier.value);
    
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

    // =================================================================
    // NOUVEAU : GETTERS POUR LES COMMENTAIRES
    // =================================================================
    const getCommentairesByDossier = computed(() => (dossierId) => {
        return commentaires.value.filter(commentaire => 
            commentaire.dossier_id === dossierId || commentaire.dossier === dossierId
        );
    });

    const getReponsesByCommentaire = computed(() => (commentaireId) => {
        return reponses.value.filter(reponse => 
            reponse.commentaire_id === commentaireId || reponse.commentaire === commentaireId
        );
    });

    const commentairesCount = computed(() => commentaires.value.length);
    const reponsesCount = computed(() => reponses.value.length);

    // =================================================================
    // ACTIONS POUR LES COMMENTAIRES
    // =================================================================

    // 1. CRUD Commentaires
    async function fetchCommentairesByDossier(dossierId) {
        commentairesLoading.value = true;
        commentairesError.value = null;
        
        try {
            const response = await api.get(`/manager/affairs/${dossierId}/commentaires/`);
            // Mettre à jour le store avec les nouveaux commentaires
            // Supporter plusieurs formes de réponse (objet {commentaires: [...] } ou directement un tableau)
            const newCommentaires = response.data?.commentaires || response.data || [];

            //console.log('fetchCommentairesByDossier response:', {
            //    url: `/manager/affairs/${dossierId}/commentaires/`,
            //    status: response.status,
            //    receivedCount: Array.isArray(newCommentaires) ? newCommentaires.length : 'N/A'
            //});

            const normalized = Array.isArray(newCommentaires) ? newCommentaires : [];

            // S'assurer que chaque commentaire a bien un champ dossier_id pour le getter
            normalized.forEach(c => {
                if (!('dossier_id' in c) && ('dossier' in c)) {
                    c.dossier_id = c.dossier;
                }
                if (!('dossier_id' in c)) {
                    c.dossier_id = dossierId;
                }
            });

            // Remplacer les commentaires existants pour ce dossier afin d'éviter des états incohérents
            commentaires.value = commentaires.value.filter(c => c.dossier_id !== dossierId).concat(normalized);

            return response.data;
        } catch (err) {
            // Log détaillé pour faciliter le debug (status + payload)
            commentairesError.value = err.response?.data?.error || 'Erreur lors du chargement des commentaires';
            //console.error('Erreur fetchCommentaires:', {
            //    status: err.response?.status,
            //    data: err.response?.data,
            //    message: err.message
            //});
            throw err;
        } finally {
            commentairesLoading.value = false;
        }
    }

    async function fetchCommentaireById(commentaireId) {
        commentairesLoading.value = true;
        commentairesError.value = null;
        
        try {
            const response = await api.get(`/manager/commentaires/${commentaireId}/`);
            currentCommentaire.value = response.data;
            
            // Mettre à jour dans la liste
            const index = commentaires.value.findIndex(c => c.id === commentaireId);
            if (index !== -1) {
                commentaires.value[index] = response.data;
            } else {
                commentaires.value.push(response.data);
            }
            
            return response.data;
        } catch (err) {
            commentairesError.value = err.response?.data?.error || 'Erreur lors du chargement du commentaire';
            throw err;
        } finally {
            commentairesLoading.value = false;
        }
    }

    async function createCommentaire(dossierId, message) {
        commentairesLoading.value = true;
        commentairesError.value = null;
        
        try {
            const response = await api.post(`/manager/affairs/${dossierId}/commentaires/`, {
                message
            });
            
            // Ajouter le nouveau commentaire au store
            commentaires.value.push(response.data);
            
            return response.data;
        } catch (err) {
            commentairesError.value = err.response?.data?.error || 'Erreur lors de la création du commentaire';
            throw err;
        } finally {
            commentairesLoading.value = false;
        }
    }

    async function updateCommentaire(commentaireId, message) {
        commentairesLoading.value = true;
        commentairesError.value = null;
        
        try {
            const response = await api.put(`/manager/commentaires/${commentaireId}/`, {
                message
            });
            
            // Mettre à jour dans le store
            const index = commentaires.value.findIndex(c => c.id === commentaireId);
            if (index !== -1) {
                commentaires.value[index] = response.data;
            }
            
            // Mettre à jour le commentaire courant si c'est le même
            if (currentCommentaire.value && currentCommentaire.value.id === commentaireId) {
                currentCommentaire.value = response.data;
            }
            
            return response.data;
        } catch (err) {
            commentairesError.value = err.response?.data?.error || 'Erreur lors de la modification du commentaire';
            throw err;
        } finally {
            commentairesLoading.value = false;
        }
    }

    async function deleteCommentaire(commentaireId) {
        commentairesLoading.value = true;
        commentairesError.value = null;
        
        try {
            await api.delete(`/manager/commentaires/${commentaireId}/`);
            
            // Retirer du store
            const commentaireIndex = commentaires.value.findIndex(c => c.id === commentaireId);
            if (commentaireIndex !== -1) {
                commentaires.value.splice(commentaireIndex, 1);
            }
            
            // Retirer les réponses associées
            reponses.value = reponses.value.filter(r => 
                r.commentaire_id !== commentaireId && r.commentaire !== commentaireId
            );
            
            // Vider le commentaire courant si c'est le même
            if (currentCommentaire.value && currentCommentaire.value.id === commentaireId) {
                currentCommentaire.value = null;
            }
            
            return true;
        } catch (err) {
            commentairesError.value = err.response?.data?.error || 'Erreur lors de la suppression du commentaire';
            throw err;
        } finally {
            commentairesLoading.value = false;
        }
    }

    // 2. CRUD Réponses
    async function fetchReponsesByCommentaire(commentaireId) {
        commentairesLoading.value = true;
        commentairesError.value = null;
        
        try {
            const response = await api.get(`/manager/commentaires/${commentaireId}/reponses/`);
            
            // Mettre à jour le store avec les nouvelles réponses
            const newReponses = response.data.reponses || [];
            
            newReponses.forEach(newReponse => {
                // Normaliser les champs de relation pour faciliter le filtrage côté client
                if (!('commentaire_id' in newReponse) && ('commentaire' in newReponse)) {
                    newReponse.commentaire_id = newReponse.commentaire;
                }
                if (!('commentaire' in newReponse) && ('commentaire_id' in newReponse)) {
                    newReponse.commentaire = newReponse.commentaire_id;
                }

                const existingIndex = reponses.value.findIndex(r => r.id === newReponse.id);
                if (existingIndex === -1) {
                    reponses.value.push(newReponse);
                } else {
                    reponses.value[existingIndex] = newReponse;
                }
            });
            
            return response.data;
        } catch (err) {
            commentairesError.value = err.response?.data?.error || 'Erreur lors du chargement des réponses';
            throw err;
        } finally {
            commentairesLoading.value = false;
        }
    }

    async function createReponse(commentaireId, message) {
        commentairesLoading.value = true;
        commentairesError.value = null;
        
        try {
            const response = await api.post(`/manager/commentaires/${commentaireId}/reponses/`, {
                message
            });
            
            // Normaliser la réponse: s'assurer qu'elle référence le commentaire parent
            const reponseData = response.data || {};
            if (!('commentaire_id' in reponseData) && !('commentaire' in reponseData)) {
                reponseData.commentaire_id = commentaireId;
                reponseData.commentaire = commentaireId;
            } else {
                // Compatibilité: garantir la présence des deux champs
                if (!('commentaire_id' in reponseData) && ('commentaire' in reponseData)) {
                    reponseData.commentaire_id = reponseData.commentaire;
                }
                if (!('commentaire' in reponseData) && ('commentaire_id' in reponseData)) {
                    reponseData.commentaire = reponseData.commentaire_id;
                }
            }

            // Ajouter la nouvelle réponse au store des réponses
            reponses.value.push(reponseData);

            // Attacher la réponse au commentaire parent si présent dans le cache
            const commentaireIndex = commentaires.value.findIndex(c => c.id === commentaireId);
            if (commentaireIndex !== -1) {
                if (!commentaires.value[commentaireIndex].reponses) {
                    commentaires.value[commentaireIndex].reponses = [];
                }
                commentaires.value[commentaireIndex].reponses.push(reponseData);
            }
            //console.debug('createReponse: réponse créée et attachée', { commentaireId, reponseData });
            
            return response.data;
        } catch (err) {
            commentairesError.value = err.response?.data?.error || 'Erreur lors de la création de la réponse';
            throw err;
        } finally {
            commentairesLoading.value = false;
        }
    }

    async function updateReponse(reponseId, message) {
        commentairesLoading.value = true;
        commentairesError.value = null;
        
        try {
            const response = await api.put(`/manager/reponses/${reponseId}/`, {
                message
            });
            
            // Mettre à jour dans le store
            const index = reponses.value.findIndex(r => r.id === reponseId);
            if (index !== -1) {
                reponses.value[index] = response.data;
            }
            
            return response.data;
        } catch (err) {
            commentairesError.value = err.response?.data?.error || 'Erreur lors de la modification de la réponse';
            throw err;
        } finally {
            commentairesLoading.value = false;
        }
    }

    async function deleteReponse(reponseId) {
        commentairesLoading.value = true;
        commentairesError.value = null;
        
        try {
            await api.delete(`/manager/reponses/${reponseId}/`);
            
            // Retirer du store
            const reponseIndex = reponses.value.findIndex(r => r.id === reponseId);
            if (reponseIndex !== -1) {
                reponses.value.splice(reponseIndex, 1);
            }
            
            return true;
        } catch (err) {
            commentairesError.value = err.response?.data?.error || 'Erreur lors de la suppression de la réponse';
            throw err;
        } finally {
            commentairesLoading.value = false;
        }
    }

    // 3. Actions utilitaires pour les commentaires
    async function loadCommentairesForDossier(dossierId) {
        try {
            // Charger les commentaires du dossier
            await fetchCommentairesByDossier(dossierId);
            
            // Pour chaque commentaire, charger ses réponses uniquement si elles ne sont pas déjà incluses
            const dossierCommentaires = getCommentairesByDossier.value(dossierId);

            const needFetch = !dossierCommentaires.some(c => Array.isArray(c.reponses) && c.reponses.length > 0);
            if (needFetch) {
                for (const commentaire of dossierCommentaires) {
                    await fetchReponsesByCommentaire(commentaire.id);
                }
            }

            // Construire la liste des réponses soit depuis les commentaires inclus, soit depuis le cache `reponses`
            let collectedReponses = [];
            if (dossierCommentaires.some(c => Array.isArray(c.reponses) && c.reponses.length > 0)) {
                collectedReponses = dossierCommentaires.flatMap(c => c.reponses.map(r => ({ ...r, commentaire: c.id, commentaire_id: c.id })));
            } else {
                collectedReponses = reponses.value.filter(r => 
                    dossierCommentaires.some(c => c.id === (r.commentaire_id || r.commentaire))
                );
            }

            return {
                commentaires: dossierCommentaires,
                reponses: collectedReponses
            };
        } catch (err) {
            //console.error('Erreur lors du chargement complet des commentaires:', err);
            throw err;
        }
    }

    function getCommentaireWithReponses(commentaireId) {
        const commentaire = commentaires.value.find(c => c.id === commentaireId);
        if (!commentaire) return null;
        
        const commentaireReponses = getReponsesByCommentaire.value(commentaireId);
        
        return {
            ...commentaire,
            reponses: commentaireReponses
        };
    }

    function clearCurrentCommentaire() {
        currentCommentaire.value = null;
    }

    function resetCommentairesError() {
        commentairesError.value = null;
    }

    function clearCommentairesStore() {
        commentaires.value = [];
        reponses.value = [];
        currentCommentaire.value = null;
        commentairesError.value = null;
    }

    // =================================================================
    // ACTIONS EXISTANTES POUR LES DOSSIERS (inchangées)
    // =================================================================
    
    function attachAffair(affair){
        currentDossier.value = affair;
        //console.log('Dossier selectionné', affair);
        return currentDossier;
    }
    
    async function fetchCategories() {
        try {
            const response = await api.get(`/manager/category`);
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
             // If caller didn't specify est_archive, backend now defaults to est_archive=false
            const response = await api.get(`/manager/affairs`, { params });
            dossiers.value = response.data.data.dossiers;
            stats.value = response.data.data.metadata;
            //console.log("Dossiers chargés", dossiers.value)
            return response.data;
        } catch (err) {
            error.value = err.response?.data?.error || 'Erreur lors du chargement des dossiers'; 
            throw err;
        } finally {
            loading.value = false;
        }
    }

    /**
     * Recherche de dossiers (pour autocomplétion)
     */
    async function searchDossiers(query, searchParams = {}) {
        loading.value = true;
        error.value = null;

        try {
            const params = {
                search: query,
                page_size: searchParams.page_size || 10, 
                ...searchParams
            };

            const response = await api.get('/manager/affairs', { params });

            // Réponse shape: response.data.data.dossiers
            const dossiersRes = response.data?.data?.dossiers || [];
            return dossiersRes;
        } catch (err) {
            error.value = err.response?.data?.error || err.message || 'Erreur lors de la recherche de dossiers';
            //console.error('Erreur searchDossiers:', err);
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function fetchArchivesDossiers(){
        try {
            const response = await api.get(`/manager/affairs?est_archive=true`)
            dossiersArchives.value = response.data.data.dossiers
            //console.log('Documents archivés', dossiersArchives)
        } catch (err) {
            error.value = err.response?.data?.error || "Un problème est lors de la réccupération des archives"
            //console.error(error)
        }   
    }

    async function fetchDossierById(id) {
        loading.value = true;
        error.value = null;
        
        try {
            ////console.log('fetchDossierById appelé avec id:', id);
            const response = await api.get(`/manager/affairs/details/${id}/`);
            ////console.log('Réponse fetchDossierById:', response.data);
            currentDossier.value = response.data;
            ////console.log('currentDossier mis à jour:', currentDossier.value);
            return response.data;
        } catch (err) {
            ////console.error('Erreur fetchDossierById:', err);
            error.value = err.response?.data?.error || 'Erreur lors du chargement du dossier';
            ////console.error('Une erreur est intervenue lors de la récupération du dossier');
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function fetchDossiersByClient(clientId, params = {}) {
        loading.value = true;
        error.value = null;

        try {
            const query = { client_id: clientId, ...params };
            const response = await api.get(`/manager/affairs`, { params: query });
            customerDossier.value = response.data.data.dossiers;
            return response.data;
        } catch (err) {
            error.value = err.response?.data?.error || 'Erreur lors du chargement des dossiers du client';
            throw err;
        } finally {
            loading.value = false;
        }
    }

    async function createDossier(dossierData) {
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
        loading.value = true;
        error.value = null;
        
        try {
            const method = partial ? 'patch' : 'put';
            const response = await api[method](`/manager/affairs/details/${id}/`, dossierData);
            
            const index = dossiers.value.findIndex(d => d.id === id);
            if (index !== -1) {
                dossiers.value[index] = response.data;
            }
            
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
            await api.delete(`/manager/affairs/details/${id}/`);
            
            const index = dossiers.value.findIndex(d => d.id === id);
            if (index !== -1) {
                dossiers.value.splice(index, 1);
            }
            
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
        clearCommentairesStore();
        localStorage.removeItem(CACHE_KEY);
    }

    // =================================================================
    // WATCHER POUR CACHE - DÉCLENCHÉ À CHAQUE CHANGEMENT
    // =================================================================
    watch(
        [
            dossiers, 
            currentDossier, 
            stats, 
            customerDossier, 
            categories, 
            dossiersArchives,
            commentaires,
            currentCommentaire,
            reponses
        ], 
        ([
            newDossiers, 
            newCurrentDossier, 
            newStats, 
            newCustomerDossier, 
            newCategories, 
            newDossiersArchives,
            newCommentaires,
            newCurrentCommentaire,
            newReponses
        ]) => {
            saveStateToCache({
                dossiers: newDossiers,
                currentDossier: newCurrentDossier,
                stats: newStats,
                customerDossier: newCustomerDossier,
                categories: newCategories,
                dossiersArchives: newDossiersArchives,
                commentaires: newCommentaires,
                currentCommentaire: newCurrentCommentaire,
                reponses: newReponses
            });
        }, 
        { deep: true, immediate: false }
    );

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
        
        // NOUVEAU : State pour commentaires
        commentaires,
        currentCommentaire,
        reponses,
        commentairesLoading,
        commentairesError,

        // Getters
        totalDossiers,
        dossiersActifs,
        dossiersEnRetard,
        dossiersParStatut,
        getCurrentDossier,
        
        // NOUVEAU : Getters pour commentaires
        getCommentairesByDossier,
        getReponsesByCommentaire,
        commentairesCount,
        reponsesCount,

        // Actions
        attachAffair,
        
        // Actions pour commentaires
        fetchCommentairesByDossier,
        fetchCommentaireById,
        createCommentaire,
        updateCommentaire,
        deleteCommentaire,
        fetchReponsesByCommentaire,
        createReponse,
        updateReponse,
        deleteReponse,
        loadCommentairesForDossier,
        getCommentaireWithReponses,
        clearCurrentCommentaire,
        resetCommentairesError,
        clearCommentairesStore,
        // Recherche
        searchDossiers,

        // Actions existantes pour dossiers
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