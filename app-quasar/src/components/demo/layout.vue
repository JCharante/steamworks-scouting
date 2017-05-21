<template>
    <q-layout>
        <FlexDrawerHeader slot="header" title="Tabby Demo" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></FlexDrawerHeader>
        <Tabby :tabs="tabs" slot="navigation"></Tabby>
        <FlexDrawerDrawer ref="drawer"></FlexDrawerDrawer>
        <router-view class="layout-view"></router-view>
    </q-layout>
</template>

<script>
    import FlexDrawerHeader from '../DrawerHead.vue'
    import FlexDrawerDrawer from '../DrawerBody.vue'
    import Tabby from './Tabby.vue'

    export default {
        components: {
            'FlexDrawerHeader': FlexDrawerHeader,
            'FlexDrawerDrawer': FlexDrawerDrawer,
            'Tabby': Tabby
        },
        data () {
            return {
                tabs: [
                    {
                        'text': 'Pre Match',
                        'route': '/demo',
                        'icon': 'info_outline'
                    },
                    {
                        'text': 'Auto',
                        'route': '/demo/tabtwo',
                        'icon': 'android'
                    }
                ]
            }
        }
    }
</script>
