<template>
    <q-list-item
        :item="{
            label: eventName,
            secondIcon: 'keyboard_arrow_right'
        }"
        link
        @click.native="$router.push(`/scout/view/event/${eventCode}`)"
    ></q-list-item>
</template>

<script>
    import { eventNames } from '../../statics/js/events.js'

    export default {
        props: ['eventCode'],
        computed: {
            eventName () {
                return eventNames[this.eventCode] || this.eventCode
            }
        },
        data () {
            return {}
        }
    }
</script>
