<template>
    <q-layout>
        <FlexDrawer title="Scout New Match" :tabs="tabs"></FlexDrawer>
        <router-view class="layout-view"></router-view>
    </q-layout>
</template>

<script>
    import FlexDrawer from '../../FlexDrawer.vue'
    import PreMatch from './PreMatch.vue'
    import Auto from './Auto.vue'
    import Teleop from './Teleop.vue'
    import AfterMatch from './AfterMatch.vue'

    export default {
        components: {
            'FlexDrawer': FlexDrawer,
            'PreMatch': PreMatch,
            'Auto': Auto,
            'Teleop': Teleop,
            'AfterMatch': AfterMatch
        },
        data () {
            return {
                tabs: [
                    {
                        'text': 'Pre Match',
                        'route': '/scout/new_match',
                        'icon': 'info_outline'
                    },
                    {
                        'text': 'Auto',
                        'route': '/scout/new_match/auto',
                        'icon': 'android'
                    },
                    {
                        'text': 'Teleop',
                        'route': '/scout/new_match/teleop',
                        'icon': 'face'
                    },
                    {
                        'text': 'After Match',
                        'route': '/scout/new_match/after_match',
                        'icon': 'gavel'
                    }
                ]
            }
        }
    }
</script>

<style>
    img {
        margin-top: 100px;
        width: 100%;
    }
</style>
