<template>
    <!--
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
    -->
    <q-toolbar>
        <q-btn flat @click="$emit('toggleLeft')">
            <q-icon name="menu"></q-icon>
        </q-btn>

        <q-toolbar-title>
            {{ title }}
            <div v-if="subtitle" slot="subtitle">{{ subtitle }}</div>
        </q-toolbar-title>
    </q-toolbar>
</template>

<script>
    import {
        dom,
        event,
        openURL,
        QLayout,
        QToolbar,
        QToolbarTitle,
        QBtn,
        QIcon,
        QList,
        QListHeader,
        QItem,
        QItemSide,
        QItemMain
    } from 'quasar'
    export default {
        components: {
            dom,
            event,
            openURL,
            QLayout,
            QToolbar,
            QToolbarTitle,
            QBtn,
            QIcon,
            QList,
            QListHeader,
            QItem,
            QItemSide,
            QItemMain
        },
        props: ['title', 'backUrl', 'subtitle'],
        data () {
            return {}
        }
    }
</script>

<style>
</style>
