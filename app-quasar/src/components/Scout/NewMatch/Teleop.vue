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
                        <q-numeric v-model="match.hoppers" :min="0"></q-numeric>
                    </div>
                </div>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.collectedFromHopper"></q-checkbox>
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
                        <q-numeric v-model="match.gears" :min="0"></q-numeric>
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
                        <q-select class="full-width" type="checkbox" v-model="match.highGoalShotFrom" :options="selectOptions.highGoalShotFrom"></q-select>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data () {
            return {
                match: {
                    totalkPa: 0,
                    hoppers: 0,
                    collectedFromHopper: false,
                    collectedFuelOffGround: false,
                    gears: 0,
                    obtainedGearFromHumanPlayer: false,
                    obtainedGearFromFloor: false,
                    shotLowGoal: false,
                    gearPosition: null,
                    highGoalShotFrom: []
                },
                selectOptions: {
                    highGoalShotFrom: [
                        {label: 'Key', value: 'key'},
                        {label: 'Wall', value: 'wall'},
                        {label: 'Afar', value: 'afar'}
                    ]
                }
            }
        }
    }
</script>
