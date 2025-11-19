<template>
    <input type="search" placeholder="Trouver un dossier">
</template>

<script>
export default {

    props:{
        placeholder:{
            type:String,
            default:"Trouver un dossier"
        }
    }

}
</script>

<style scoped>
input{
    outline:none;
}
input:focus{
    outline: none;
}
</style>