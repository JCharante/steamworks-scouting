<template>
    <div class="layout-view">
        <div class="layout-padding">
            <div class="group">
                <button class="full-width primary keep-case" @click="placeholderLoading">Upload My Matches</button>
                <button class="full-width secondary keep-case" @click="placeholderLoading">Upload All Matches</button>
            </div>
        </div>
    </div>
</template>

<script>
    import { Loading } from 'quasar'

    export default {
        methods: {
            placeholderLoading () {
                Loading.show({
                    spinner: 'gears',
                    spinnerColor: 'yellow',
                    spinnerSize: 220,
                    message: 'Uploading... This may take a while... I\'m not frozen...',
                    messageColor: '#FFFFFF'
                })
                setTimeout(() => {
                    Loading.hide()
                }, 5000)
            }
        }
    }
</script>

<style>
    .keep-case {
        text-transform: none;
    }
</style>
