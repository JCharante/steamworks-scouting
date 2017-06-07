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
            <q-drawer-link icon="note_add" to="/scout/new">
                New Match
            </q-drawer-link>
            <q-drawer-link icon="view_list" to="/scout/view">
                View Matches
            </q-drawer-link>
            <q-drawer-link icon="poll" to="/">
                Overview
            </q-drawer-link>
            <q-drawer-link icon="cloud" to="/server" exact>
                Server
            </q-drawer-link>

            <hr>
            <div class="list-label">Miscellaneous</div>
            <q-drawer-link icon="settings" to="/settings">
                Settings
            </q-drawer-link>
            <q-drawer-link icon="volume_up" to="/soundboard">
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
