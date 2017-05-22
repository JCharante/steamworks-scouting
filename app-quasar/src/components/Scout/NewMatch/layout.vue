<template>
    <q-layout>
        <DrawerHead slot="header" title="Scout New Match" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></DrawerHead>
        <q-tabs slot="navigation">
            <q-tab icon="tune" route="/scout/new_match" exact replace>Pre Match</q-tab>
            <q-tab icon="android" route="/scout/new_match/auto" exact replace>Auto</q-tab>
            <q-tab icon="face" route="/scout/new_match/teleop" exact replace>Teleop</q-tab>
            <q-tab icon="gavel" route="/scout/new_match/after_match" exact replace>After Match</q-tab>
        </q-tabs>
        <DrawerBody ref="drawer"></DrawerBody>
        <router-view class="layout-view"></router-view>
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
        components: {
            'DrawerHead': DrawerHead,
            'DrawerBody': DrawerBody,
            'PreMatch': PreMatch,
            'Auto': Auto,
            'Teleop': Teleop,
            'AfterMatch': AfterMatch
        },
        data () {
            return {}
        }
    }
</script>

<style>
    img {
        margin-top: 100px;
        width: 100%;
    }
</style>
