<template>
  <div class="input__family center__flex_start">
    <label :for="identifiant">{{ label }}</label>
    <input 
      :type="type" 
      :id="identifiant" 
      :placeholder="placeholder"
      :value="modelValue"
      @input="handleInput"
      @blur="validateField"
      :class="{ 'error': hasError }"
    >
    <span v-if="hasError" class="error-message">
      {{ errorMessage }}
    </span>
  </div>
</template>

<script>
export default {
  props: {
    identifiant: {
      type: String,
      default: "Username"
    },
    label: {
      type: String,
      default: "Username"
    },
    placeholder: {
      type: String,
      default: "Entrer votre username"
    },
    modelValue: {
      type: String,
      default: ""
    },
    required: {
      type: Boolean,
      default: false
    },
    type: {
      type: String,
      default: "text"
    }
  },
  emits: ['update:modelValue'],
  data() {
    return {
      hasError: false,
      errorMessage: "Ce champ est obligatoire",
      isTouched: false
    }
  },
  methods: {
    handleInput(event) {
      const value = event.target.value;
      this.$emit('update:modelValue', value);
      
      // Validation en temps réel si le champ a déjà été touché
      if (this.isTouched) {
        this.validateField();
      }
    },
    
    validateField() {
      this.isTouched = true;
      
      if (this.required && !this.modelValue.trim()) {
        this.hasError = true;
        return false;
      } else {
        this.hasError = false;
        return true;
      }
    },
    
    // Méthode publique pour validation externe
    validate() {
      return this.validateField();
    },
    
    // Réinitialiser l'état d'erreur
    resetValidation() {
      this.hasError = false;
      this.isTouched = false;
    }
  },
  
  watch: {
    modelValue(newValue) {
      // Auto-validation quand la valeur change et que le champ a été touché
      if (this.isTouched) {
        this.validateField();
      }
    }
  }
}
</script>

<style scoped>
.input__family{
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: start;
    gap: 0.5rem;
}

label{
    font-size: 1rem;
    font-weight: 500;
    color: #535353;
}

input{
    padding: 0.8rem;
    width: 100%;
    max-width: 500px;
    font-size: 0.9rem;
    font-weight: 500;
    border-radius: 0.2rem;
    border: 1px solid #cacaca;
    outline: none;
    transition: border-color 0.3s ease;
}

input:placeholder-shown{
    font-weight: 400;
}

input:focus {
    border-color: #2563eb;
}

input.error {
    border-color: #dc2626;
    background-color: #fef2f2;
}

.error-message {
    color: #dc2626;
    font-size: 0.8rem;
    font-weight: 500;
    margin-top: 0.25rem;
}
</style>