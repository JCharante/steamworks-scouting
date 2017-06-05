<template>
    <q-layout>
        <router-view class="layout-view"></router-view>
    </q-layout>
</template>

<script>
    import DrawerHead from '../DrawerHead.vue'
    import DrawerBody from '../DrawerBody.vue'
    import * as matchActions from '../../actions/matches.js'
    import '../../store.js'

    export default {
        components: { DrawerHead, DrawerBody },
        beforeDestroy () {
            let self = this
            matchActions.saveStoreToLocalStorage(self.$select('matches'))
        },
        data () {
            return {}
        }
    }
</script>
