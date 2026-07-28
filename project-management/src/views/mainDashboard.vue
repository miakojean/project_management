<template>
    <div class="main-layout">

        <h3>Que faisons-nous aujourd'hui?</h3>

        <div class="w-full flex justify-center items-center gap-4">
            <add-button label="Nouveau"/>
        </div>
    </div>
</template>

<script>
import addButton from '../components/button/addButton.vue'
import inputfamily from '../components/input/inputfamily.vue'
export default {

    components:{
        addButton,
        inputfamily
    }

}
</script>

<style>

</style>