<template>
    <div class="layout-view">
        <div class="layout-padding">
            <div class="group">
                <q-btn color="primary" class="full-width" @click="placeholderLoading" no-caps>Download</q-btn>
            </div>
        </div>
    </div>
</template>

<script>
    import {
        QBtn,
        Loading,
        QSpinnerGears
    } from 'quasar'

    export default {
        components: {
            QBtn,
            QSpinnerGears
        },
        methods: {
            placeholderLoading () {
                Loading.show({
                    spinner: QSpinnerGears,
                    spinnerColor: 'yellow',
                    spinnerSize: 220,
                    message: 'Downloading... This may take a while... I\'m not frozen...',
                    messageColor: 'white'
                })
                setTimeout(() => {
                    Loading.hide()
                }, 5000)
            }
        }
    }
</script>
