<template>
  <div class="input__family center__flex_start">
    <label :for="identifiant">{{ label }}</label>
    <input type="text" :id="identifiant" :placeholder="placeholder">
  </div>
</template>

<script>
export default {

    props:{
        identifiant:{
            type:String,
            default: "Username"
        },
        label:{
            type:String,
            default: "Username"
        },
        placeholder:{
            type:String,
            default:"Entrer votre username"
        }
    }

}
</script>

<style scoped>

.input__family{
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: start;
    gap: 0.5rem;
}

label{
    font-size: 1rem;
    font-weight: 500;
    color: #535353;
}

input{
    padding: 0.9rem;
    width: 100%;
    max-width: 500px;
    font-size: 0.9rem;
    font-weight: 500;
    border-radius: 0.3rem;
    border: 1px solid #b6b6b6;
    outline: none;
}

</style>