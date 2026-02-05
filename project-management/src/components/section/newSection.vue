<template>
  <div class="min-h-screen flex items-center justify-center p-6">
    
    <div class="bg-white w-full max-w-6xl rounded-[40px] shadow-xl p-8 md:p-12 lg:p-16 flex flex-col lg:flex-row gap-12 lg:gap-20">
      
      <div class="lg:w-1/3 flex flex-col justify-between">
        <div>
          <h2 class="text-5xl font-black text-black leading-tight mb-6">
            Latest <br /> News
          </h2>
          <p class="text-gray-500 text-lg leading-relaxed mb-10 max-w-sm">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
          </p>
        </div>

        <a href="#" class="group relative inline-flex items-center w-fit mt-auto">
          <div class="absolute left-0 w-14 h-14 bg-gradient-to-tr from-orange-500 to-orange-200 rounded-full blur-sm opacity-80 transition-all duration-300 group-hover:w-full group-hover:opacity-100"></div>
          <span class="relative z-10 pl-6 pr-4 font-bold text-black group-hover:text-white transition-colors duration-300">
            View All News
          </span>
        </a>
      </div>

      <div class="lg:w-2/3 flex flex-col gap-4">
        
        <article 
          v-for="item in newsItems" 
          :key="item.id"
          class="group relative bg-gray-50 hover:bg-gray-100 rounded-2xl p-6 transition-all duration-300 cursor-pointer flex justify-between items-start gap-4"
        >
          <div>
            <div class="flex items-center gap-3 text-xs font-bold tracking-wider mb-2">
              <span class="text-orange-400 uppercase">{{ item.category }}</span>
              <span class="w-1 h-1 bg-gray-300 rounded-full"></span>
              <span class="text-gray-400 uppercase">{{ item.date }}</span>
            </div>
            <h3 class="text-lg font-bold text-gray-900 leading-snug group-hover:underline decoration-2 decoration-orange-400 underline-offset-4">
              {{ item.title }}
            </h3>
          </div>

          <div class="text-gray-300 group-hover:text-orange-500 transition-colors duration-300 flex-shrink-0">
            <svg 
              xmlns="http://www.w3.org/2000/svg" 
              fill="none" 
              viewBox="0 0 24 24" 
              stroke-width="2.5" 
              stroke="currentColor" 
              class="w-6 h-6 transform group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform duration-300"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25" />
            </svg>
          </div>
        </article>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

// Données fictives basées sur l'image
const newsItems = ref([
  {
    id: 1,
    category: 'CATEGORY',
    date: 'JUNE 2023',
    title: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.',
    link: '#'
  },
  {
    id: 2,
    category: 'CATEGORY',
    date: 'JUNE 2023',
    title: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.',
    link: '#'
  },
  {
    id: 3,
    category: 'CATEGORY',
    date: 'JUNE 2023',
    title: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.',
    link: '#'
  }
]);
</script>

<style scoped>
/* Pas besoin de CSS supplémentaire si Tailwind est configuré correctement */
</style>