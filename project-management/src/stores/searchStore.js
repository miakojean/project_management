import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useSearchStore = defineStore('search', () => {
    const query = ref('');
    const results = ref([]);
    const lastUpdated = ref(null);

    function setSearch(q, res = []) {
        query.value = q || '';
        results.value = Array.isArray(res) ? res : [];
        lastUpdated.value = new Date();
    }

    function clearSearch() {
        query.value = '';
        results.value = [];
        lastUpdated.value = new Date();
    }

    return {
        query,
        results,
        lastUpdated,
        setSearch,
        clearSearch
    };
});
