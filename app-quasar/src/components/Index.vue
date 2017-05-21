<template>
    <q-layout>
        <div>
            <div class="layout-padding">
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

        <FlexDrawer title="Scout New Match"></FlexDrawer>

        <router-view class="layout-view"></router-view>

    </q-layout>
</template>

<script>
    import FlexDrawer from './FlexDrawer.vue'

    export default {
        components: {
            'FlexDrawer': FlexDrawer
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
