<template>
    <section class="flex flex-col min-h-screen gap-8">

        <div class="grid grid-cols-2 gap-6 flex-1">
            <!-- Colonne gauche fixe -->
            <div class="sticky top-4 self-start">

                <cardsaffairs
                    title="Dossier Marketing Q4"
                    description="Campagne publicitaire pour le lancement du nouveau produit"
                    status="active"
                    date="20 Jan 2024"
                    clientName="Entreprise ABC"
                    :progress="80"
                    @view="handleView"
                    @edit="handleEdit"
                    @action="handleAction"
                />
            </div>

            <!-- Colonne droite défilante -->
            <div class="sticky top-4 self-start">
                <uploadFileButton />
            </div>
        </div>

        <div class="">
            <documentList/>
        </div>
    </section>
</template>

<script>
import cardsaffairs from '../cards/cardsaffairs.vue';
import documentList from '../items/documentList.vue';
import fileInput from '../input/fileInput.vue';
import uploadFileButton from '../button/uploadFileButton.vue';

export default {
    components: {
        cardsaffairs,
        documentList,
        fileInput,
        uploadFileButton
    },
    methods: {
        handleView() {
            // Votre logique
        },
        handleEdit() {
            // Votre logique
        },
        handleAction() {
            // Votre logique
        }
    }
}
</script>