<template>
    <q-layout>
        <DrawerHead slot="header" title="Scout New Match" @openDrawerBody="$refs.drawer.$refs.drawer.open()"></DrawerHead>
        <DrawerBody ref="drawer"></DrawerBody>

        <div class="layout-view">
            <div class="layout-padding">
                <p>Creating New Match</p>
            </div>
        </div>
    </q-layout>
</template>

<script>
    import DrawerHead from '../DrawerHead.vue'
    import DrawerBody from '../DrawerBody.vue'
    import store from '../../store.js'
    import * as matchActions from '../../actions/matches.js'
    import * as util from '../../util.js'

    export default {
        mounted () {
            let self = this
            self.matchID = util.generateUUID4()
            store.dispatch(matchActions.createMatch(self.matchID))
            console.info('%cnew: %cCreated Match %O: %O', 'color: blue', 'color: black', self.matchID, matchActions.fetchMatch(self.$select('matches'), self.matchID))
            console.info('%cnew: %cRedirecting to scout page', 'color: blue', 'color: black')
            self.$router.push('/scout/edit/' + self.matchID)
        },
        components: {
            'DrawerHead': DrawerHead,
            'DrawerBody': DrawerBody
        },
        data () {
            return {
                matchID: null
            }
        }
    }
</script>
