<template>
    <nav>
        <div class="research__box">
            <researchfamily/>
        </div>
        <div class="btn__frame">
            <!-- Icône de notification avec bulle -->
            <addButton/>
            <div class="notification-wrapper">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1" stroke="currentColor" class="size-8">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
                </svg>
                <!-- Bulle de notification -->
                <span v-if="notificationCount > 0" class="notification-bubble">
                    {{ notificationCount > 99 ? '99+' : notificationCount }}
                </span>
            </div>
        </div>
    </nav>
</template>

<script>
import addButton from '../button/addButton.vue';
import researchfamily from '../input/researchfamily.vue';
export default {
    components:{
        addButton,
        researchfamily,
    },
    data() {
        return {
            notificationCount: 3 // Exemple: 3 notifications
        }
    },
    methods: {
        // Méthode pour simuler la réception d'une notification
        addNotification() {
            this.notificationCount++;
        },
        // Méthode pour vider les notifications
        clearNotifications() {
            this.notificationCount = 0;
        }
    }
}
</script>

<style scoped>
nav{
    padding: 1rem;
    display:flex;
    align-items:center;
    justify-content: end;
    gap: 1rem;
    width: 100%;
}

.research__box{
    width: 400px;
}

input{
    border: 1px solid #dbdbdb;
    border-radius: 0.5rem;
    padding: 0.7rem;
    width: 100%;
}

ul{
    display:flex;
    align-items: center;
    gap: 1rem;
}

.btn__frame{
    display: flex;
    align-items: center;
    gap: 1rem;
}

/* Styles pour le wrapper de notification */
.notification-wrapper {
    position: relative;
    display: inline-block;
    cursor: pointer;
}

svg{
    transition: all 0.3s ease;
}

svg:hover{
    background: #dbdbdb;
    border-radius: 50%;
}

/* Styles pour la bulle de notification */
.notification-bubble {
    position: absolute;
    top: -5px;
    right: -5px;
    background: #ff4444;
    color: white;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    font-size: 0.7rem;
    font-weight: bold;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid white;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    animation: pulse 2s infinite;
}

/* Animation pour attirer l'attention */
@keyframes pulse {
    0% {
        transform: scale(1);
        box-shadow: 0 0 0 0 rgba(255, 68, 68, 0.7);
    }
    50% {
        transform: scale(1.05);
        box-shadow: 0 0 0 5px rgba(255, 68, 68, 0);
    }
    100% {
        transform: scale(1);
        box-shadow: 0 0 0 0 rgba(255, 68, 68, 0);
    }
}

/* Version alternative sans animation */
.notification-bubble.no-animation {
    animation: none;
}

/* Différentes couleurs selon le nombre de notifications */
.notification-bubble.low {
    background: #4CAF50; /* Vert pour peu de notifications */
}

.notification-bubble.medium {
    background: #FF9800; /* Orange pour un nombre moyen */
}

.notification-bubble.high {
    background: #ff4444; /* Rouge pour beaucoup de notifications */
}
</style>