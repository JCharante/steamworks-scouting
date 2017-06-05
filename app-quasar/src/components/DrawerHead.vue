<template>
    <div slot="header" class="toolbar">
        <button v-if="backUrl" class="hide-on-drawer-visible" @click="$router.push(backUrl)">
            <i>keyboard_arrow_left</i>
        </button>
        <button v-else class="hide-on-drawer-visible" @click="$emit('openDrawerBody')">
            <i>menu</i>
        </button>
        <q-toolbar-title :padding="1">
            {{ title }}
        </q-toolbar-title>
    </div>
</template>

<script>
    export default {
        props: ['title', 'backUrl'],
        data () {
            return {}
        }
    }
</script>

<style>
</style>
