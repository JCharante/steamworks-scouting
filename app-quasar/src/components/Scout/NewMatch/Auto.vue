<template>
    <div>
        <div class="layout-padding">
            <div class="list">
                <div class="list-label">Autonomous Info</div>

                <div class="item two-lines">
                    <div class="item-content">
                        <span class="item-label">kPa: </span>
                        <q-numeric v-model="match.kPa" :min="0"></q-numeric>
                    </div>
                </div>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.crossedLine"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Crossed Line
                    </div>
                </label>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.dumpedHopper"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Dumped Hopper
                    </div>
                </label>

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
                        <q-checkbox v-model="match.lowGoal"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Low Goal
                    </div>
                </label>

                <div class="item two-lines">
                    <div class="item-content row items-center">
                        <label style="margin-right: 10px;">Gear Position:</label>
                        <br>
                        <q-select class="full-width" type="radio" v-model="match.gearPosition" :options="selectOptions.gearPosition"></q-select>
                    </div>
                </div>

                <label class="item">
                    <div class="item-primary">
                        <q-checkbox v-model="match.successfulGearPlacement"></q-checkbox>
                    </div>
                    <div class="item-content">
                        Successful Gear Placement
                    </div>
                </label>

                <div class="item two-lines">
                    <div class="item-content row items-center">
                        <label style="margin-right: 10px;">High Goal Position:</label>
                        <br>
                        <q-select class="full-width" type="radio" v-model="match.highGoalShotFrom" :options="selectOptions.highGoalShotFrom"></q-select>
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
                    kPa: 0,
                    crossedLine: false,
                    dumpedHopper: false,
                    collectedFromHopper: false,
                    lowGoal: false,
                    gearPosition: null,
                    successfulGearPlacement: false,
                    highGoalShotFrom: null
                },
                selectOptions: {
                    gearPosition: [
                        {label: 'None', value: null},
                        {label: 'Left', value: 'left'},
                        {label: 'Middle', value: 'middle'},
                        {label: 'Right', value: 'right'}
                    ],
                    highGoalShotFrom: [
                        {label: 'None', value: null},
                        {label: 'Key', value: 'key'},
                        {label: 'Wall', value: 'wall'},
                        {label: 'Afar', value: 'afar'}
                    ]
                }
            }
        }
    }
</script>
