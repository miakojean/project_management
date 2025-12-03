<template>
    <div class="input__family">
      <label :for="label">{{ label }}</label>
      <select 
        :id="label"
        v-model="inputValue"
        @change="updateValue"
        :class="{ 'error': error }"
      >
        <option value="" disabled>-- Sélectionner --</option>
        <option 
          v-for="(item, index) in options" 
          :key="index" 
          :value="item.value"
        >
          {{ item.label }}
        </option>
      </select>
      <span v-if="error" class="error-message">{{ error }}</span>
    </div>
  </template>
    
  <script>
    import { ref, watch } from 'vue';
    
    export default {
      props: {
        label: {
          type: String,
          default: "Type de dossier"
        },
        options: {
          type: Array,
          default: () => []
        },
        modelValue: {
          type: String,
          default: ''
        },
        error: {
          type: String,
          default: ''
        }
      },
      emits: ['update:modelValue'],
      setup(props, { emit }) {
        const inputValue = ref(props.modelValue);
    
        // Met à jour la valeur parente quand inputValue change
        const updateValue = () => {
          emit('update:modelValue', inputValue.value);
        };
    
        // Synchronise inputValue si modelValue change depuis le parent
        watch(() => props.modelValue, (newVal) => {
          inputValue.value = newVal;
        });
    
        return {
          inputValue,
          updateValue
        };
      }
    }
</script>
    
  <style scoped>
  .input__family {
    display: flex;
    flex-direction: column;
    justify-content: start;
    gap: 0.5rem;
    width: 100%;
    max-width: 600px;
  }

  label {
    font-size: 1rem;
    font-weight: 500;
    color: #535353;
  }

  select {
    padding: 0.9rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 0.9rem;
    width: 100%;
    box-sizing: border-box;
    transition: ease-in-out 0.3s;
    outline: none;
  }

  select:focus {
    border-color: #2563eb;
  }

  select.error {
    border-color: #dc2626;
    background-color: #fef2f2;
  }

  option {
    font-size: 0.9rem;
  }

  .error-message {
    color: #dc2626;
    font-size: 0.8rem;
    font-weight: 500;
    margin-top: 0.25rem;
  }
</style>