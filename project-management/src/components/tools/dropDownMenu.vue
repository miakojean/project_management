<!-- DropdownMenu.vue -->
<template>
    <div class="dropdown-container" v-click-outside="closeDropdown">
        <slot name="trigger" :toggle="toggleDropdown" :is-open="isOpen">
            <button class="dropdown-trigger" @click="toggleDropdown" aria-label="Menu déroulant">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="icon">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 12.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5ZM12 18.75a.75.75 0 1 1 0-1.5.75.75 0 0 1 0 1.5Z" />
                </svg>
            </button>
        </slot>
        
        <div v-if="isOpen" class="dropdown-menu" :style="menuStyle" :class="menuClass">
            <slot name="content">
                <ul class="dropdown-list">
                    <li 
                        v-for="(item, index) in items" 
                        :key="index" 
                        class="dropdown-item"
                        :class="{'dropdown-item-danger': item.danger}"
                        @click="handleItemClick(item)"
                    >
                        <component v-if="item.icon" :is="item.icon" class="dropdown-icon" />
                        <span>{{ item.label }}</span>
                    </li>
                </ul>
            </slot>
        </div>
    </div>
</template>

<script>
export default {
    name: 'DropdownMenu',
    
    props: {
        items: {
            type: Array,
            default: () => []
        },
        placement: {
            type: String,
            default: 'bottom-right',
            validator: (value) => ['bottom-right', 'bottom-left', 'top-right', 'top-left'].includes(value)
        },
        closeOnClick: {
            type: Boolean,
            default: true
        }
    },
    
    data() {
        return {
            isOpen: false
        };
    },
    
    computed: {
        menuStyle() {
            const styles = {};
            if (this.placement.includes('right')) {
                styles.right = '0';
            }
            if (this.placement.includes('left')) {
                styles.left = '0';
            }
            if (this.placement.includes('top')) {
                styles.bottom = '100%';
                styles.marginTop = '0';
                styles.marginBottom = '0.25rem';
            }
            if (this.placement.includes('bottom')) {
                styles.top = '100%';
                styles.marginTop = '0.25rem';
            }
            return styles;
        },
        
        menuClass() {
            return `dropdown-${this.placement}`;
        }
    },
    
    methods: {
        toggleDropdown() {
            this.isOpen = !this.isOpen;
            if (this.isOpen) {
                this.$emit('open');
            }
        },
        
        closeDropdown() {
            this.isOpen = false;
            this.$emit('close');
        },
        
        handleItemClick(item) {
            if (item.action) {
                this.$emit('item-click', item);
            }
            if (this.closeOnClick) {
                this.closeDropdown();
            }
        }
    },
    
    directives: {
        'click-outside': {
            bind(el, binding, vnode) {
                el.clickOutsideEvent = function(event) {
                    if (!(el === event.target || el.contains(event.target))) {
                        vnode.context[binding.expression](event);
                    }
                };
                document.body.addEventListener('click', el.clickOutsideEvent);
            },
            unbind(el) {
                document.body.removeEventListener('click', el.clickOutsideEvent);
            }
        }
    }
}
</script>

<style scoped>
.dropdown-container {
    position: relative;
    display: inline-block;
}

.dropdown-trigger {
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.2s;
    color: #718096;
}

.dropdown-trigger:hover {
    background-color: #edf2f7;
    color: #4299e1;
}

.dropdown-trigger .icon {
    width: 1.5rem;
    height: 1.5rem;
}

.dropdown-menu {
    position: absolute;
    z-index: 1000;
    min-width: 200px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    border: 1px solid #e2e8f0;
    animation: dropdownFade 0.2s ease;
}

@keyframes dropdownFade {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.dropdown-list {
    list-style: none;
    padding: 0.5rem 0;
    margin: 0;
}

.dropdown-item {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    cursor: pointer;
    transition: background-color 0.2s;
    font-size: 0.875rem;
    color: #4a5568;
    gap: 0.75rem;
}

.dropdown-item:hover {
    background-color: #f7fafc;
}

.dropdown-icon {
    width: 1.25rem;
    height: 1.25rem;
    flex-shrink: 0;
}

.dropdown-divider {
    height: 1px;
    background: #e2e8f0;
    margin: 0.5rem 0;
}

.dropdown-item-danger {
    color: #e53e3e;
}

.dropdown-item-danger:hover {
    background-color: #fed7d7;
}

/* Responsive */
@media (max-width: 480px) {
    .dropdown-menu {
        position: fixed;
        right: 1rem;
        left: 1rem;
        bottom: 1rem;
        max-height: 60vh;
        overflow-y: auto;
    }
}
</style>