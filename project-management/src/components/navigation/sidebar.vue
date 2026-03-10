<template>
    <!-- Overlay mobile (fond semi-transparent) -->
    <div 
        v-if="isMobile && !isCollapsed" 
        class="sidebar-overlay" 
        @click="isCollapsed = true"
    />

    <aside :class="['sidebar-area', { 'collapsed': isCollapsed }]">
        
        <!-- Bouton toggle collapse -->
        <button class="collapse-btn" @click="toggleSidebar" :title="isCollapsed ? 'Agrandir' : 'Réduire'">
            <svg 
                xmlns="http://www.w3.org/2000/svg" 
                fill="none" viewBox="0 0 24 24" 
                stroke-width="2" 
                stroke="currentColor"
                :class="['collapse-icon', { 'rotated': isCollapsed }]"
            >
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
            </svg>
        </button>

        <brand/>

        <nav class="main-nav">
            <ul class="nav-list">
                <li 
                    v-for="item in mainMenuItems" 
                    :key="item.id"
                    :class="['nav-item', { 'active': isActive(item.route) }]"
                    @click="navigateTo(item.route)"
                    :title="isCollapsed ? item.label : ''"
                >
                    <div class="nav-link">
                        <span class="nav-icon" v-html="item.icon"></span>
                        <span class="nav-text">{{ item.label }}</span>
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
                        :title="isCollapsed ? item.label : ''"
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
            <div class="user-profile" @click="toggleProfileMenu" :title="isCollapsed ? userName : ''">
                <div class="user-avatar">
                    <img :src="userAvatar" :alt="userName">
                </div>
                <div class="user-info">
                    <p class="user-name">{{ userName }}</p>
                </div>
                <svg xmlns="http://www.w3.org/2000/svg" 
                    fill="none" viewBox="0 0 24 24" 
                    stroke-width="1.5" 
                    stroke="currentColor" 
                    class="chevron-icon"
                >
                    <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5" />
                </svg>
            </div>

            <button class="logout-btn" @click="logout" :disabled="isLoggingOut" :title="isCollapsed ? 'Déconnexion' : ''">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 9V5.25A2.25 2.25 0 0 1 10.5 3h6a2.25 2.25 0 0 1 2.25 2.25v13.5A2.25 2.25 0 0 1 16.5 21h-6a2.25 2.25 0 0 1-2.25-2.25V15m-3 0-3-3m0 0 3-3m-3 3H15" />
                </svg>
                <span>{{ isLoggingOut ? 'Déconnexion...' : 'Déconnexion' }}</span>
            </button>
        </div>
    </aside>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
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
    props: {
        // Permet au parent (layout) de contrôler l'état collapsed
        isCollapsedProp: {
            type: Boolean,
            default: null
        }
    },
    emits: ['collapse-change'],
    setup(props, { emit }) {
        const route = useRoute();
        const router = useRouter();
        const authStore = useAuthStore();
        const customerStore = useCustomerStore();
        const dossierStore = useDossierStore();
        
        // Réactives
        const isLoggingOut = ref(false);
        const isCollapsed = ref(false);
        const isMobile = ref(false);

        // Sync avec la prop du parent si fournie
        watch(() => props.isCollapsedProp, (val) => {
            if (val !== null) isCollapsed.value = val;
        });

        // Détection mobile
        const checkMobile = () => {
            isMobile.value = window.innerWidth < 768;
            if (isMobile.value) {
                isCollapsed.value = true; // Fermée par défaut sur mobile
            }
        };

        const toggleSidebar = () => {
            isCollapsed.value = !isCollapsed.value;
            emit('collapse-change', isCollapsed.value);
        };

        // Émettre le changement pour que le layout parent puisse s'adapter
        watch(isCollapsed, (val) => {
            emit('collapse-change', val);
        });
        
        // Données des menus
        const mainMenuItems = ref([
            {
                id:'Dashboard',
                label:'Dashboard',
                route:'dashboard',
                icon:`<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z" />
                </svg>`,
            },
            {
                id: 'dossiers',
                label: 'Dossiers',
                route: 'dashboard-affairs',
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
                route:'charts',
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
            router.push({ name: routeName });
            // Fermer la sidebar sur mobile après navigation
            if (isMobile.value) {
                isCollapsed.value = true;
            }
        };

        const customersCount = computed(() => {
            return customerStore.customersStats.total || 0;
        });

        const dossiersCount = computed(() => {
            return dossierStore.totalDossiers || dossierStore.stats.count || 0;
        });

        const dossiersArchivesCount = computed(() => {
            return dossierStore.dossiersArchives.length || 0;
        });

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

        const setActive = (itemId) => {
            router.push({ name: itemId });
        };

        const toggleProfileMenu = () => {};

        const loadCustomers = async () => {
            try {
                await customerStore.fetchCustomers();
            } catch (error) {}
        };

        const loadDossiers = async () => {
            try {
                await dossierStore.fetchDossiers();
                await dossierStore.fetchArchivesDossiers();
            } catch (error) {}
        };

        const logout = async () => {
            if (isLoggingOut.value) return;
            isLoggingOut.value = true;
            try {
                await authStore.logout();
            } catch (error) {
            } finally {
                isLoggingOut.value = false;
                router.push('/login');
            }
        };

        onMounted(async () => {
            checkMobile();
            window.addEventListener('resize', checkMobile);
            await loadCustomers();
            await loadDossiers();
            await authStore.fetchCurrentUser();
        });

        onUnmounted(() => {
            window.removeEventListener('resize', checkMobile);
        });

        return {
            route,
            customerStore,
            dossierStore,
            isLoggingOut,
            isCollapsed,
            isMobile,
            toggleSidebar,
            mainMenuItems,
            managementItems,
            isActive,
            navigateTo,
            currentActiveTab,
            customersCount,
            dossiersCount,
            dossiersArchivesCount,
            userName,
            userRole,
            userAvatar,
            setActive,
            toggleProfileMenu,
            logout
        };
    }
}
</script>

<style scoped>
/* ─── Variables & Base ─────────────────────────────────────── */
.sidebar-area {
    position: relative;
    display: flex;
    flex-direction: column;
    grid-area: sidebar;
    height: 100%;
    width: 100%; /* S'adapte à la colonne de la grille parente */
    min-height: 0;
    background: var(--primary-color);
    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
}

/* La largeur collapsed est pilotée par la grille du layout parent */

/* ─── Overlay mobile ───────────────────────────────────────── */
.sidebar-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    z-index: 40;
    backdrop-filter: blur(2px);
}

/* ─── Bouton collapse ──────────────────────────────────────── */
.collapse-btn {
    position: absolute;
    top: 1.2rem;
    right: -14px;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    background: var(--primary-color);
    border: 2px solid rgba(255, 255, 255, 0.25);
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.2s ease;
    color: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.25);
}

.collapse-btn:hover {
    background: #37cd7f;
    border-color: #37cd7f;
    transform: scale(1.1);
}

.collapse-icon {
    width: 14px;
    height: 14px;
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.collapse-icon.rotated {
    transform: rotate(180deg);
}

/* ─── Brand ────────────────────────────────────────────────── */
.brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1.5rem 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    white-space: nowrap;
    overflow: hidden;
}

.brand-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, var(--primary-color, #3b82f6) 0%, #2563eb 100%);
    border-radius: 0.75rem;
    color: white;
    flex-shrink: 0;
}

.brand-icon svg { width: 24px; height: 24px; }

.brand h4 {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1f2937;
    margin: 0;
    transition: opacity 0.2s ease, width 0.3s ease;
}

/* Cacher les textes en mode collapsed */
.sidebar-area.collapsed .brand h4,
.sidebar-area.collapsed .nav-text,
.sidebar-area.collapsed .nav-badge,
.sidebar-area.collapsed .nav-count,
.sidebar-area.collapsed .user-info,
.sidebar-area.collapsed .logout-btn span,
.sidebar-area.collapsed .section-title,
.sidebar-area.collapsed .chevron-icon {
    opacity: 0;
    width: 0;
    overflow: hidden;
    pointer-events: none;
}

/* ─── Navigation ───────────────────────────────────────────── */
.main-nav {
    flex: 1;
    padding: 1rem 0;
    overflow-y: auto;
    overflow-x: hidden;
}

.nav-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.nav-item {
    margin: 0.25rem 0.75rem;
    border-radius: 0.5rem;
    transition: all 0.2s ease;
    cursor: pointer;
}

.sidebar-area.collapsed .nav-item {
    margin: 0.25rem 0.5rem;
}

.nav-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    color: var(--adn-white-color);
    font-size: 0.875rem;
    font-weight: 500;
    transition: all 0.2s ease;
    white-space: nowrap;
}

.sidebar-area.collapsed .nav-link {
    justify-content: center;
    padding: 0.75rem;
    gap: 0;
}

.nav-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--adn-white-color);
    width: 20px;
    height: 20px;
    flex-shrink: 0;
}

.nav-icon svg {
    width: 20px;
    height: 20px;
    color: var(--adn-white-color);
}

.nav-text {
    flex: 1;
    color: var(--adn-white-color);
    transition: opacity 0.2s ease;
}

.nav-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 20px;
    height: 20px;
    padding: 0 0.375rem;
    background: #ef4444;
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 9999px;
    transition: opacity 0.2s ease;
}

.nav-count {
    color: var(--adn-white-color);
    font-size: 0.75rem;
    font-weight: 500;
    transition: opacity 0.2s ease;
}

/* États actif & hover */
.nav-item.active { background: #37cd7f; }
.nav-item.active .nav-link { color: var(--primary-color, #3b82f6); }
.nav-item.active .nav-icon { color: var(--primary-color, #3b82f6); }
.nav-item:not(.active):hover { background: #37cd7f; }
.nav-item:not(.active):hover .nav-link { color: #374151; }

/* Section séparée */
.nav-section {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.1);
}

.section-title {
    padding: 0 1.5rem;
    margin: 0 0 0.75rem 0;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    color: #ffffff;
    transition: opacity 0.2s ease;
    white-space: nowrap;
    overflow: hidden;
}

/* ─── Footer ───────────────────────────────────────────────── */
.sidebar-footer {
    padding: 1rem;
    border-top: 1px solid rgba(255,255,255,0.1);
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.user-profile {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
    overflow: hidden;
}

.sidebar-area.collapsed .user-profile {
    justify-content: center;
    gap: 0;
    padding: 0.5rem;
}

.user-profile:hover { background: rgba(255,255,255,0.08); }

.user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden;
    flex-shrink: 0;
}

.user-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.user-info {
    flex: 1;
    min-width: 0;
    transition: opacity 0.2s ease;
    overflow: hidden;
}

.user-name {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--adn-white-color);
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.chevron-icon {
    width: 16px;
    height: 16px;
    color: #9ca3af;
    transition: transform 0.2s ease, opacity 0.2s ease;
    flex-shrink: 0;
}

.user-profile:hover .chevron-icon { transform: translateY(-2px); }

/* Bouton déconnexion */
.logout-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    width: 100%;
    padding: 0.75rem;
    background: #fef2f2;
    color: #dc2626;
    border: 1px solid #fee2e2;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
    overflow: hidden;
}

.sidebar-area.collapsed .logout-btn { gap: 0; }

.logout-btn:disabled { opacity: 0.6; cursor: not-allowed; }

.logout-btn svg { width: 18px; height: 18px; flex-shrink: 0; }

.logout-btn:hover:not(:disabled) {
    background: #fee2e2;
    border-color: #fecaca;
    transform: translateY(-1px);
}

/* ─── Scrollbar ────────────────────────────────────────────── */
.main-nav::-webkit-scrollbar { width: 4px; }
.main-nav::-webkit-scrollbar-track { background: transparent; }
.main-nav::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.2); border-radius: 2px; }
.main-nav::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.35); }

/* ─── Responsive mobile ────────────────────────────────────── */
@media (max-width: 768px) {
    .sidebar-area {
        position: fixed;
        left: 0;
        top: 0;
        bottom: 0;
        z-index: 50;
        width: 260px;
        transform: translateX(0);
        transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* Sur mobile, "collapsed" = sidebar hors écran (slide out) */
    .sidebar-area.collapsed {
        width: 260px; /* Garde la largeur, on translate à la place */
        transform: translateX(-100%);
    }

    /* Bouton toggle caché sur mobile (géré via le parent/hamburger) */
    .collapse-btn {
        display: none;
    }
}
</style>