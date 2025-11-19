<template>
    <button class="center__flex">
        {{ label }}
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 10.5v6m3-3H9m4.06-7.19-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z" />
        </svg>
    </button>
</template>

<script>
export default {

    props:{
        label:{
            type:String,
            default:"Nouveau dossier"
        }
    }

}
</script>

<style scoped>
button{
    padding: 0.5rem;
    border: none;
    border-radius: 0.3rem;
    color:#fff;
    font-size: 1rem;
    font-weight: 500;
    width: 100%;
    min-width: 200px;
    transition: all 0.3s ease-in-out;
    cursor: pointer;
    background: #00a2ff;
}

button:hover{
    background: #007bc2;
    transition: ease-in-out 0.2s;
}
</style>