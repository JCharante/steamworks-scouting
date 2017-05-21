<template>
    <q-layout>
        <DrawerHead slot="header" title="Tabby Demo" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></DrawerHead>
        <Tabby :tabs="tabs" slot="navigation"></Tabby>
        <DrawerBody ref="drawer"></DrawerBody>
        <router-view class="layout-view"></router-view>
    </q-layout>
</template>

<script>
    import DrawerHead from '../DrawerHead.vue'
    import DrawerBody from '../DrawerBody.vue'
    import Tabby from './Tabby.vue'

    export default {
        components: {
            'DrawerHead': DrawerHead,
            'DrawerBody': DrawerBody,
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
