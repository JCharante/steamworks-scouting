<template>
    <q-layout>
        <FlexDrawerHeader slot="header" title="Scout New Match" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></FlexDrawerHeader>
        <q-tabs slot="navigation">
            <q-tab icon="info_outline" route="/scout/new_match" exact replace>Pre Match</q-tab>
            <q-tab icon="android" route="/scout/new_match/auto" exact replace>Auto</q-tab>
            <q-tab icon="face" route="/scout/new_match/teleop" exact replace>Teleop</q-tab>
            <q-tab icon="gavel" route="/scout/new_match/after_match" exact replace>After Match</q-tab>
        </q-tabs>
        <FlexDrawerDrawer ref="drawer"></FlexDrawerDrawer>
        <router-view class="layout-view"></router-view>
    </q-layout>
</template>

<script>
    import FlexDrawerHeader from '../../DrawerHead.vue'
    import FlexDrawerDrawer from '../../DrawerBody.vue'
    import PreMatch from './PreMatch.vue'
    import Auto from './Auto.vue'
    import Teleop from './Teleop.vue'
    import AfterMatch from './AfterMatch.vue'

    export default {
        components: {
            'FlexDrawerHeader': FlexDrawerHeader,
            'FlexDrawerDrawer': FlexDrawerDrawer,
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
