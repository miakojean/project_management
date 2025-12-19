<template>
<!-- From Uiverse.io by satyamchaudharydev --> 

  <div class="loader"></div>
</template>

<script>
export default {

}
</script>

<style scoped>
/* From Uiverse.io by satyamchaudharydev */ 
.loader {
  display: block;
  --height-of-loader: 4px;
  --loader-color: #1edb70;
  width: 130px;
  height: var(--height-of-loader);
  border-radius: 30px;
  background-color: rgba(0,0,0,0.2);
  position: relative;
}

.loader::before {
  content: "";
  position: absolute;
  background: var(--loader-color);
  top: 0;
  left: 0;
  width: 0%;
  height: 100%;
  border-radius: 30px;
  animation: moving 1s ease-in-out infinite;
  ;
}

@keyframes moving {
  50% {
    width: 100%;
  }

  100% {
    width: 0;
    right: 0;
    left: unset;
  }
}
</style>