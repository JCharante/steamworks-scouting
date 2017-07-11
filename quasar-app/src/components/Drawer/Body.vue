<template>
    <div>
        <q-list no-border link inset-delimiter>
            <q-list-header>Steamworks Scouting</q-list-header>
            <q-side-link item to="/">
                <q-item-side icon="home" />
                <q-item-main label="Home"/>
            </q-side-link>

            <q-list-header>Scout</q-list-header>
            <q-side-link item to="/scout/new">
                <q-item-side icon="note_add" />
                <q-item-main label="New Match"/>
            </q-side-link>
            <q-side-link item to="/scout/view">
                <q-item-side icon="view_list" />
                <q-item-main label="View Matches"/>
            </q-side-link>
            <q-side-link item to="/">
                <q-item-side icon="poll" />
                <q-item-main label="Overview"/>
            </q-side-link>
            <q-side-link item to="/server">
                <q-item-side icon="cloud" />
                <q-item-main label="Server"/>
            </q-side-link>

            <q-list-header>Miscellaneous</q-list-header>
            <q-side-link item to="/settings">
                <q-item-side icon="settings" />
                <q-item-main label="Settings"/>
            </q-side-link>
            <q-side-link item to="/soundboard">
                <q-item-side icon="volume_up" />
                <q-item-main label="Soundboard"/>
            </q-side-link>
        </q-list>
    </div>
</template>

<script>
    import {
        dom,
        event,
        openURL,
        QLayout,
        QToolbar,
        QToolbarTitle,
        QBtn,
        QIcon,
        QList,
        QListHeader,
        QItem,
        QItemSide,
        QItemMain,
        QSideLink
    } from 'quasar'
    export default {
        components: {
            dom,
            event,
            openURL,
            QLayout,
            QToolbar,
            QToolbarTitle,
            QBtn,
            QIcon,
            QList,
            QListHeader,
            QItem,
            QItemSide,
            QItemMain,
            QSideLink
        },
        data () {
            return {}
        }
    }
</script>

<style>
</style>
