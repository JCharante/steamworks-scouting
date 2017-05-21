<template>
    <q-drawer ref="drawer">
        <div class="toolbar light">
            <q-toolbar-title :padding="1">
                Steamworks Scouting
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
</template>

<script>
    export default {
        data () {
            return {}
        }
    }
</script>

<style>
</style>
