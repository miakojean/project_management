# 🚀 Guide de Migration JavaScript → TypeScript pour Vue.js

## Table des matières

1. [Prérequis](#1-prérequis)
2. [Installation des dépendances](#2-installation-des-dépendances)
3. [Configuration TypeScript](#3-configuration-typescript)
4. [Configuration Vite / Vue CLI](#4-configuration-vite--vue-cli)
5. [Migration des fichiers](#5-migration-des-fichiers)
6. [Migration des composants Vue](#6-migration-des-composants-vue)
7. [Migration du store Pinia / Vuex](#7-migration-du-store-pinia--vuex)
8. [Migration du routeur Vue Router](#8-migration-du-routeur-vue-router)
9. [Migration des appels API](#9-migration-des-appels-api)
10. [Erreurs fréquentes et solutions](#10-erreurs-fréquentes-et-solutions)
11. [Checklist de migration](#11-checklist-de-migration)

---

## 1. Prérequis

- Node.js >= 16
- Vue 3.x (la migration TS est nettement plus simple avec Vue 3)
- Vite ou Vue CLI v5+

> ⚠️ Si vous êtes encore sur **Vue 2**, envisagez d'abord la migration vers Vue 3 avant d'introduire TypeScript.

---

## 2. Installation des dépendances

```bash
# TypeScript core
npm install -D typescript

# Support TypeScript pour Vue
npm install -D vue-tsc

# Types pour les libs courantes
npm install -D @types/node
```

Si vous utilisez **Vue CLI** :

```bash
npm install -D @vue/cli-plugin-typescript
```

Si vous utilisez **Vite** (recommandé) :

```bash
npm install -D @vitejs/plugin-vue
# Vite supporte TypeScript nativement, aucun plugin supplémentaire requis
```

---

## 3. Configuration TypeScript

### Créer `tsconfig.json` à la racine du projet

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "jsx": "preserve",
    "lib": ["ESNext", "DOM"],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },
    "skipLibCheck": true,
    "noEmit": true,
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true
  },
  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"],
  "exclude": ["node_modules", "dist"]
}
```

### Créer `env.d.ts` dans `src/`

```typescript
/// <reference types="vite/client" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}
```

---

## 4. Configuration Vite / Vue CLI

### Avec Vite (`vite.config.ts`)

Renommer `vite.config.js` → `vite.config.ts` :

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
```

### Mettre à jour `package.json`

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vue-tsc && vite build",
    "preview": "vite preview",
    "type-check": "vue-tsc --noEmit"
  }
}
```

---

## 5. Migration des fichiers

### Stratégie recommandée : migration progressive

Ne migrez **pas** tout d'un coup. Procédez fichier par fichier :

```
src/
├── main.js          → main.ts
├── App.vue          (ajouter lang="ts")
├── router/
│   └── index.js     → index.ts
├── stores/
│   └── counter.js   → counter.ts
└── components/
    └── MyComponent.vue  (ajouter lang="ts")
```

### Renommer les fichiers

```bash
# Linux / macOS
find src -name "*.js" ! -name "*.config.js" -exec bash -c 'mv "$0" "${0%.js}.ts"' {} \;

# Ou manuellement un par un (recommandé pour contrôler chaque migration)
mv src/main.js src/main.ts
mv src/router/index.js src/router/index.ts
mv src/stores/counter.js src/stores/counter.ts
```

---

## 6. Migration des composants Vue

### Avant (JavaScript)

```vue
<script>
export default {
  name: 'UserCard',
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      isLoading: false,
    }
  },
  methods: {
    greet() {
      console.log(`Bonjour ${this.user.name}`)
    },
  },
}
</script>
```

### Après (TypeScript avec `<script setup>`)

```vue
<script setup lang="ts">
interface User {
  id: number
  name: string
  email: string
}

const props = defineProps<{
  user: User
}>()

const isLoading = ref<boolean>(false)

function greet(): void {
  console.log(`Bonjour ${props.user.name}`)
}
</script>
```

### Cas avec valeurs par défaut (`withDefaults`)

```vue
<script setup lang="ts">
interface Props {
  title: string
  count?: number
  active?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  count: 0,
  active: false,
})
</script>
```

### Typer les `emit`

```vue
<script setup lang="ts">
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'close'): void
}>()
</script>
```

### Typer les `ref` et `computed`

```typescript
import { ref, computed } from 'vue'

const count = ref<number>(0)
const message = ref<string>('')
const items = ref<string[]>([])

const doubleCount = computed<number>(() => count.value * 2)
```

---

## 7. Migration du store Pinia / Vuex

### Pinia (recommandé) — Avant (JS)

```javascript
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    name: '',
    age: 0,
  }),
  actions: {
    setName(name) {
      this.name = name
    },
  },
})
```

### Pinia — Après (TS)

```typescript
import { defineStore } from 'pinia'

interface UserState {
  name: string
  age: number
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    name: '',
    age: 0,
  }),
  actions: {
    setName(name: string): void {
      this.name = name
    },
  },
  getters: {
    isAdult: (state): boolean => state.age >= 18,
  },
})
```

### Vuex — Avant (JS)

```javascript
export default {
  state: { count: 0 },
  mutations: {
    increment(state) { state.count++ }
  }
}
```

### Vuex — Après (TS)

```typescript
import { MutationTree, ActionTree, GetterTree } from 'vuex'

interface State {
  count: number
}

const state = (): State => ({ count: 0 })

const mutations: MutationTree<State> = {
  increment(state: State): void {
    state.count++
  },
}

export default { state, mutations }
```

---

## 8. Migration du routeur Vue Router

### Avant (JS)

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'

const routes = [
  { path: '/', component: Home },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
```

### Après (TS)

```typescript
import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import Home from '@/views/Home.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('@/views/About.vue'), // lazy loading
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
```

---

## 9. Migration des appels API

### Avant (JS)

```javascript
async function fetchUser(id) {
  const response = await fetch(`/api/users/${id}`)
  const data = await response.json()
  return data
}
```

### Après (TS)

```typescript
interface User {
  id: number
  name: string
  email: string
  role: 'admin' | 'user' | 'guest'
}

interface ApiResponse<T> {
  data: T
  message: string
  success: boolean
}

async function fetchUser(id: number): Promise<User> {
  const response = await fetch(`/api/users/${id}`)

  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`)
  }

  const result: ApiResponse<User> = await response.json()
  return result.data
}
```

### Centraliser les types dans `src/types/`

```
src/
└── types/
    ├── index.ts       ← re-export tout
    ├── user.ts
    ├── api.ts
    └── router.ts
```

```typescript
// src/types/user.ts
export interface User {
  id: number
  name: string
  email: string
}

// src/types/index.ts
export * from './user'
export * from './api'
```

---

## 10. Erreurs fréquentes et solutions

### ❌ `Property 'x' does not exist on type '{}'`

```typescript
// ❌ Mauvais
const obj = {}
obj.name = 'Alice' // Erreur

// ✅ Bon
const obj: { name: string } = { name: '' }
obj.name = 'Alice'
```

### ❌ `Object is possibly 'null' or 'undefined'`

```typescript
// ❌ Mauvais
const el = document.getElementById('app')
el.innerHTML = 'Hello' // Erreur : el peut être null

// ✅ Bon — optional chaining
el?.innerHTML = 'Hello' // ← ne fonctionne pas sur les assignations

// ✅ Bon — assertion non-null (si vous êtes sûr)
const el = document.getElementById('app')!
el.innerHTML = 'Hello'

// ✅ Bon — guard
if (el) el.innerHTML = 'Hello'
```

### ❌ `Type 'string | undefined' is not assignable to type 'string'`

```typescript
// ❌ Mauvais
const name: string = user?.name // peut être undefined

// ✅ Bon
const name: string = user?.name ?? 'Inconnu'
```

### ❌ Import de `.vue` non reconnu

Assurez-vous que `env.d.ts` contient :

```typescript
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}
```

### ❌ Alias `@/` non résolu

Vérifiez dans `tsconfig.json` :

```json
"paths": {
  "@/*": ["./src/*"]
}
```

Et dans `vite.config.ts` :

```typescript
resolve: {
  alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) }
}
```

---

## 11. Checklist de migration

### Setup initial

- [ ] Installer `typescript` et `vue-tsc`
- [ ] Créer `tsconfig.json`
- [ ] Créer `src/env.d.ts`
- [ ] Mettre à jour `vite.config.js` → `vite.config.ts`
- [ ] Mettre à jour les scripts dans `package.json`

### Migration des fichiers

- [ ] `main.js` → `main.ts`
- [ ] `router/index.js` → `router/index.ts`
- [ ] Fichiers de store (Pinia/Vuex)
- [ ] Services / utilitaires
- [ ] Composants Vue (ajout de `lang="ts"`)

### Bonnes pratiques

- [ ] Créer un dossier `src/types/` pour centraliser les interfaces
- [ ] Activer `strict: true` dans `tsconfig.json`
- [ ] Remplacer `Options API` par `<script setup lang="ts">` (progressivement)
- [ ] Typer toutes les props, emits, refs et computed
- [ ] Typer les réponses API avec des interfaces génériques
- [ ] Lancer `npm run type-check` régulièrement

### Validation finale

- [ ] `npm run type-check` → 0 erreur
- [ ] `npm run build` → build réussi
- [ ] Tests unitaires qui passent (si applicable)

---

## Ressources utiles

- [Documentation officielle Vue 3 + TypeScript](https://vuejs.org/guide/typescript/overview.html)
- [Documentation Vite](https://vitejs.dev/guide/features#typescript)
- [Documentation Pinia + TypeScript](https://pinia.vuejs.org/core-concepts/#typing-store-s-state)
- [Vue Router + TypeScript](https://router.vuejs.org/guide/advanced/typed-routes.html)
- [TypeScript Playground](https://www.typescriptlang.org/play)

---

> 💡 **Conseil** : Activez TypeScript en mode non-strict (`"strict": false`) au début si votre projet est grand, puis activez-le progressivement une fois tous les fichiers migrés.
