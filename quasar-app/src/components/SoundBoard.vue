<template>
    <q-layout ref="layout">
        <drawer-head slot="header" title="Home" @toggleLeft="$refs.layout.toggleLeft()"></drawer-head>
        <drawer-body slot="left"></drawer-body>
        <div class="layout-view">
            <div class="layout-padding">

                <div class="group">
                    <q-btn class="full-width" color="secondary" @click="playSound('charge-1.wav')" no-caps>Charge</q-btn>
                    <q-btn class="full-width" color="warning" @click="playSound('three-bells.wav')" no-caps>Tele Op Start</q-btn>
                    <q-btn class="full-width" color="negative" @click="playSound('fog-blast.wav')" no-caps>Carson Anthem</q-btn>
                    <q-btn class="full-width" color="info" @click="playSound('buzzer.wav')" no-caps>Match End</q-btn>
                </div>

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
        methods: {
            playSound: function (soundFile) {
                let audio = new Audio(`../statics/external/media/${soundFile}`)
                audio.play()
                return null
            }
        },
        data () {
            return {}
        }
    }
</script>
