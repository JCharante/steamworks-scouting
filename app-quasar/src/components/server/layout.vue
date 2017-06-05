<template>
    <q-layout>
        <DrawerHead slot="header" title="Server" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></DrawerHead>
        <q-tabs slot="navigation">
            <q-tab class="keep-case" icon="cloud_upload" :route="'/server'" exact replace>Upload</q-tab>
            <q-tab class="keep-case" icon="cloud_download" :route="'/server/download'" exact replace>Download</q-tab>
        </q-tabs>
        <DrawerBody ref="drawer"></DrawerBody>
        <router-view class="layout-view"></router-view>
    </q-layout>
</template>

<script>
    import DrawerHead from '../DrawerHead.vue'
    import DrawerBody from '../DrawerBody.vue'
    import Upload from './Upload.vue'
    import Download from './Download.vue'

    export default {
        components: {
            'DrawerHead': DrawerHead,
            'DrawerBody': DrawerBody,
            'Upload': Upload,
            'Download': Download
        },
        data () {
            return {}
        }
    }
</script>

<style>
    .keep-case {
        text-transform: none;
    }
</style>
