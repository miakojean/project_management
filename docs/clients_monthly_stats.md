## Statistiques mensuelles des clients ✅

Endpoint backend:

- URL: `GET /manager/clients/stats/monthly/`
- Auth: **Authentification requise** (utilisez la session ou un token selon votre configuration DRF)
- Réponse JSON (200):

```json
{
  "success": true,
  "labels": ["2025-01","2025-02","2025-03"],
  "data": [1,3,1]
}
```

Notes d'intégration frontend:

- Un nouveau store a été ajouté: `src/stores/custumerStore.js`
  - action: `fetchCustomersMonthlyStats()`
  - getter: `getMonthlyStats` (retourne { labels, data })

- Un composant Vue est disponible: `src/components/charts/ClientsMonthlyChart.vue`
  - Utilise Chart.js pour afficher un graphique en barres
  - Se place par exemple dans le dashboard (`src/views/dashboarIndexView.vue` est déjà mis à jour)

Exemple rapide (avec session auth via navigateur):

1. Connectez-vous sur l'interface web (si vous utilisez l'auth par session)
2. Ouvrez le dashboard; le graphique se chargera automatiquement

Si vous utilisez un token (JWT), envoyez l'entête `Authorization: Bearer <token>` avec la requête.
