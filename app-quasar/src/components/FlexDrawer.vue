<template>
    <q-layout>
        <div slot="header" class="toolbar">
            <button class="hide-on-drawer-visible" @click="$refs.drawer.open()">
                <i>menu</i>
            </button>
            <q-toolbar-title :padding="1">
                {{ title }}
            </q-toolbar-title>
        </div>

        <q-tabs v-if="tabs != null && tabs.length > 0" slot="navigation">
            <q-tab v-for="tab in tabs" :key="tab.route" :icon="tab.icon" :route="tab.route" exact replace>{{ tab.text }}</q-tab>
        </q-tabs>

        <q-drawer ref="drawer">
            <div class="toolbar light">
                <q-toolbar-title :padding="1">
                    Drawer
                </q-toolbar-title>
            </div>

            <div class="list no-border platform-delimiter">
                <q-drawer-link icon="home" to="/" exact>
                    Home
                </q-drawer-link>

                <hr>
                <div class="list-label">Scout</div>
                <q-drawer-link icon="note_add" to="/scout/new_match">
                    New Match
                </q-drawer-link>
                <q-drawer-link icon="view_list" to="/">
                    View Matches
                </q-drawer-link>
                <q-drawer-link icon="poll" to="/">
                    Overview
                </q-drawer-link>
                <q-drawer-link icon="cloud" to="/">
                    Server
                </q-drawer-link>

                <hr>
                <div class="list-label">Miscellaneous</div>
                <q-drawer-link icon="settings" to="/">
                    Settings
                </q-drawer-link>
                <q-drawer-link icon="volume_up" to="/">
                    Soundboard
                </q-drawer-link>
            </div>
        </q-drawer>

    </q-layout>
</template>

<script>
    export default {
        props: ['title', 'tabs'],
        data () {
            return {}
        }
    }
</script>

<style>
</style>
