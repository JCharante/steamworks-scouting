<template>
    <q-layout>
        <DrawerHead slot="header" title="Scout New Match" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></DrawerHead>
        <q-tabs slot="navigation">
            <q-tab icon="tune" :route="'/scout/' + matchID" exact replace>Pre Match</q-tab>
            <q-tab icon="android" :route="'/scout/' + matchID + '/auto'" exact replace>Auto</q-tab>
            <q-tab icon="face" :route="'/scout/' + matchID + '/teleop'" exact replace>Teleop</q-tab>
            <q-tab icon="gavel" :route="'/scout/' + matchID + '/after_match'" exact replace>After Match</q-tab>
        </q-tabs>
        <DrawerBody ref="drawer"></DrawerBody>
        <router-view ref="cur" class="layout-view"></router-view>
    </q-layout>
</template>

<script>
    import DrawerHead from '../../DrawerHead.vue'
    import DrawerBody from '../../DrawerBody.vue'
    import PreMatch from './PreMatch.vue'
    import Auto from './Auto.vue'
    import Teleop from './Teleop.vue'
    import AfterMatch from './AfterMatch.vue'

    export default {
        mounted () {
            let self = this
            self.matchID = self.$route.params.matchID
            // console.log('layout: Mounted with route prop matchID =', self.matchID)
        },
        components: {
            'DrawerHead': DrawerHead,
            'DrawerBody': DrawerBody,
            'PreMatch': PreMatch,
            'Auto': Auto,
            'Teleop': Teleop,
            'AfterMatch': AfterMatch
        },
        data () {
            return {
                matchID: null
            }
        }
    }
</script>
