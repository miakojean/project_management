<template>
    <div class="input__family">
      <label :for="label">{{ label }}</label>
      <select 
        :id="label"
        v-model="inputValue"
        @change="updateValue"
      >
        <option 
          v-for="(item, index) in options" 
          :key="index" 
          :value="item.matching"
        >
          {{ item.value }}
        </option>
      </select>
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
          default: () => [
            {value:'Constitution', matching:'FD'}, 
            {value:'Modification', matching:'DR'}, 
            {value: 'Dissolution', matching:"CT"},
            {value: 'Contentieux', matching: 'AUT'},
            {value: 'Conseil', matching: 'AUT'},
            {value:'Contrat', matching:'FD'}, 
            {value:'Audit', matching:'DR'}, 
            {value: 'Propriété intellectuelle', matching:"CT"},
            {value: 'Fusion acquisition', matching: 'AUT'},
            {value: 'Recouvrement', matching: 'AUT'}
          ]
        },
        modelValue: {
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
    max-width: 400px;
  }

select{
    padding: 0.9rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 0.9rem;
    width: 100%;
    box-sizing: border-box;
    transition: ease-in-out 0.3s;
    outline: none;
}

option{
    font-size: 0.9rem;
}
</style>