<template>
  <div class="new-section">
    <div class="section-header">
      <div class="left__side">
        <div class="section-label">Dernières nouvelles</div>
        <h2 class="section-title">Restez aux courants des dernières actualités</h2>
        <p class="section-description">
          Discover the latest trends, insights, and updates from our team. 
          We're constantly exploring new ideas to share with our community.
        </p>
      </div>
      <div class="header-decoration">
        <div class="decoration-dot"></div>
        <div class="decoration-line"></div>
      </div>
    </div>
    
    <div class="news-grid">
      <div 
        v-for="news in newsItems" 
        :key="news.id" 
        class="news-card"
        :class="{'featured': news.featured}"
        @click="handleNewsClick(news)"
      >
        <div class="card-badge" :style="{backgroundColor: getCategoryColor(news.category)}">
          {{ news.category }}
        </div>
        
        <div class="card-content">
          <div class="card-date">
            <svg class="calendar-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 4H5C3.89543 4 3 4.89543 3 6V20C3 21.1046 3.89543 22 5 22H19C20.1046 22 21 21.1046 21 20V6C21 4.89543 20.1046 4 19 4Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M16 2V6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M8 2V6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M3 10H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            {{ news.date }}
          </div>
          
          <h3 class="card-title">{{ news.title }}</h3>
          
          <p class="card-excerpt">
            {{ news.excerpt || 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna.' }}
          </p>
          
          <div class="card-footer">
            <div class="read-time">
              <svg class="clock-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M12 6V12L16 14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              {{ news.readTime || '3 min read' }}
            </div>
            
            <button class="read-more-btn" aria-label="Read more about this article">
              Read More
              <svg class="arrow-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 5L19 12L12 19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import mainButton from '../button/mainButton.vue';

// Données enrichies avec plus de variété
const newsItems = ref([
  {
    id: 1,
    category: 'Technology',
    date: 'June 15, 2023',
    title: 'The Future of AI in Everyday Applications',
    excerpt: 'Exploring how artificial intelligence is transforming daily life and business operations across multiple industries.',
    readTime: '4 min read',
    featured: true,
    link: '#'
  },
  {
    id: 2,
    category: 'Design',
    date: 'June 10, 2023',
    title: 'Minimalist UI Trends for 2023',
    excerpt: 'A look at the rising popularity of minimalist design and how it improves user experience and accessibility.',
    readTime: '5 min read',
    featured: false,
    link: '#'
  },
  {
    id: 3,
    category: 'Business',
    date: 'June 5, 2023',
    title: 'Remote Work Culture in the Post-Pandemic Era',
    excerpt: 'How companies are adapting their culture and operations to support hybrid and fully remote teams effectively.',
    readTime: '6 min read',
    featured: false,
    link: '#'
  },
  {
    id: 4,
    category: 'Innovation',
    date: 'May 28, 2023',
    title: 'Sustainable Tech Solutions for Modern Cities',
    excerpt: 'Examining innovative technologies that are helping urban areas become more sustainable and environmentally friendly.',
    readTime: '7 min read',
    featured: false,
    link: '#'
  }
]);

// Fonction pour gérer les clics sur les cartes
const handleNewsClick = (news) => {
  // console.log('News clicked:', news.title);
  // Navigation vers la page de détail de l'article
  // window.location.href = news.link;
};

// Fonction pour obtenir une couleur selon la catégorie
const getCategoryColor = (category) => {
  const colorMap = {
    'Technology': '#3B82F6',
    'Design': '#8B5CF6',
    'Business': '#10B981',
    'Innovation': '#F59E0B'
  };
  
  return colorMap[category] || '#6B7280';
};
</script>

<style scoped>
.new-section {
  display: flex;
  flex-direction: column;
  gap: 3rem;
  padding: 2rem 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  position: relative;
}

.left__side {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 500px;
}

.section-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #3B82F6;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  line-height: 1.2;
  color: #1F2937;
  margin: 0;
}

.section-description {
  font-size: 1.125rem;
  line-height: 1.6;
  color: #6B7280;
  margin: 0;
}

.header-decoration {
  display: none;
}

.news-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

.news-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid #E5E7EB;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}

.news-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: #3B82F6;
}

.news-card.featured {
  border-left: 4px solid #3B82F6;
}

.card-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 0.5rem;
}

.card-date {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #6B7280;
}

.calendar-icon {
  color: #9CA3AF;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.4;
  color: #1F2937;
  margin: 0;
}

.card-excerpt {
  font-size: 1rem;
  line-height: 1.6;
  color: #4B5563;
  margin: 0;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
}

.read-time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #6B7280;
}

.clock-icon {
  color: #9CA3AF;
}

.read-more-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: none;
  border: none;
  font-weight: 600;
  color: #3B82F6;
  cursor: pointer;
  padding: 0.5rem 0;
  transition: gap 0.2s ease;
}

.read-more-btn:hover {
  gap: 0.75rem;
}

.arrow-icon {
  transition: transform 0.2s ease;
}

.read-more-btn:hover .arrow-icon {
  transform: translateX(3px);
}

.section-footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  padding: 2rem;
  background-color: #F9FAFB;
  border-radius: 12px;
  text-align: center;
}

.newsletter-cta {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1F2937;
  margin: 0;
}

.cta-button {
  align-self: flex-start;
}

/* Responsive Design */
@media (min-width: 768px) {
  .new-section {
    padding: 3rem 2rem;
    gap: 4rem;
  }
  
  .header-decoration {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    margin-top: 3rem;
  }
  
  .decoration-dot {
    width: 8px;
    height: 8px;
    background-color: #3B82F6;
    border-radius: 50%;
  }
  
  .decoration-line {
    width: 2px;
    height: 60px;
    background: linear-gradient(to bottom, #3B82F6, transparent);
  }
  
  .news-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .news-card.featured {
    grid-column: span 2;
  }
}

@media (min-width: 1024px) {
  .new-section {
    padding: 4rem;
  }
  
  .section-title {
    font-size: 3rem;
  }
  
  .news-grid {
    grid-template-columns: repeat(3, 1fr);
  }
  
  .news-card.featured {
    grid-column: span 1;
    grid-row: span 2;
  }
}
</style>