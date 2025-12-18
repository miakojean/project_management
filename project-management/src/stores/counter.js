// stores/countdownStore.js
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useCountdownStore = defineStore('countdown', () => {
  // Store les comptes à rebours actifs
  const activeCountdowns = ref(new Map())
  
  // Liste des intervals en cours
  const intervals = ref(new Map())
  
  // Calculer le temps restant pour une date donnée
  const calculateTimeRemaining = (endDate) => {
    const now = new Date()
    const end = new Date(endDate)
    const total = end - now
    
    if (total <= 0) {
      return {
        total: 0,
        days: 0,
        hours: 0,
        minutes: 0,
        seconds: 0,
        expired: true,
        overdue: Math.ceil(Math.abs(total) / (1000 * 60 * 60 * 24))
      }
    }
    
    const seconds = Math.floor((total / 1000) % 60)
    const minutes = Math.floor((total / 1000 / 60) % 60)
    const hours = Math.floor((total / (1000 * 60 * 60)) % 24)
    const days = Math.floor(total / (1000 * 60 * 60 * 24))
    
    return {
      total,
      days,
      hours,
      minutes,
      seconds,
      expired: false,
      overdue: 0
    }
  }
  
  // Formater le temps restant pour l'affichage
  const formatCountdown = (timeRemaining) => {
    if (timeRemaining.expired) {
      return {
        text: `+${timeRemaining.overdue}j`,
        class: 'countdown-expired',
        tooltip: `Échéance dépassée depuis ${timeRemaining.overdue} jour(s)`,
        urgency: 'expired'
      }
    }
    
    const { days, hours, minutes, seconds } = timeRemaining
    
    // Déterminer l'urgence
    let urgency = 'normal'
    if (days === 0 && hours < 24) {
      urgency = hours < 12 ? 'urgent' : 'warning'
    } else if (days < 3) {
      urgency = 'warning'
    }
    
    // Format d'affichage
    let text = ''
    if (days > 0) {
      text = `${days} jour${days > 1 ? 's' : ''}`
    } else if (hours > 0) {
      text = `${hours}h ${minutes}m`
    } else if (minutes > 0) {
      text = `${minutes}m ${seconds}s`
    } else {
      text = `${seconds}s`
    }
    
    // Classes CSS
    const classMap = {
      'normal': 'countdown-normal',
      'warning': 'countdown-warning',
      'urgent': 'countdown-urgent',
      'expired': 'countdown-expired'
    }
    
    // Tooltip
    const tooltipMap = {
      'normal': `Échéance dans ${days} jour(s)`,
      'warning': `Échéance proche : ${days}j ${hours}h`,
      'urgent': `Échéance imminente : ${hours}h ${minutes}m`,
      'expired': `Dépassé de ${timeRemaining.overdue} jour(s)`
    }
    
    return {
      text,
      class: classMap[urgency],
      tooltip: tooltipMap[urgency],
      urgency,
      raw: timeRemaining
    }
  }
  
  // Démarrer un compte à rebours
  const startCountdown = (id, endDate, onUpdate = null) => {
    // Mettre à jour immédiatement
    updateCountdown(id, endDate, onUpdate)
    
    // Créer l'interval si pas déjà existant
    if (!intervals.value.has(id)) {
      const interval = setInterval(() => {
        updateCountdown(id, endDate, onUpdate)
      }, 1000)
      
      intervals.value.set(id, interval)
    }
    
    return getCountdown(id)
  }
  
  // Mettre à jour un compte à rebours
  const updateCountdown = (id, endDate, onUpdate = null) => {
    const timeRemaining = calculateTimeRemaining(endDate)
    const formatted = formatCountdown(timeRemaining)
    
    // Stocker dans le store
    activeCountdowns.value.set(id, {
      id,
      endDate,
      formatted,
      lastUpdate: new Date()
    })
    
    // Appeler le callback si fourni
    if (onUpdate && typeof onUpdate === 'function') {
      onUpdate(formatted)
    }
    
    return formatted
  }
  
  // Récupérer un compte à rebours
  const getCountdown = (id) => {
    return activeCountdowns.value.get(id)?.formatted || null
  }
  
  // Arrêter un compte à rebours
  const stopCountdown = (id) => {
    if (intervals.value.has(id)) {
      clearInterval(intervals.value.get(id))
      intervals.value.delete(id)
    }
    
    if (activeCountdowns.value.has(id)) {
      activeCountdowns.value.delete(id)
    }
  }
  
  // Arrêter tous les comptes à rebours
  const stopAllCountdowns = () => {
    intervals.value.forEach(interval => {
      clearInterval(interval)
    })
    intervals.value.clear()
    activeCountdowns.value.clear()
  }
  
  // Version simplifiée pour affichage statique
  const getStaticCountdown = (endDate) => {
    const timeRemaining = calculateTimeRemaining(endDate)
    return formatCountdown(timeRemaining)
  }
  
  // Calculer les jours restants seulement
  const getDaysRemaining = (endDate) => {
    const now = new Date()
    const end = new Date(endDate)
    const diffTime = end - now
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  }
  
  // Vérifier si une date est urgente
  const isDateUrgent = (endDate) => {
    const days = getDaysRemaining(endDate)
    return days <= 3 && days >= 0
  }
  
  // Nettoyer les anciens comptes à rebours
  const cleanupOldCountdowns = () => {
    const now = new Date()
    const oneDayAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000)
    
    for (const [id, data] of activeCountdowns.value.entries()) {
      if (data.lastUpdate < oneDayAgo) {
        stopCountdown(id)
      }
    }
  }
  
  return {
    // Données
    activeCountdowns: computed(() => Array.from(activeCountdowns.value.values())),
    
    // Méthodes principales
    startCountdown,
    stopCountdown,
    stopAllCountdowns,
    getCountdown,
    updateCountdown,
    
    // Méthodes utilitaires
    getStaticCountdown,
    getDaysRemaining,
    isDateUrgent,
    calculateTimeRemaining,
    formatCountdown,
    cleanupOldCountdowns
  }
})