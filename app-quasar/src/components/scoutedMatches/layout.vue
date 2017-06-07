<template>
    <q-layout>
        <router-view class="layout-view"></router-view>
    </q-layout>
</template>

<script>
    import DrawerHead from '../DrawerHead.vue'
    import DrawerBody from '../DrawerBody.vue'
    import { writeStoresToDisk } from '../../store.js'

    export default {
        components: { DrawerHead, DrawerBody },
        beforeDestroy () {
            writeStoresToDisk()
        },
        data () {
            return {}
        }
    }
</script>
