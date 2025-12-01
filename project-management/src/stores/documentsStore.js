import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/_services/api";

export const useDocumentStore = defineStore('documents', ()=>{
    // state
    const customerDocuments = ref([]);
    const currentDocument = ref({});

    // Actions 

    async function fetchDocuments (){
        return
    }

    async function addCustomerDocuments(){

    }


    return{
        customerDocuments
    }
}) 