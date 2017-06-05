<template>
    <q-list-item
        :item="{
            label: eventName,
            secondIcon: 'keyboard_arrow_right'
        }"
        link
        @click.native="$router.push(`/scout/view/event/${eventName}`)"
    ></q-list-item>
</template>

<script>
    export default {
        props: ['eventName'],
        data () {
            return {}
        }
    }
</script>
