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
                    <p class="user-role">{{ userRole }}</p>
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
                id: 'recent-documents',
                label: 'Dossiers récents',
                route: 'dashboard-recents', // Vous devrez créer cette route
                icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 12c0-1.232-.046-2.453-.138-3.662a4.006 4.006 0 0 0-3.7-3.7 48.678 48.678 0 0 0-7.324 0 4.006 4.006 0 0 0-3.7 3.7c-.017.22-.032.441-.046.662M19.5 12l3-3m-3 3-3-3m-12 3c0 1.232.046 2.453.138 3.662a4.006 4.006 0 0 0 3.7 3.7 48.656 48.656 0 0 0 7.324 0 4.006 4.006 0 0 0 3.7-3.7c.017-.22.032-.441.046-.662M4.5 12l3 3m-3-3-3 3" />
                </svg>`,     
            },
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
                id: 'calendrier',
                label: 'Calendrier',
                route: 'calendrier', // Ajouter la route
                icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
                </svg>`,
            },
            {
                id: 'equipe',
                label: 'Équipe',
                count: 8,
                icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 0 0 3.741-.479 3 3 0 0 0-4.682-2.72m.94 3.198.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0 1 12 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 0 1 6 18.719m12 0a5.971 5.971 0 0 0-.941-3.197m0 0A5.995 5.995 0 0 0 12 12.75a5.995 5.995 0 0 0-5.058 2.772m0 0a3 3 0 0 0-4.681 2.72 8.986 8.986 0 0 0 3.74.477m.94-3.197a5.971 5.971 0 0 0-.94 3.197M15 6.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm6 3a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Zm-13.5 0a2.25 2.25 0 1 1-4.5 0 2.25 2.25 0 0 1 4.5 0Z" />
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
                id: 'parametres',
                label: 'Paramètres',
                icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.325.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 0 1 1.37.49l1.296 2.247a1.125 1.125 0 0 1-.26 1.431l-1.003.827c-.293.241-.438.613-.43.992a7.723 7.723 0 0 1 0 .255c-.008.378.137.75.43.991l1.004.827c.424.35.534.955.26 1.43l-1.298 2.247a1.125 1.125 0 0 1-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.47 6.47 0 0 1-.22.128c-.331.183-.581.495-.644.869l-.213 1.281c-.09.543-.56.94-1.11.94h-2.594c-.55 0-1.019-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 0 1-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 0 1-1.369-.49l-1.297-2.247a1.125 1.125 0 0 1 .26-1.431l1.004-.827c.292-.24.437-.613.43-.991a6.932 6.932 0 0 1 0-.255c.007-.38-.138-.751-.43-.992l-1.004-.827a1.125 1.125 0 0 1-.26-1.43l1.297-2.247a1.125 1.125 0 0 1 1.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.086.22-.128.332-.183.582-.495.644-.869l.214-1.28Z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                </svg>`,
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
            
            if (!confirm('Êtes-vous sûr de vouloir vous déconnecter ?')) {
                return;
            }
            
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