import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '@/_services/api';

export const useCustomerStore = defineStore('customer', () => {
    // --- STATE ---
    const customers = ref([]);
    const currentCustomer = ref(null);
    const loading = ref(false);
    const error = ref(null);
    const pagination = ref({
        page: 1,
        page_size: 20,
        total: 0,
        pages: 0
    });
    const filters = ref({
        type_client: '',
        statut: '',
        search: '' 
    });

    // Statistiques mensuelles pour les graphiques
    const monthlyStats = ref({ labels: [], data: [] });

    // --- GETTERS ---
    const getCustomers = computed(() => customers.value);
    const getCurrentCustomer = computed(() => currentCustomer.value);
    const isLoading = computed(() => loading.value);
    const getError = computed(() => error.value);
    const getPagination = computed(() => pagination.value);
    const getFilters = computed(() => filters.value);
    const getMonthlyStats = computed(() => monthlyStats.value);

    // --- ATTACH CUSTOMER ---
    function attachCustomer(customer){
        currentCustomer.value = customer
    }

    // Clients par type
    const physicalCustomers = computed(() => 
        customers.value.filter(c => c.type_client === 'PERSONNE_PHYSIQUE')
    );
    
    const moralCustomers = computed(() => 
        customers.value.filter(c => c.type_client === 'PERSONNE_MORALE')
    );

    // Statistiques
    const customersStats = computed(() => ({
        total: customers.value.length,
        physical: physicalCustomers.value.length,
        moral: moralCustomers.value.length,
        active: customers.value.filter(c => c.statut === 'ACTIF').length,
        prospect: customers.value.filter(c => c.statut === 'PROSPECT').length,
        inactive: customers.value.filter(c => c.statut === 'INACTIF').length
    }));

    // --- ACTIONS ---

    /*
     Récupère la liste des clients avec pagination et filtres
    */
    async function fetchCustomers(params = {}) {
        loading.value = true;
        error.value = null;

        try {
            // Fusionner les paramètres avec les filtres actuels et la pagination
            const queryParams = {
                page: params.page || pagination.value.page,
                page_size: params.page_size || pagination.value.page_size,
                ...filters.value,
                ...params
            };

            // Nettoyer les paramètres vides
            Object.keys(queryParams).forEach(key => {
                if (queryParams[key] === '' || queryParams[key] === null) {
                    delete queryParams[key];
                }
            });

            // Get Differents customer

            const response = await api.get('/manager/clients/', { params: queryParams });
            
            if (response.data.success) {
                customers.value = response.data.clients;
                pagination.value = response.data.pagination;
                
                // Mettre à jour les filtres appliqués
                if (response.data.filters) {
                    filters.value = { ...filters.value, ...response.data.filters };
                }

                // Afficher les clients
                console.log(response.data.clients)

                return response.data;
            } else {
                throw new Error(response.data.message || 'Erreur lors de la récupération des clients');
            }
        } catch (err) {
            error.value = err.response?.data?.message || err.message || 'Erreur réseau';
            console.error('Erreur fetchCustomers:', err);
            throw err;
        } finally {
            loading.value = false;
        }
    }

        /**
         * Récupère les statistiques mensuelles des clients (labels et data)
         */
        async function fetchCustomersMonthlyStats() {
            loading.value = true;
            error.value = null;

            try {
                const response = await api.get('/manager/clients/stats/monthly/');
                if (response.data.success) {
                    monthlyStats.value = {
                        labels: response.data.labels || [],
                        data: response.data.data || []
                    };
                    return monthlyStats.value;
                } else {
                    throw new Error(response.data.message || 'Erreur lors du chargement des statistiques');
                }
            } catch (err) {
                error.value = err.response?.data?.message || err.message || 'Erreur réseau';
                console.error('Erreur fetchCustomersMonthlyStats:', err);
                throw err;
            } finally {
                loading.value = false;
            }
        }

    /**
     * Récupère les détails d'un client spécifique
     */
    async function fetchCustomerById(customerId) {
        loading.value = true;
        error.value = null;

        try {
            const response = await api.get(`/manager/clients/${customerId}/`);
            
            if (response.data.success) {
                currentCustomer.value = response.data.client;
                console.log('Détails du client:', response.data.client);
                return response.data.client;
            } else {
                throw new Error(response.data.message || 'Client non trouvé');
            }
        } catch (err) {
            error.value = err.response?.data?.message || err.message || 'Erreur réseau';
            console.error('Erreur fetchCustomerById:', err);
            throw err;
        } finally {
            loading.value = false;
        }
    }

    /**
     * Recherche avancée de clients
     */
    async function searchCustomers(query, searchParams = {}) {
        loading.value = true;
        error.value = null;

        try {
            const params = {
                q: query,
                ...searchParams
            };

            const response = await api.get('/manager/clients/search/', { params });
            
            if (response.data.success) {
                return response.data.results;
            } else {
                throw new Error(response.data.message || 'Erreur lors de la recherche');
            }
        } catch (err) {
            error.value = err.response?.data?.message || err.message || 'Erreur réseau';
            console.error('Erreur searchCustomers:', err);
            throw err;
        } finally {
            loading.value = false;
        }
    }

    /**
     * Crée un nouveau client
     */
    async function createCustomer(customerData) {
        loading.value = true;
        error.value = null;

        try {
            const response = await api.post('/manager/clients/ajouter/', customerData);
            
            if (response.data.success) {
                // Ajouter le nouveau client à la liste
                customers.value.unshift(response.data.client);
                
                // Mettre à jour la pagination
                pagination.value.total += 1;
                pagination.value.pages = Math.ceil(pagination.value.total / pagination.value.page_size);
                
                return response.data.client;
            } else {
                throw new Error(response.data.message || 'Erreur lors de la création du client');
            }
        } catch (err) {
            error.value = err.response?.data?.errors || err.response?.data?.message || err.message || 'Erreur réseau';
            console.error('Erreur createCustomer:', err);
            throw err;
        } finally {
            loading.value = false;
        }
    }

    /**
     * Met à jour un client existant
     */
    async function updateCustomer(customerId, customerData) {
        loading.value = true;
        error.value = null;

        try {
            const response = await api.put(`/manager/clients/${customerId}/`, customerData);
            
            if (response.data.success) {
                // Mettre à jour le client dans la liste
                const index = customers.value.findIndex(c => c.id === customerId);
                if (index !== -1) {
                    customers.value[index] = response.data.client;
                }
                
                // Mettre à jour le client courant si c'est le même
                if (currentCustomer.value && currentCustomer.value.id === customerId) {
                    currentCustomer.value = response.data.client;
                }
                
                return response.data.client;
            } else {
                throw new Error(response.data.message || 'Erreur lors de la mise à jour du client');
            }
        } catch (err) {
            error.value = err.response?.data?.errors || err.response?.data?.message || err.message || 'Erreur réseau';
            console.error('Erreur updateCustomer:', err);
            throw err;
        } finally {
            loading.value = false;
        }
    }

    /**
     * Change le statut d'un client (soft delete)
     */
    async function deleteCustomer(customerId) {
        loading.value = true;
        error.value = null;

        try {
            const response = await api.delete(`/manager/clients/${customerId}/delete/`);
            
            if (response.data.success) {
                // Retirer le client de la liste ou marquer comme inactif
                const index = customers.value.findIndex(c => c.id === customerId);
                if (index !== -1) {
                    customers.value[index].statut = 'INACTIF';
                }
                
                return response.data.message;
            } else {
                throw new Error(response.data.message || 'Erreur lors de la suppression du client');
            }
        } catch (err) {
            error.value = err.response?.data?.message || err.message || 'Erreur réseau';
            console.error('Erreur deleteCustomer:', err);
            throw err;
        } finally {
            loading.value = false;
        }
    }

    /**
     * Met à jour les filtres de recherche
     */
    function setFilters(newFilters) {
        filters.value = { ...filters.value, ...newFilters };
        // Réinitialiser à la première page lors du changement de filtres
        pagination.value.page = 1;
    }

    /**
     * Réinitialise les filtres
     */
    function resetFilters() {
        filters.value = {
            type_client: '',
            statut: '',
            search: ''
        };
        pagination.value.page = 1;
    }

    /**
     * Change la page courante
     */
    function setPage(newPage) {
        if (newPage >= 1 && newPage <= pagination.value.pages) {
            pagination.value.page = newPage;
        }
    }

    /**
     * Change la taille de page
     */
    function setPageSize(newSize) {
        pagination.value.page_size = newSize;
        pagination.value.page = 1; // Retour à la première page
    }

    /**
     * Réinitialise le store
     */
    function resetStore() {
        customers.value = [];
        currentCustomer.value = null;
        loading.value = false;
        error.value = null;
        pagination.value = {
            page: 1,
            page_size: 20,
            total: 0,
            pages: 0
        };
        filters.value = {
            type_client: '',
            statut: '',
            search: ''
        };
    }

    return {
        // State
        customers,
        currentCustomer,
        loading,
        error,
        pagination,
        filters,

        // Getters
        getCustomers,
        getCurrentCustomer,
        isLoading,
        getError,
        getPagination,
        getFilters,
        physicalCustomers,
        moralCustomers,
        customersStats,

        //
        attachCustomer,

        // Actions
        fetchCustomers,
        fetchCustomerById,
        searchCustomers,
        createCustomer,
        updateCustomer,
        deleteCustomer,
        setFilters,
        resetFilters,
        setPage,
        setPageSize,
        resetStore
        , fetchCustomersMonthlyStats
    };
});