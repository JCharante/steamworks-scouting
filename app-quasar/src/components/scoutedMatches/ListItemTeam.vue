<template>
    <div class="item">
        <div class="item-content has-secondary">
            <div>Team: {{ match.teamNumber }}</div>
        </div>
        <div class="item-secondary">
            <i slot="target">
                more_vert
                <q-popover ref="popover">
                    <div class="list">
                        <div class="item item-link" @click="$router.push(`/scout/edit/${match.matchID}`)">
                            <div class="item-content">Edit</div>
                        </div>
                        <div class="item item-link" @click="deleteMatch">
                            <div class="item-content">Delete</div>
                        </div>
                    </div>
                </q-popover>
            </i>
        </div>
    </div>
</template>

<script>
    import store from '../../store.js'
    import * as matchActions from '../../actions/matches.js'
    import { Dialog, Toast } from 'quasar'

    export default {
        props: ['matchID'],
        methods: {
            deleteMatch () {
                let self = this
                self.$refs.popover.close()
                Dialog.create({
                    title: 'Confirm',
                    message: `Are you sure you want to delete ${self.match.eventName} >> Q${self.match.matchNumber} >> ${self.match.teamNumber} ?`,
                    buttons: [
                        {
                            label: 'Nevermind',
                            handler () {
                                Toast.create('😎 I knew you couldn\'t give me up..')
                            }
                        },
                        {
                            label: 'Delete',
                            handler () {
                                Toast.create('💔 but I was your biggest fan')
                                store.dispatch(matchActions.deleteMatch(self.matchID))
                                self.$emit('updateList')
                            }
                        }
                    ]
                })
            }
        },
        data () {
            return {
                match: matchActions.fetchMatch(this.$select('matches'), this.matchID)
            }
        }
    }
</script>
