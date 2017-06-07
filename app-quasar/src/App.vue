<template>
  <!-- Don't drop "q-app" class -->
  <div id="q-app">
    <router-view></router-view>
  </div>
</template>

<script>
/*
 * Root component
 */

import './store.js'

export default {
    mounted () {
        console.log('%cachilles', 'font-family: cursive; font-size: 100px; background-color: #2b9eb3; color: white; border-style: solid;')
    }
}
</script>

<style></style>
