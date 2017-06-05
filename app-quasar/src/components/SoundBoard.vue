<template>
    <q-layout>
        <DrawerHead slot="header" title="Soundboard" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></DrawerHead>
        <DrawerBody ref="drawer"></DrawerBody>
        <div class="layout-view">
            <div class="layout-padding">

                <div class="group">
                    <button class="full-width secondary" @click="playSound('charge-1.wav')">Charge</button>
                    <button class="full-width warning" @click="playSound('three-bells.wav')">Tele Op Start</button>
                    <button class="full-width negative" @click="playSound('fog-blast.wav')">Carson Anthem</button>
                    <button class="full-width info" @click="playSound('buzzer.wav')">Match End</button>
                </div>

            </div>
        </div>

    </q-layout>
</template>

<script>
    import DrawerHead from './DrawerHead.vue'
    import DrawerBody from './DrawerBody.vue'

    export default {
        components: { DrawerHead, DrawerBody },
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
