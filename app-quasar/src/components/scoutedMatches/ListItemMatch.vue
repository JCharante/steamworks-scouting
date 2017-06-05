<template>
    <q-list-item
        :item="{
            label: 'Q' + matchNumber,
            secondIcon: 'keyboard_arrow_right'
        }"
        link
        @click.native="$router.push(`/scout/view/event/${eventName}/match/${matchNumber}`)"
    ></q-list-item>
</template>

<script>
    export default {
        props: ['eventName', 'matchNumber'],
        data () {
            return {}
        }
    }
</script>
