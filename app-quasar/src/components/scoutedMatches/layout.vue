<template>
    <q-layout>
        <DrawerHead slot="header" title="Scouted Matches" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></DrawerHead>
        <DrawerBody ref="drawer"></DrawerBody>
        <router-view class="layout-view"></router-view>
    </q-layout>
</template>

<script>
    import DrawerHead from '../DrawerHead.vue'
    import DrawerBody from '../DrawerBody.vue'
    import '../../store.js'

    export default {
        components: {
            'DrawerHead': DrawerHead,
            'DrawerBody': DrawerBody
        },
        data () {
            return {}
        }
    }
</script>
