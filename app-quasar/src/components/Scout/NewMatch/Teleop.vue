<template>
    <div>
        <div class="layout-padding">
            <div class="list">
                <div class="list-label">Teleop Info</div>

                <div class="item two-lines">
                    <div class="item-content">
                        <span class="item-label">Total kPa: </span>
                        <q-numeric v-model="match.totalkPa" :min="0"></q-numeric>
                    </div>
                </div>

                <div class="item two-lines">
                    <div class="item-content">
                        <span class="item-label">Total Dumped Hoppers: </span>
                        <q-numeric v-model="match.totalHoppers" :min="0"></q-numeric>
                    </div>
                </div>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.tCollectedFromHopper"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Collected from Hopper
                    </div>
                </label>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.collectedFuelOffGround"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Collected Fuel from Floor
                    </div>
                </label>

                <div class="item two-lines">
                    <div class="item-content">
                        <span class="item-label">Total Gears: </span>
                        <q-numeric v-model="match.totalGears" :min="0"></q-numeric>
                    </div>
                </div>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.obtainedGearFromHumanPlayer"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Obtained Gear from Human Player
                    </div>
                </label>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.obtainedGearFromFloor"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Obtained Gear from Floor
                    </div>
                </label>

                <div class="item two-lines">
                    <div class="item-content row items-center">
                        <label style="margin-right: 10px;">High Goal Position:</label>
                        <br>
                        <q-select class="full-width" type="checkbox" v-model="match.tHighGoalShotFrom" :options="selectOptions.tHighGoalShotFrom"></q-select>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
    import store from '../../../store.js'
    import * as matchActions from '../../../actions/matches.js'

    export default {
        mounted () {
            let self = this
            console.info('%cTeleop: %cMounted with router prop matchID = %O', 'color: blue', 'color: black', self.$route.params.matchID)
            let fetchedMatch = matchActions.fetchMatch(self.$select('matches'), self.$route.params.matchID)
            console.info('%cTeleop: %cfetchedMatch = %O', 'color: blue', 'color: black', fetchedMatch)
            if (fetchedMatch === undefined) {
                console.info('%cTeleop: %cCouldn\'t find match in store. Redirecting to create new match', 'color: blue', 'color: red')
                self.$router.push('/scout/new')
            }
            else {
                console.info('%cTeleop: %cLoading match data from Redux Store', 'color: blue', 'color: green')
                self.match = Object.assign({}, self.match, fetchedMatch)
            }
        },
        beforeDestroy () {
            let self = this
            self.saveChangesInRedux()
        },
        methods: {
            saveChangesInRedux () {
                let self = this
                let fetchedMatch = matchActions.fetchMatch(self.$select('matches'), self.$route.params.matchID)
                if (fetchedMatch !== undefined) {
                    console.info('%cTeleop: %cSaving to Redux Store', 'color: blue', 'color: black')
                    store.dispatch(matchActions.updateMatch(self.match.matchID, self.match))
                }
            }
        },
        data () {
            return {
                match: {
                    totalkPa: 0,
                    totalHoppers: 0,
                    tCollectedFromHopper: false,
                    collectedFuelOffGround: false,
                    totalGears: 0,
                    obtainedGearFromHumanPlayer: false,
                    obtainedGearFromFloor: false,
                    tShotLowGoal: false,
                    tHighGoalShotFrom: []
                },
                selectOptions: {
                    tHighGoalShotFrom: [
                        {label: 'Key', value: 'key'},
                        {label: 'Wall', value: 'wall'},
                        {label: 'Afar', value: 'afar'}
                    ]
                }
            }
        }
    }
</script>
