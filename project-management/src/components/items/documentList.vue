<template>
    <div class=" flex items-start flex-col gap-6">
        <h4>Liste des documents</h4>

        <ul class="center__flex_start">
            <li>
                <div class="icons center__flex">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                    </svg>
                </div>
                <div class="informations center__flex_start">
                    <h4>
                        Cahier de charges du logiciel de gestion de documents
                    </h4>
                    <p>
                        Lorem ipsum, dolor sit amet consectetur adipisicing elit. 
                        Architecto commodi corrupti ullam laudantium alias debitis 
                        deleniti aliquid dolorum enim exercitationem.
                    </p>
                    <span class="flex gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                        </svg>
                        10H58
                    </span>
                </div>
            </li>

            <li>
                <div class="icons center__flex">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                    </svg>
                </div>
                <div class="informations center__flex_start">
                    <h4>
                        Cahier de charges du logiciel de gestion de documents
                    </h4>
                    <p>
                        Lorem ipsum, dolor sit amet consectetur adipisicing elit. 
                        Architecto commodi corrupti ullam laudantium alias debitis 
                        deleniti aliquid dolorum enim exercitationem.
                    </p>
                    <span class="flex gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                        </svg>
                        10H58
                    </span>
                </div>
            </li>

            <li>
                <div class="icons center__flex">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
                    </svg>
                </div>
                <div class="informations center__flex_start">
                    <h4>
                        Cahier de charges du logiciel de gestion de documents
                    </h4>
                    <p>
                        Lorem ipsum, dolor sit amet consectetur adipisicing elit. 
                        Architecto commodi corrupti ullam laudantium alias debitis 
                        deleniti aliquid dolorum enim exercitationem.
                    </p>
                    <span class="flex gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z" />
                        </svg>
                        10H58
                    </span>
                </div>
            </li>
        </ul>
    </div>
</template>

<script>
export default {

}
</script>

<style scoped>
li{
    display: flex;
    align-items: normal;
    justify-content: start;
    gap: 1rem;
}

.icons{
    padding: 1rem;
    background: rgb(255, 183, 183);
    height: 60px;
    border-radius: 1rem;
}

.informations{
  display: flex;
  flex-direction: column;
  justify-content: start;
  gap: 0.5rem;
}

.informations h4{
    font-size: 1.2rem;
    font-weight: 500;
}

.informations p{
    font-size: 0.9rem;
    font-weight: 400;
    color: #9b9b9b;
}

.informations span{
    font-size: 1rem;
    font-weight: 500;
    color: var(--primary-color);
}
</style>