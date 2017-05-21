<template>
    <q-layout>
        <FlexDrawerHeader slot="header" title="Home" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></FlexDrawerHeader>
        <FlexDrawerDrawer ref="drawer"></FlexDrawerDrawer>
        <div class="layout-view">
            <div class="layout-padding">
                <div class="row inline">
                    <div class="auto">
                        <router-link to="/scout/new_match">
                            <img src="../assets/achilles-1024.png" class="responsive">
                        </router-link>
                    </div>
                </div>
                <p class="text-center">Logo by Wil W.L.</p>
            </div>
        </div>

    </q-layout>
</template>

<script>
    import FlexDrawerHeader from './DrawerHead.vue'
    import FlexDrawerDrawer from './DrawerBody.vue'

    export default {
        components: {
            'FlexDrawerHeader': FlexDrawerHeader,
            'FlexDrawerDrawer': FlexDrawerDrawer
        },
        data () {
            return {}
        }
    }
</script>
