<template>
    <q-list-item
        :item="{
            label: 'Q' + matchNumber,
            secondIcon: 'keyboard_arrow_right'
        }"
        link
        @click.native="$router.push(`/scout/view/event/${eventCode}/match/${matchNumber}`)"
    ></q-list-item>
</template>

<script>
    export default {
        props: ['eventCode', 'matchNumber'],
        data () {
            return {}
        }
    }
</script>
