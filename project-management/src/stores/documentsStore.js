import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/_services/api";

export const useDocumentStore = defineStore('documents', ()=>{
    // state
    const customerDocuments = ref([]);
    const currentDocument = ref({});

    // Fonction utilitaire pour sauvegarder le fichier
    function saveFile(blob, filename) {
        return new Promise((resolve, reject) => {
            try {
                // Créer un lien de téléchargement
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement('a');
                
                link.href = url;
                link.download = filename;
                link.style.display = 'none';
                
                // Ajouter au DOM et cliquer
                document.body.appendChild(link);
                link.click();
                
                // Nettoyer
                setTimeout(() => {
                    document.body.removeChild(link);
                    window.URL.revokeObjectURL(url);
                    resolve();
                }, 100);
            } catch (error) {
                reject(error);
            }
        });
    }

    // Actions 
    async function downloadDocuments(documentIds, options = {}, fileName) {
        try {
            const config = {
                method: 'GET',
                responseType: 'blob', // Important pour les fichiers binaires
                headers: {
                    'Accept': '*/*', 
                    ...options.headers
                }
            };

            let response;
            let filename = fileName;

            // Si c'est un seul document, utiliser GET
            if (typeof documentIds === 'number' || (Array.isArray(documentIds) && documentIds.length === 1)) {
                const documentId = Array.isArray(documentIds) ? documentIds[0] : documentIds;
                
                // Téléchargement simple avec GET
                response = await api.get(`/manager/documents/${documentId}/download/`, config);
                
                // Extraire le nom de fichier de l'en-tête Content-Disposition
                const contentDisposition = response.headers['content-disposition'];
                if (contentDisposition) {
                    const filenameMatch = contentDisposition.match(/filename="?(.+?)"?$/);
                    if (filenameMatch) filename = filenameMatch[1];
                }
            }
            // Si plusieurs documents, utiliser POST pour les options
            else if (Array.isArray(documentIds) && documentIds.length > 1) {
                const payload = {
                    document_ids: documentIds,
                    format: options.format || 'zip',
                    compress_level: options.compressLevel || 6,
                    inclure_metadata: options.includeMetadata || false
                };

                response = await api.post('/manager/documents/download-multiple/', payload, {
                    ...config,
                    method: 'POST'
                });

                filename = options.filename || `documents_${new Date().toISOString().slice(0,10)}.zip`;
            }

            // Créer et télécharger le fichier
            await saveFile(response.data, filename);
            
            return {
                success: true,
                filename,
                size: response.data.size,
                status: response.status
            };

        } catch (error) {
            console.error('Erreur lors du téléchargement:', error);
            
            // Gestion des erreurs spécifiques
            if (error.response) {
                switch (error.response.status) {
                    case 401:
                        throw new Error('Non authentifié. Veuillez vous reconnecter.');
                    case 403:
                        throw new Error('Vous n\'avez pas la permission de télécharger ce document.');
                    case 404:
                        throw new Error('Document non trouvé.');
                    case 410:
                        throw new Error('Le document n\'est plus disponible.');
                    default:
                        throw new Error(`Erreur serveur: ${error.response.status}`);
                }
            } else if (error.request) {
                throw new Error('Pas de réponse du serveur. Vérifiez votre connexion.');
            } else {
                throw new Error('Erreur de configuration: ' + error.message);
            }
        }
    }

    async function addCustomerDocuments(){
        // Votre logique ici
    }

    return{
        customerDocuments,
        downloadDocuments,
    }
})