<template>
    <section class="flex flex-col min-h-screen">
       

        <div class="grid grid-cols-2 gap-6 flex-1">
            <!-- Colonne gauche fixe -->
            <div class="sticky top-4 self-start">

                <h3 class="w-full text-left mb-4">Détail du dossier ABC</h3>

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
            <div class="overflow-y-auto">
                <documentList/>
            </div>
        </div>
    </section>
</template>

<script>
import cardsaffairs from '../cards/cardsaffairs.vue';
import documentList from '../items/documentList.vue';

export default {
    components: {
        cardsaffairs,
        documentList
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