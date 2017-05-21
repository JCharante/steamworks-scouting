<template>
    <q-tabs v-if="(tabs !== undefined && tabs !== null) && tabs.length > 0">
        <q-tab v-for="tab in tabs" :key="tab.route" :icon="tab.icon" :route="tab.route" exact replace>{{ tab.text }}</q-tab>
    </q-tabs>
</template>

<script>
    export default {
        props: ['tabs'],
        data () {
            return {}
        }
    }
</script>
