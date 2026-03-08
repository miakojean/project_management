<template>
    <main class="center__flex__column">
        <affairForm
            @notification="handleNotification"
        />
        <notificationPopup 
            :message="notificationMessage"
            :type="notificationType"
            :visible="showNotification"
            :duration="notificationDuration"
            @close="showNotification = false"
        />
    </main>
</template>

<script>
import affairForm from '../forms/affairForm.vue';
import notificationPopup from '../tools/notificationPopup.vue';
import { ref } from 'vue';
export default {
    components:{
        affairForm,
        notificationPopup
    },

    setup(){
        // Gestion des notifications
        const showNotification = ref(false);
        const notificationMessage = ref('');
        const notificationType = ref('success');
        const notificationDuration = ref(3000);

        const handleNotification = (notification) => {
            //console.log('📢 Notification reçue:', notification);
            showNotification.value = true;
            notificationMessage.value = notification.message;
            notificationType.value = notification.type;
            // Clamp to maximum 3000ms
            notificationDuration.value = Math.min(notification.duration || 3000, 3000);

            // Auto-hide après la durée spécifiée
            setTimeout(() => {
                showNotification.value = false;
            }, notificationDuration.value);
        };

        return{
            showNotification,
            notificationDuration,
            notificationMessage,
            notificationType,

            handleNotification,
        }
    }
}
</script>

<style scoped>

main{
    min-height: 100vh;
}

</style>