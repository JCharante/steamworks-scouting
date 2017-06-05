<template>
    <q-layout>
        <DrawerHead slot="header" title="Home" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></DrawerHead>
        <DrawerBody ref="drawer"></DrawerBody>
        <div class="layout-view">
            <div class="layout-padding">
                <h4 class="text-center">Steamworks Scouting</h4>
                <p class="text-center">by the Innocuous Achilles group</p>
            </div>
        </div>

    </q-layout>
</template>

<script>
    import DrawerHead from './DrawerHead.vue'
    import DrawerBody from './DrawerBody.vue'

    export default {
        components: { DrawerHead, DrawerBody },
        data () {
            return {}
        }
    }
</script>
