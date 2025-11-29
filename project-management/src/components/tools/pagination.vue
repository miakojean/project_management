<template>
    <div class="pagination-container">
        <div class="pagination-info">
            Affichage de {{ startIndex + 1 }} à {{ endIndex }} sur {{ totalItems }} éléments
        </div>
        
        <div class="pagination-controls">
            <button 
                class="pagination-btn pagination-prev"
                @click="prevPage"
                :disabled="currentPage === 1"
            >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
                </svg>
                Précédent
            </button>
            
            <div class="pagination-pages">
                <button
                    v-for="page in visiblePages"
                    :key="page"
                    class="pagination-page"
                    :class="{ 'active': page === currentPage }"
                    @click="goToPage(page)"
                >
                    {{ page }}
                </button>
                
                <span v-if="showEllipsis" class="pagination-ellipsis">...</span>
            </div>
            
            <button 
                class="pagination-btn pagination-next"
                @click="nextPage"
                :disabled="currentPage === totalPages"
            >
                Suivant
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="m8.25 4.5 7.5 7.5-7.5 7.5" />
                </svg>
            </button>
        </div>
        
        <div class="pagination-size" v-if="showPageSize">
            <label for="pageSize">Éléments par page :</label>
            <select 
                id="pageSize"
                v-model="localPageSize" 
                @change="onPageSizeChange"
                class="page-size-select"
            >
                <option value="6">6</option>
                <option value="12">12</option>
                <option value="24">24</option>
                <option value="48">48</option>
            </select>
        </div>
    </div>
</template>

<script>
import { ref, computed, watch } from 'vue';

export default {
    name: 'PaginationComponent',
    props: {
        totalItems: {
            type: Number,
            required: true,
            default: 0
        },
        currentPage: {
            type: Number,
            required: true,
            default: 1
        },
        pageSize: {
            type: Number,
            required: true,
            default: 6
        },
        showPageSize: {
            type: Boolean,
            default: true
        },
        maxVisiblePages: {
            type: Number,
            default: 5
        }
    },
    emits: ['page-change', 'page-size-change'],
    setup(props, { emit }) {
        const localPageSize = ref(props.pageSize);

        // Computed properties
        const totalPages = computed(() => Math.ceil(props.totalItems / localPageSize.value));
        
        const startIndex = computed(() => (props.currentPage - 1) * localPageSize.value);
        
        const endIndex = computed(() => {
            const end = startIndex.value + localPageSize.value;
            return end > props.totalItems ? props.totalItems : end;
        });
        
        const visiblePages = computed(() => {
            const pages = [];
            let start = Math.max(1, props.currentPage - Math.floor(props.maxVisiblePages / 2));
            let end = Math.min(totalPages.value, start + props.maxVisiblePages - 1);
            
            if (end - start + 1 < props.maxVisiblePages) {
                start = Math.max(1, end - props.maxVisiblePages + 1);
            }
            
            for (let i = start; i <= end; i++) {
                pages.push(i);
            }
            
            return pages;
        });
        
        const showEllipsis = computed(() => {
            return totalPages.value > visiblePages.value.length && 
                   visiblePages.value[visiblePages.value.length - 1] < totalPages.value;
        });

        // Methods
        const goToPage = (page) => {
            if (page >= 1 && page <= totalPages.value) {
                emit('page-change', page);
                scrollToTop();
            }
        };
        
        const nextPage = () => {
            if (props.currentPage < totalPages.value) {
                emit('page-change', props.currentPage + 1);
                scrollToTop();
            }
        };
        
        const prevPage = () => {
            if (props.currentPage > 1) {
                emit('page-change', props.currentPage - 1);
                scrollToTop();
            }
        };
        
        const onPageSizeChange = () => {
            emit('page-size-change', parseInt(localPageSize.value));
            // Retour à la première page quand on change la taille
            emit('page-change', 1);
        };
        
        const scrollToTop = () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        };

        // Watcher pour synchroniser la pageSize externe
        watch(
            () => props.pageSize,
            (newSize) => {
                localPageSize.value = newSize;
            }
        );

        return {
            localPageSize,
            totalPages,
            startIndex,
            endIndex,
            visiblePages,
            showEllipsis,
            goToPage,
            nextPage,
            prevPage,
            onPageSizeChange
        };
    }
}
</script>

<style scoped>
.pagination-container {
    margin-top: 2rem;
    padding: 1.5rem;
    background: #f8fafc;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

.pagination-info {
    color: #64748b;
    font-size: 0.875rem;
    font-weight: 500;
}

.pagination-controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.pagination-btn {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    border: 1px solid #d1d5db;
    background: white;
    color: #374151;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}

.pagination-btn:hover:not(:disabled) {
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
}

.pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.pagination-btn svg {
    width: 1rem;
    height: 1rem;
}

.pagination-pages {
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.pagination-page {
    min-width: 2.5rem;
    height: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #d1d5db;
    background: white;
    color: #374151;
    border-radius: 8px;
    font-size: 0.875rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
}

.pagination-page:hover {
    background: #f1f5f9;
    border-color: #3b82f6;
}

.pagination-page.active {
    background: #3b82f6;
    color: white;
    border-color: #3b82f6;
}

.pagination-ellipsis {
    padding: 0 0.5rem;
    color: #64748b;
    font-weight: 500;
}

.pagination-size {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.pagination-size label {
    color: #64748b;
    font-size: 0.875rem;
    font-weight: 500;
}

.page-size-select {
    padding: 0.5rem;
    border: 1px solid #d1d5db;
    border-radius: 6px;
    background: white;
    color: #374151;
    font-size: 0.875rem;
    cursor: pointer;
}

/* Responsive Design */
@media (max-width: 768px) {
    .pagination-container {
        flex-direction: column;
        align-items: stretch;
        text-align: center;
    }
    
    .pagination-controls {
        justify-content: center;
    }
    
    .pagination-pages {
        flex-wrap: wrap;
        justify-content: center;
    }
}
</style>