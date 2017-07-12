<template>
    <q-layout ref="layout">
        <drawer-head slot="header" title="Server" @toggleLeft="$refs.layout.toggleLeft()"></drawer-head>
        <q-tabs slot="navigation">
            <q-route-tab slot="title" class="keep-case" icon="cloud_upload" to="/server" exact replace label="Upload" />
            <q-route-tab slot="title" class="keep-case" icon="cloud_download" to="/server/download" exact replace label="Download" />
        </q-tabs>
        <drawer-body slot="left"></drawer-body>
        <router-view class="layout-view"></router-view>
    </q-layout>
</template>

<script>
    import {
        dom,
        event,
        openURL,
        QLayout,
        QField,
        QInput,
        QToolbar,
        QToolbarTitle,
        QBtn,
        QIcon,
        QList,
        QListHeader,
        QRouteTab,
        QTab,
        QTabs,
        QKnob
    } from 'quasar'
    import DrawerHead from '../Drawer/Head.vue'
    import DrawerBody from '../Drawer/Body.vue'
    import Upload from './Upload.vue'
    import Download from './Download.vue'

    export default {
        components: {
            dom,
            event,
            openURL,
            QLayout,
            QField,
            QInput,
            QToolbar,
            QToolbarTitle,
            QBtn,
            QIcon,
            QList,
            QListHeader,
            QRouteTab,
            QKnob,
            QTab,
            QTabs,
            DrawerHead,
            DrawerBody,
            Upload,
            Download
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
