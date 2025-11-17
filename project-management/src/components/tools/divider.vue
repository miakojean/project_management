<template>
<div class="section-divider">
    <div class="divider-title">
    <span class="line"></span>
    <span class="line"></span>
    </div>
</div>
</template>

<script>
export default{
name:"dividertool",

}
</script>

<style scoped>
.section-divider {
width: 100%;
margin: 0.5rem 0; /* Espace au-dessus et en-dessous du bloc entier */
}

.divider-title {
display: flex;
align-items: center;
text-align: center;
color: #b0b0b0; /* Couleur du texte discrète */
}

/* Les lignes de chaque côté du texte */
.line {
flex-grow: 1; /* Permet aux lignes de prendre toute la place disponible */
height: 1px;
background-color: #e0e0e0; /* Couleur de la ligne */
}

/* Le texte au milieu */
.text {
padding: 0 1rem; /* Espace entre le texte et les lignes */
font-size: 0.8rem;
font-weight: 600;
letter-spacing: 0.5px;
}

/* Le conteneur pour votre contenu */
.content {
margin-top: 0.5rem; /* Espace entre le séparateur et le contenu en-dessous */
}


</style>