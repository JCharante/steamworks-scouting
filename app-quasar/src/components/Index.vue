<template>
    <q-layout>
        <FlexDrawerHeader slot="header" title="Home" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></FlexDrawerHeader>
        <FlexDrawerDrawer ref="drawer"></FlexDrawerDrawer>
        <div class="layout-view">
            <div class="layout-padding">
                <p>Hi</p>
                <div class="row inline">
                    <div class="auto">
                        <a href="#">
                            <img src="../assets/achilles-1024.png" alt="achilles Logo">
                        </a>
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

<style>
    img {
        margin-top: 100px;
        width: 100%;
    }
</style>
