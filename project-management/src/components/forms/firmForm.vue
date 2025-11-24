<template>
    <form class="form-container" @submit.prevent="handleSubmit">
        <div class="form-grid">
            
            <div class="form-row">
                <inputfamily 
                    identifiant="Raison morale" 
                    label="Raison morale" 
                    placeholder="Entrer le nom l'entreprise"
                    v-model="formData.nom"
                    :required="true"
                />
                <inputfamily 
                    identifiant="Forme juridique" 
                    label="Forme juridique" 
                    placeholder="Entrer la forme juridique"
                    v-model="formData.prenoms"
                    :required="true"
                />
                <inputfamily 
                    identifiant="Numéro RCCM" 
                    label="Numéro RCCM" 
                    placeholder="Entrer votre uméro rccm"
                    type="texte"
                    v-model="formData.date_naissance"
                />
            </div>
            
            <div class="form-row">
                <inputfamily 
                    identifiant="CompteContribuable" 
                    label="Numéro Compte Contribuable" 
                    placeholder="Numéro Compte Contribuable"
                    v-model="formData.lieu_naissance"
                />
                <inputfamily 
                    identifiant="Capitalsocial" 
                    label="Capital social" 
                    placeholder="Votre Capital social"
                    v-model="formData.lieu_naissance"
                />
                <inputfamily 
                    identifiant="adresse" 
                    label="Adresse" 
                    placeholder="Entrer l'adresse"
                    type="text"
                    v-model="formData.adresse"
                    :required="true"
                />
            </div>

            <div class="form-row">
                <inputfamily 
                    identifiant="ville" 
                    label="Ville" 
                    placeholder="Entrer la ville"
                    v-model="formData.ville"
                />
                <inputfamily 
                    identifiant="telephone" 
                    label="Téléphone" 
                    placeholder="Entrer le téléphone"
                    type="tel"
                    v-model="formData.telephone_1"
                />

                <inputfamily 
                    identifiant="telephone 2" 
                    label="Téléphone 2" 
                    placeholder="Entrer le deuxième numéro"
                    v-model="formData.telephone_2"
                />
                
            </div>

            <div class="form-row">
                <inputfamily 
                    identifiant="email" 
                    label="Email" 
                    placeholder="Entrer votre email"
                    v-model="formData.email"
                />
                <inputfamily 
                    identifiant="representantLegal" 
                    label="Nom du representant legal" 
                    placeholder="Entrer le pays"
                    v-model="formData.representant_legal_nom"
                />
                <inputfamily 
                    identifiant="profession" 
                    label="Profession" 
                    placeholder="Entrer la profession"
                    v-model="formData.representant_legal_fonction"
                />
            </div>
        </div>

        <div class="form-actions">
            <prevButton @click="handlePrevStep"/>
            <mainButton 
                :loading="isLoading"
                label="Ajouter client"
                type="submit"
            >
                
            </mainButton>
        </div>
    </form>
</template>

<script>
import { ref, reactive } from 'vue';
import inputfamily from '../input/inputfamily.vue';
import mainButton from '../button/mainButton.vue';
import prevButton from '../button/prevButton.vue';
export default {
    name: 'ClientPhysiqueForm',
    components: {
        inputfamily,
        mainButton,
        prevButton,
    },
    emits: ['submit', 'prevstep'],
    setup(props, { emit }) {
        const isLoading = ref(false);
        
        const formData = reactive({
            type:'PERSONNE_PHYSIQUE',
            nom: '',
            prenoms: '',
            date_naissance: '',
            lieu_naissance: '',
            adresse: '',
            ville: '',
            commune:'',
            telephone_1: '',
            telephone_2: '',
            email: '',
            representant_legal_nom: '',
            representant_legal_fonction:'',
            charge_de_clientele:'',
        });

        const handlePrevStep = () => {
            emit('prevstep');
        };

        const handleSubmit = async () => {
            isLoading.value = true;
            
            try {
                // Validation des champs requis
                if (!formData.nomComplet || !formData.prenoms || !formData.email) {
                    alert('Veuillez remplir les champs obligatoires');
                    return;
                }

                // Simulation d'appel API
                await new Promise(resolve => setTimeout(resolve, 1000));
                
                // Émission des données
                emit('submit', {
                    ...formData,
                    type: 'physique'
                });

                // Réinitialisation du formulaire
                Object.keys(formData).forEach(key => {
                    formData[key] = '';
                });

            } catch (error) {
                console.error('Erreur lors de la soumission:', error);
            } finally {
                isLoading.value = false;
            }
        };

        return {
            isLoading,
            formData,
            handleSubmit,
            handlePrevStep
        };
    }
};
</script>

<style scoped>
.form-container {
    width: 100%;
    max-width: 1000px; /* Augmenté un peu pour accommoder 3 colonnes */
    margin: 0 auto;
    padding-top: 4rem;
}

.form-grid {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    width: 100%;
}

.form-row {
    display: grid;
    /* C'est ici que se joue le 3 par 3 */
    grid-template-columns: repeat(3, 1fr); 
    gap: 1rem;
    align-items: start;
}

.form-actions {
    display: flex;
    justify-content: center;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e5e7eb;
    width: 100%;
    gap: 2rem;
}

/* Responsive */
@media (max-width: 992px) {
    /* Sur tablette moyenne, on passe à 2 colonnes */
    .form-row {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 600px) {
    /* Sur mobile, on passe à 1 colonne */
    .form-row {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .form-actions {
        justify-content: center;
    }
    
    .form-container {
        padding: 0 1rem;
    }
}

/* Animation */
.form-row {
    animation: fadeInUp 0.5s ease;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Stagger animation pour les lignes */
.form-row:nth-child(1) { animation-delay: 0.1s; }
.form-row:nth-child(2) { animation-delay: 0.2s; }
.form-row:nth-child(3) { animation-delay: 0.3s; }
.form-row:nth-child(4) { animation-delay: 0.4s; }
</style>