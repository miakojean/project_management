<template>
    <nav>
        <h4>DocSira</h4>
    </nav>
</template>

<script>
export default {

}
</script>

<style scoped>
nav{
    position: fixed;
    top: 10px;
    width: 100%;
    display: flex;
    justify-content: left;
    padding: 1rem;
}

nav h4{
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--primary-color);
}

@media(min-width: 1024px){

    nav{
        display: none;
    }
}
</style>