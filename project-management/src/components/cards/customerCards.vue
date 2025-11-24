<template>
    <div class="card">
        <div class="card__header">
            <span class="label">Entreprise</span>
        </div>

        <div class="card__body">
            <!-- Tu pourras ajouter ici le contenu de la carte -->
            <h4>ADN consulting</h4>
            <p class="placeholder-text">
                Informations de lentité juridique (raison sociale, SIREN, adresse, etc.)
            </p>

            <div class="affairs__details">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 12.75V12A2.25 2.25 0 0 1 4.5 9.75h15A2.25 2.25 0 0 1 21.75 12v.75m-8.69-6.44-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
                </svg>
                <p>9</p>
            </div>
        </div>

        <div class="card__footer">
            <button class="btn-primary">Ouvrir</button>
        </div>
    </div>
</template>

<script>
export default {
  name: 'LegalEntityCard'
}
</script>

<style scoped>
.card {
  width: 380px;
  height: 340px;
  background: #ffffff;
  border-radius: 1.2rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.12);
}

.card__header {
  padding: 1.25rem 1.5rem 0;
  text-align: left;
}

.label {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #e6f6fe 0%, #c3e7fd 100%);
  color: #0b79d0;
  font-size: 0.875rem;
  font-weight: 600;
  border-radius: 2rem;
  letter-spacing: 0.5px;
  box-shadow: 0 2px 8px rgba(11, 121, 208, 0.15);
}

.card__body {
  flex: 1;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.card__body h4 {
    font-size: 1.5rem;
    font-weight: 600;
}

.affairs__details{
    width: 100%;
    display:flex;
    justify-content:start;
    align-items: center;
    gap: 1rem;
    font-size:1.2rem;
    color:#64748b;
}

.placeholder-text {
  color: #64748b;
  font-size: 0.95rem;
  line-height: 1.6;
  margin: 0;
}

/* Footer avec boutons */
.card__footer {
  padding: 1rem 1.5rem;
  display: flex;
  gap: 0.75rem;
  justify-content: flex-end;
  border-top: 1px solid #f1f5f9;
  background: #fafafa;
}

.btn-outline,
.btn-primary {
  padding: 0.55rem 1.2rem;
  border-radius: 0.6rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-outline {
  background: transparent;
  border: 2px solid #cbd5e1;
  color: #475569;
}

.btn-outline:hover {
  background: #f8fafc;
  border-color: #94a3b8;
}

.btn-primary {
  background: linear-gradient(135deg, #0b79d0 0%, #085fa8 100%);
  border: none;
  color: white;
  box-shadow: 0 4px 12px rgba(11, 121, 208, 0.3);
}

.btn-primary:hover {
  background: linear-gradient(135deg, #086bb8 0%, #074e8c 100%);
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(11, 121, 208, 0.4);
}

/* Responsive */
@media (max-width: 480px) {
  .card {
    width: 100%;
    max-width: 360px;
  }
}
</style>