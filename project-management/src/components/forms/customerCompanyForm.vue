<template>
  <div class="max-w-2xl mx-auto p-6 bg-white shadow-lg rounded-lg mt-10">
    <h2 class="text-2xl font-bold mb-6 text-gray-800 border-b pb-2">
      Enregistrer une nouvelle entreprise
    </h2>

    <div v-if="submitStatus === 'success'" class="mb-4 p-4 bg-green-100 text-green-700 rounded">
      ✅ L'entreprise a été enregistrée avec succès dans la base de données.
    </div>

    <div v-if="submitStatus === 'error'" class="mb-4 p-4 bg-red-100 text-red-700 rounded">
      ❌ Une erreur est survenue lors de l'enregistrement. Veuillez réessayer.
    </div>

    <form @submit.prevent="handleSubmit" class="space-y-6">
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="companyName" class="block text-sm font-medium text-gray-700 mb-1">Nom de l'entreprise *</label>
          <input 
            id="companyName"
            v-model="form.name"
            type="text"
            :class="{'border-red-500': errors.name}"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            placeholder="Ex: Tech Solutions SAS"
          />
          <span v-if="errors.name" class="text-xs text-red-500 mt-1">{{ errors.name }}</span>
        </div>

        <div>
          <label for="siret" class="block text-sm font-medium text-gray-700 mb-1">Numéro SIRET *</label>
          <input 
            id="siret"
            v-model="form.siret"
            type="text"
            maxlength="14"
            @input="filterNumbers"
            :class="{'border-red-500': errors.siret}"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            placeholder="14 chiffres"
          />
          <span v-if="errors.siret" class="text-xs text-red-500 mt-1">{{ errors.siret }}</span>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email professionnel *</label>
          <input 
            id="email"
            v-model="form.email"
            type="email"
            :class="{'border-red-500': errors.email}"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            placeholder="contact@entreprise.com"
          />
          <span v-if="errors.email" class="text-xs text-red-500 mt-1">{{ errors.email }}</span>
        </div>

        <div>
          <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">Téléphone</label>
          <input 
            id="phone"
            v-model="form.phone"
            type="tel"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            placeholder="01 23 45 67 89"
          />
        </div>
      </div>

      <div>
        <label for="address" class="block text-sm font-medium text-gray-700 mb-1">Adresse du siège</label>
        <textarea 
          id="address"
          v-model="form.address"
          rows="3"
          class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          placeholder="12 rue de l'Innovation, 75000 Paris"
        ></textarea>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label for="sector" class="block text-sm font-medium text-gray-700 mb-1">Secteur d'activité</label>
          <select 
            id="sector" 
            v-model="form.sector"
            class="w-full border border-gray-300 rounded px-3 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
          >
            <option value="" disabled>Sélectionner un secteur</option>
            <option value="tech">Technologie & Informatique</option>
            <option value="finance">Finance & Assurance</option>
            <option value="retail">Commerce & Distribution</option>
            <option value="health">Santé</option>
            <option value="other">Autre</option>
          </select>
        </div>
         <div>
          <label for="website" class="block text-sm font-medium text-gray-700 mb-1">Site Web</label>
          <input 
            id="website"
            v-model="form.website"
            type="url"
            class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
            placeholder="https://..."
          />
        </div>
      </div>

      <div class="pt-4">
        <button 
          type="submit" 
          :disabled="isLoading"
          class="w-full bg-blue-600 text-white font-bold py-3 px-4 rounded hover:bg-blue-700 transition duration-200 flex justify-center items-center disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="isLoading" class="mr-2">
            <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          </span>
          {{ isLoading ? 'Enregistrement en cours...' : 'Enregistrer l\'entreprise' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
// Si tu utilises axios : import axios from 'axios';

// --- 1. Gestion de l'état (Reactivity) ---
const form = reactive({
  name: '',
  siret: '',
  email: '',
  phone: '',
  address: '',
  sector: '',
  website: ''
});

const errors = reactive({});
const isLoading = ref(false);
const submitStatus = ref(null); // 'success', 'error', ou null

// --- 2. Logique de Validation ---
const validateForm = () => {
  // Reset des erreurs
  Object.keys(errors).forEach(key => delete errors[key]);
  let isValid = true;

  if (!form.name.trim()) {
    errors.name = "Le nom de l'entreprise est requis.";
    isValid = false;
  }

  if (!form.siret) {
    errors.siret = "Le numéro SIRET est requis.";
    isValid = false;
  } else if (form.siret.length !== 14) {
    errors.siret = "Le SIRET doit contenir exactement 14 chiffres.";
    isValid = false;
  }

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!form.email) {
    errors.email = "L'email est requis.";
    isValid = false;
  } else if (!emailRegex.test(form.email)) {
    errors.email = "Format d'email invalide.";
    isValid = false;
  }

  return isValid;
};

// Helper pour forcer uniquement les chiffres dans le SIRET
const filterNumbers = (event) => {
  const value = event.target.value;
  form.siret = value.replace(/[^0-9]/g, '');
};

// --- 3. Soumission du formulaire ---
const handleSubmit = async () => {
  submitStatus.value = null;
  
  if (!validateForm()) {
    return; // Stop si validation échoue
  }

  isLoading.value = true;

  try {
    // --- Simulation de l'appel API ---
    // Remplacer ceci par : await axios.post('/api/companies', form);
    
    await new Promise(resolve => setTimeout(resolve, 1500)); // Fake delay
    
    console.log("Données envoyées :", JSON.parse(JSON.stringify(form)));
    
    submitStatus.value = 'success';
    
    // Optionnel : Réinitialiser le formulaire après succès
    Object.keys(form).forEach(key => form[key] = '');
    
  } catch (error) {
    console.error("Erreur API :", error);
    submitStatus.value = 'error';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* Tu peux ajouter du CSS personnalisé ici si tu n'utilises pas Tailwind */
</style>