<template>
    <div slot="header" class="toolbar">
        <button class="hide-on-drawer-visible" @click="$emit('openDrawerBody')">
            <i>menu</i>
        </button>
        <q-toolbar-title :padding="1">
            {{ title }}
        </q-toolbar-title>
    </div>
</template>

<script>
    export default {
        props: ['title'],
        data () {
            return {}
        }
    }
</script>

<style>
</style>
