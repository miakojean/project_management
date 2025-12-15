<template>
    <aside class="sidebar-area">
        
        <brand/>

        <nav class="main-nav">
            <ul class="nav-list">
                <li 
                    v-for="item in mainMenuItems" 
                    :key="item.id"
                    :class="['nav-item', { 'active': isActive(item.route) }]"
                    @click="navigateTo(item.route)"
                >
                    <div class="nav-link">
                        <span class="nav-icon" v-html="item.icon"></span>
                        <span class="nav-text">{{ item.label }}</span>
                        <!-- Ajout du badge pour les dossiers -->
                        <span v-if="item.id === 'dossiers'" class="nav-count">
                            {{ dossiersCount }}
                        </span>
                        <span v-else-if="item.badge" class="nav-badge">{{ item.badge }}</span>
                    </div>
                </li>
            </ul>

            <div class="nav-section">
                <h5 class="section-title">Gestion</h5>
                <ul class="nav-list">
                    <li 
                            v-for="item in managementItems" 
                            :key="item.id"
                            :class="['nav-item', { 'active': isActive(item.route) }]"
                            @click="navigateTo(item.route)"
                        >
                        <div class="nav-link">
                            <span class="nav-icon" v-html="item.icon"></span>
                            <span class="nav-text">{{ item.label }}</span>
                            <span v-if="item.id === 'getCustomer'" class="nav-count">
                                {{ customersCount }}
                            </span>
                            <span v-if="item.id === 'Archives'" class="nav-count">
                                {{ dossiersArchivesCount }}
                            </span>
                            <span v-else-if="item.count" class="nav-count">
                                {{ item.count }}
                            </span>
                        </div>
                    </li>
                </ul>
            </div>
        </nav>

        <div class="sidebar-footer">
            <div class="user-profile" @click="toggleProfileMenu">
                <div class="user-avatar">
                    <img :src="userAvatar" :alt="userName">
                </div>
                <div class="user-info">
                    <p class="user-name">{{ userName }}</p>
                </div>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="chevron-icon">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5" />
                </svg>
            </div>

            <button class="logout-btn" @click="logout" :disabled="isLoggingOut">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
                </svg>
                <span>{{ isLoggingOut ? 'Déconnexion...' : 'Déconnexion' }}</span>
            </button>
        </div>
    </aside>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useCustomerStore } from '@/stores/custumerStore';
import { useDossierStore } from '@/stores/dossierStore';
import brand from './brand.vue';

export default {
    name: 'Sidebar',
    components: {
        brand
    },
    setup() {
        const route = useRoute();
        const router = useRouter();
        const authStore = useAuthStore();
        const customerStore = useCustomerStore();
        const dossierStore = useDossierStore();
        
        // Réactives
        const isLoggingOut = ref(false);
        
        // Données des menus
        const mainMenuItems = ref([
            {
                id: 'dossiers',
                label: 'Dossiers',
                route: 'dashboard', // Ajouter la route
                icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
                </svg>`,
            },
        ]);

        const managementItems = ref([
            {
                id: 'getCustomer',
                label: 'Clients',
                route:'getCustomer',
                icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
                </svg>`,
            },
            {
                id: 'Archives',
                label: 'Archives',
                route:'archives',
                icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m20.25 7.5-.625 10.632a2.25 2.25 0 0 1-2.247 2.118H6.622a2.25 2.25 0 0 1-2.247-2.118L3.75 7.5M10 11.25h4M3.375 7.5h17.25c.621 0 1.125-.504 1.125-1.125v-1.5c0-.621-.504-1.125-1.125-1.125H3.375c-.621 0-1.125.504-1.125 1.125v1.5c0 .621.504 1.125 1.125 1.125Z" />
                </svg>`,
            },
            {
                id: 'Rapport',
                label: 'Rapport',
                route:'archives',
                icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z" />
                    </svg>
                `,
            },
        ]);

        const currentActiveTab = computed(() => {
            return route.name || 'dashboard';
        });

        const isActive = (routeName) => {
            return currentActiveTab.value === routeName;
        };

        const navigateTo = (routeName) => {
            // Navigation simple : on laisse le route guard gérer l'auth
            router.push({ name: routeName });
        };

        const customersCount = computed(() => {
            return customerStore.customersStats.total || 0;
        });

        const dossiersCount = computed(() => {
            return dossierStore.totalDossiers || dossierStore.stats.count || 0;
        })

        const dossiersArchivesCount = computed(()=>{
            return dossierStore.dossiersArchives.length || 0;
        })

        const userName = computed(() => {
            if (!authStore.user) return 'Utilisateur';
            return `${authStore.user.first_name || ''} ${authStore.user.last_name || ''}`.trim() || 
                authStore.user.username || 'Utilisateur';
        });

        const userRole = computed(() => {
            return authStore.user?.category_title || 'Avocat principal';
        });

        const userAvatar = computed(() => {
            const name = userName.value;
            return `https://ui-avatars.com/api/?name=${encodeURIComponent(name)}&background=3b82f6&color=fff`;
        });

        // Methods
        const setActive = (itemId) => {
            router.push({ name: itemId });
        };

        const toggleProfileMenu = () => {
            console.log('👤 Toggle profile menu');
        };

        // Chargement des données métier uniquement
        const loadCustomers = async () => {
            try {
                console.log('🔄 Chargement des clients dans sidebar...');
                await customerStore.fetchCustomers();
            } catch (error) {
                // On ne bloque pas l'UI et on ne déconnecte pas si ça échoue
                console.warn('⚠️ Erreur non critique chargement clients sidebar:', error);
            }
        };

        const loadDossiers = async () => {
            try {
                console.log('🔄 Chargement des dossiers dans sidebar...');
                await dossierStore.fetchDossiers();
                await dossierStore.fetchArchivesDossiers()
            } catch (error) {
                console.warn('⚠️ Erreur non critique chargement dossiers sidebar:', error);
            }
        };

        const logout = async () => {
            if (isLoggingOut.value) return;
            
            isLoggingOut.value = true;
            
            try {
                await authStore.logout();
            } catch (error) {
                console.error('❌ Erreur déconnexion:', error);
            } finally {
                // On force la redirection vers login quoi qu'il arrive
                isLoggingOut.value = false;
                router.push('/login');
            }
        };

        // Lifecycle simplifié : Pas de vérification d'auth ici !
        onMounted(async () => {
            // On ne charge que les stats utiles à la sidebar
            await loadCustomers();
            await loadDossiers();
            await authStore.fetchCurrentUser();
            console.log('Nombre de dossier archivés',dossiersArchivesCount.value)

        });

        return {
            // Route
            route,
            // Stores
            customerStore,
            dossierStore,
            // Réactives
            isLoggingOut,
            mainMenuItems,
            managementItems,
            isActive,
            navigateTo,
            currentActiveTab,
            // Computed
            customersCount,
            dossiersCount, // EXPOSER dossiersCount
            dossiersArchivesCount,
            userName,
            userRole,
            userAvatar,
            // Methods
            setActive,
            toggleProfileMenu,
            logout
        };
    }
}
</script>

<style scoped>

</style>