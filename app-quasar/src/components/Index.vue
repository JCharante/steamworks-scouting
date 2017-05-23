<template>
    <q-layout>
        <DrawerHead slot="header" title="Home" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></DrawerHead>
        <DrawerBody ref="drawer"></DrawerBody>
        <div class="layout-view">
            <div class="layout-padding">
                <div class="row inline">
                    <div class="auto  ">
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
    import DrawerHead from './DrawerHead.vue'
    import DrawerBody from './DrawerBody.vue'

    export default {
        components: {
            'DrawerHead': DrawerHead,
            'DrawerBody': DrawerBody
        },
        data () {
            return {}
        }
    }
</script>
