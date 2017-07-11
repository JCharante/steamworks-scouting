<template>
    <q-layout ref="layout">
        <drawer-head slot="header" title="Home" @toggleLeft="$refs.layout.toggleLeft()"></drawer-head>
        <drawer-body slot="left"></drawer-body>
        <div class="layout-view">
            <div class="layout-padding">
                <h4 class="text-center">Steamworks Scouting</h4>
                <p class="text-center">by the Innocuous Achilles group</p>
            </div>
        </div>

    </q-layout>
</template>

<script>
    import {
        dom,
        event,
        openURL,
        QLayout,
        QField,
        QInput,
        QToolbar,
        QToolbarTitle,
        QBtn,
        QIcon,
        QList,
        QListHeader,
        QItem,
        QItemSide,
        QItemMain,
        QKnob
    } from 'quasar'
    import DrawerHead from './Drawer/Head.vue'
    import DrawerBody from './Drawer/Body.vue'

    export default {
        components: {
            dom,
            event,
            openURL,
            QLayout,
            QField,
            QInput,
            QToolbar,
            QToolbarTitle,
            QBtn,
            QIcon,
            QList,
            QListHeader,
            QItem,
            QItemSide,
            QItemMain,
            QKnob,
            DrawerHead,
            DrawerBody
        },
        data () {
            return {}
        }
    }
</script>
