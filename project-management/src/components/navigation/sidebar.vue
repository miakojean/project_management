<template>
    <aside class="sidebar-area">
        <!-- Brand / Logo -->
        <brand/>

        <!-- Navigation principale -->
        <nav class="main-nav">
            <ul class="nav-list">
                <li 
                    v-for="item in mainMenuItems" 
                    :key="item.id"
                    :class="['nav-item', { 'active': activeItem === item.id }]"
                    @click="setActive(item.id)"
                >
                    <div class="nav-link">
                        <span class="nav-icon" v-html="item.icon"></span>
                        <span class="nav-text">{{ item.label }}</span>
                        <span v-if="item.badge" class="nav-badge">{{ item.badge }}</span>
                    </div>
                </li>
            </ul>

            <!-- Section séparée -->
            <div class="nav-section">
                <h5 class="section-title">Gestion</h5>
                <ul class="nav-list">
                    <li 
                        v-for="item in managementItems" 
                        :key="item.id"
                        :class="['nav-item', { 'active': activeItem === item.id }]"
                        @click="setActive(item.id)"
                    >
                        <div class="nav-link">
                            <span class="nav-icon" v-html="item.icon"></span>
                            <span class="nav-text">{{ item.label }}</span>
                            <span v-if="item.count" class="nav-count">{{ item.count }}</span>
                        </div>
                    </li>
                </ul>
            </div>
        </nav>

        <!-- Section du bas (profil + déconnexion) -->
        <div class="sidebar-footer">
            <!-- Profil utilisateur -->
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

            <!-- Bouton de déconnexion -->
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
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import brand from './brand.vue';

export default {
    name: 'Sidebar',
    components: {
        brand
    },
    setup() {
        const router = useRouter();
        const authStore = useAuthStore();
        
        // Réactives
        const activeItem = ref('dashboard');
        const isLoggingOut = ref(false);
        
        // Données des menus
        const mainMenuItems = ref([
            {
                id: 'dashboard',
                label: 'Dashboard',
                icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25A2.25 2.25 0 0 1 13.5 18v-2.25Z" />
                </svg>`,
            },
            {
                id: 'dossiers',
                label: 'Dossiers',
                badge: '12',
                icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
                </svg>`,
            },
            {
                id: 'documents',
                label: 'Documents',
                icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                </svg>`,
            },
            {
                id: 'calendrier',
                label: 'Calendrier',
                icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6.75 3v2.25M17.25 3v2.25M3 18.75V7.5a2.25 2.25 0 0 1 2.25-2.25h13.5A2.25 2.25 0 0 1 21 7.5v11.25m-18 0A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75m-18 0v-7.5A2.25 2.25 0 0 1 5.25 9h13.5A2.25 2.25 0 0 1 21 11.25v7.5" />
                </svg>`,
            },
        ]);

        const managementItems = ref([
            {
                id: 'getCustomer',
                label: 'Clients',
                count: 45,
                icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 19.128a9.38 9.38 0 0 0 2.625.372 9.337 9.337 0 0 0 4.121-.952 4.125 4.125 0 0 0-7.533-2.493M15 19.128v-.003c0-1.113-.285-2.16-.786-3.07M15 19.128v.106A12.318 12.318 0 0 1 8.624 21c-2.331 0-4.512-.645-6.374-1.766l-.001-.109a6.375 6.375 0 0 1 11.964-3.07M12 6.375a3.375 3.375 0 1 1-6.75 0 3.375 3.375 0 0 1 6.75 0Zm8.25 2.25a2.625 2.625 0 1 1-5.25 0 2.625 2.625 0 0 1 5.25 0Z" />
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
                id: 'rapports',
                label: 'Rapports',
                icon: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 6a7.5 7.5 0 1 0 7.5 7.5h-7.5V6Z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 10.5H21A7.5 7.5 0 0 0 13.5 3v7.5Z" />
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

        // Computed
        const userName = computed(() => {
            return authStore.user ? 
                `${authStore.user.first_name || ''} ${authStore.user.last_name || ''}`.trim() || 
                authStore.user.username : 
                'Utilisateur';
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
            activeItem.value = itemId;
            console.log('📍 Navigation vers:', itemId);
            
            if (authStore.isAuthenticated) {
                router.push({ name: itemId });
            } else {
                console.log('🚫 Non authentifié, redirection login');
                router.push('/login');
            }
        };

        const toggleProfileMenu = () => {
            console.log('👤 Toggle profile menu');
            // Logique pour afficher/masquer le menu profil
        };

        const loadCurrentUser = async () => {
            try {
                console.log('🔄 Chargement utilisateur dans sidebar...');
                
                if (!authStore.isAuthenticated) {
                    const token = sessionStorage.getItem('authToken') || localStorage.getItem('authToken');
                    if (!token) {
                        console.log('🚫 Pas de token, redirection login');
                        router.push('/login');
                        return;
                    }
                    
                    await authStore.fetchCurrentUser();
                }
                
                console.log('✅ Utilisateur chargé dans sidebar');
                
            } catch (error) {
                console.error('❌ Erreur chargement utilisateur sidebar:', error);
                router.push('/login');
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
                router.push('/login');
            } catch (error) {
                console.error('❌ Erreur déconnexion:', error);
                router.push('/login');
            } finally {
                isLoggingOut.value = false;
            }
        };

        // Lifecycle
        onMounted(() => {
            loadCurrentUser();
        });

        // Return
        return {
            // Réactives
            activeItem,
            isLoggingOut,
            mainMenuItems,
            managementItems,
            
            // Computed
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
.sidebar-area {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: #ffffff;
}

/* Brand / Logo */
.brand {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1.5rem 1rem;
    border-bottom: 1px solid #f3f4f6;
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
}

.brand-icon svg {
    width: 24px;
    height: 24px;
}

.brand h4 {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1f2937;
    margin: 0;
}

/* Navigation principale */
.main-nav {
    flex: 1;
    padding: 1rem 0;
    overflow-y: auto;
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

.nav-link {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
    color: #6b7280;
    font-size: 0.875rem;
    font-weight: 500;
    transition: all 0.2s ease;
}

.nav-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 20px;
    height: 20px;
    flex-shrink: 0;
}

.nav-icon svg {
    width: 20px;
    height: 20px;
}

.nav-text {
    flex: 1;
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
}

.nav-count {
    color: #9ca3af;
    font-size: 0.75rem;
    font-weight: 500;
}

/* État actif */
.nav-item.active {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(37, 99, 235, 0.05) 100%);
}

.nav-item.active .nav-link {
    color: var(--primary-color, #3b82f6);
}

.nav-item.active .nav-icon {
    color: var(--primary-color, #3b82f6);
}

/* Hover */
.nav-item:not(.active):hover {
    background: #f9fafb;
}

.nav-item:not(.active):hover .nav-link {
    color: #374151;
}

/* Section séparée */
.nav-section {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #f3f4f6;
}

.section-title {
    padding: 0 1.5rem;
    margin: 0 0 0.75rem 0;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #9ca3af;
}

/* Footer de la sidebar */
.sidebar-footer {
    padding: 1rem;
    border-top: 1px solid #f3f4f6;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

/* Profil utilisateur */
.user-profile {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.75rem;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: all 0.2s ease;
}

.user-profile:hover {
    background: #f9fafb;
}

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
}

.user-name {
    font-size: 0.875rem;
    font-weight: 600;
    color: #1f2937;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.user-role {
    font-size: 0.75rem;
    color: #6b7280;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.chevron-icon {
    width: 16px;
    height: 16px;
    color: #9ca3af;
    transition: transform 0.2s ease;
}

.user-profile:hover .chevron-icon {
    transform: translateY(-2px);
}

/* Bouton de déconnexion */
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
}

.logout-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.logout-btn svg {
    width: 18px;
    height: 18px;
}

.logout-btn:hover:not(:disabled) {
    background: #fee2e2;
    border-color: #fecaca;
    transform: translateY(-1px);
}

/* Scrollbar personnalisée */
.main-nav::-webkit-scrollbar {
    width: 4px;
}

.main-nav::-webkit-scrollbar-track {
    background: transparent;
}

.main-nav::-webkit-scrollbar-thumb {
    background: #e5e7eb;
    border-radius: 2px;
}

.main-nav::-webkit-scrollbar-thumb:hover {
    background: #d1d5db;
}

/* Responsive */
@media (max-width: 768px) {
    .brand h4 {
        display: none;
    }
    
    .nav-text,
    .nav-badge,
    .nav-count,
    .user-info,
    .logout-btn span {
        display: none;
    }
    
    .nav-item {
        margin: 0.25rem 0.5rem;
    }
    
    .nav-link {
        justify-content: center;
        padding: 0.75rem;
    }
}
</style>